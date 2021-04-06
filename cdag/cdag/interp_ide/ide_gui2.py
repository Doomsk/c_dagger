import sys
import regex
import subprocess
from PySide6 import QtWidgets
from PySide6.QtWidgets import (QApplication, QDialog, QVBoxLayout, QComboBox, QPushButton, QTabBar,
                               QTabWidget, QFileDialog, QGridLayout, QMainWindow, QStatusBar)
from PySide6.QtCore import (Slot, Qt, QRect, QSize, QRegularExpression,
                            QRegularExpressionMatchIterator)
from PySide6.QtGui import (QColor, QBrush, QPainter, QTextFormat, QFont, QTextCursor,
                           QSyntaxHighlighter, QTextCharFormat, QPalette)
from PySide6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit, QLabel
from interpreter.localization import (available_languages, from_code2lang, from_lang2code,
                                      map_lang2code, map_code2lang, highlighting)
from interpreter.interp import Interpreter

# TODO:
#  - this is the current version

git_version = subprocess.check_output(["git", "describe", "--always"]).strip()


class LineNumberArea(QWidget):
    def __init__(self, editor_):
        QWidget.__init__(self, editor_)
        self.codeEditor = editor_

    def sizeHint(self):
        return QSize(self.codeEditor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self):
        QPlainTextEdit.__init__(self)
        self.line_number_area = LineNumberArea(self)

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setFont(QFont('Menlo', 13, 550))
        palette = QPalette()
        palette.setColor(QPalette.Text, Qt.black)
        self.setPalette(palette)

        self.setMinimumWidth(250)
        self.setMinimumHeight(200)

        self.blockCountChanged[int].connect(self.update_line_number_area_width)
        self.updateRequest[QRect, int].connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_area_width(0)
        self.highlight_current_line()
        self.codegroupbox = QtWidgets.QGroupBox('Code Editor')

    def line_number_area_width(self):
        digits = 2
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num *= 0.1
            digits += 1

        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def resizeEvent(self, e):
        super().resizeEvent(e)
        cr = self.contentsRect()
        width = self.line_number_area_width()
        rect = QRect(cr.left(), cr.top(), width, cr.height())
        self.line_number_area.setGeometry(rect)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), Qt.lightGray)
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        offset = self.contentOffset()
        top = self.blockBoundingGeometry(block).translated(offset).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.black)
                width = self.line_number_area.width()
                height = self.fontMetrics().height()
                painter.drawText(0, top, width, height, Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    @Slot()
    def update_line_number_area_width(self, newBlockCount):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    @Slot()
    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            width = self.line_number_area.width()
            self.line_number_area.update(0, rect.y(), width, rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    @Slot()
    def highlight_current_line(self):
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor('#eff9f9')
            selection.format.setBackground(line_color)

            selection.format.setProperty(QTextFormat.FullWidthSelection, True)

            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()

            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)


class CdagSyntax(QSyntaxHighlighter):
    def __init__(self, parent, lang):
        super(CdagSyntax, self).__init__(parent)
        self.lang = lang

    def highlightBlock(self, text):
        qc_ = QColor()
        qc_.name(QColor.HexRgb)
        for hk, hv in highlighting.items():
            tcf = QTextCharFormat()
            if hk not in ['elements', 'misc', 'string', 'extra', 'bools', 'attr_types']:
                tcf.setFontWeight(QFont.DemiBold)
            elif hk in ['misc', 'elements']:
                tcf.setFontWeight(QFont.Black)
            qbc = QBrush()
            qbc.setColor(hv[1])
            tcf.setForeground(qbc.color())
            if hk in ['actions', 'attr_types', 'bools', 'complements']:
                if self.lang not in ['', 'en']:
                    new_hv = [from_code2lang[self.lang][i] for i in hv[0]]
                else:
                    new_hv = hv[0]
            else:
                new_hv = hv[0]
            k_ = '|'.join([k for k in new_hv])
            if hk in ['actions', 'complements', 'extra', 'bools']:
                expr = rf'(?<!\w)({k_})(?!\w)'
            else:
                expr = rf'{k_}'
            r = QRegularExpression(expr,
                                   options=QRegularExpression.ExtendedPatternSyntaxOption | QRegularExpression.UseUnicodePropertiesOption)
            a = QRegularExpressionMatchIterator(r.globalMatch(text))
            while a.hasNext():
                n = a.next()
                self.setFormat(n.capturedStart(), n.capturedLength(), tcf)


class MainDialog(QMainWindow):
    def __init__(self):
        super(MainDialog, self).__init__()
        self.tabnum = 0

        self.setWindowTitle("C† Code Editor")
        self.cursor1 = QTextCursor()

        self.fname_list = []
        self.cur_data = []
        self.lang_list = []
        self.itprtr = Interpreter()

        # Open/New/Save buttons as vertical layout
        self.opopt = QtWidgets.QGroupBox('File')
        vlayout = QtWidgets.QVBoxLayout()
        self.pb = QtWidgets.QPushButton("Open code file...")
        self.pb.setFocusPolicy(Qt.NoFocus)
        self.nb = QtWidgets.QPushButton("New file")
        self.nb.setFocusPolicy(Qt.NoFocus)
        self.sb = QtWidgets.QPushButton("Save current file")
        self.sb.setFocusPolicy(Qt.NoFocus)
        vlayout.addWidget(self.pb)
        vlayout.addWidget(self.nb)
        vlayout.addWidget(self.sb)
        self.opopt.setLayout(vlayout)

        # Language preferences as horizontal layout
        self.langopt = QtWidgets.QGroupBox('Language Options')
        llayout = QtWidgets.QGridLayout()
        self.lcb_w = QtWidgets.QComboBox()
        self.lcb_w.setEditable(False)
        self.lcb_w.setInsertPolicy(QComboBox.InsertAlphabetically)
        self.lcb_w.addItems(available_languages)
        llayout.addWidget(QLabel('Write code in:'), 0, 0)
        llayout.addWidget(self.lcb_w, 0, 1)

        self.lcb_r = QtWidgets.QComboBox()
        self.lcb_r.setEditable(False)
        self.lcb_r.setInsertPolicy(QComboBox.InsertAlphabetically)
        self.lcb_r.addItems(available_languages)
        llayout.addWidget(QLabel('Load code from:'), 1, 0)
        llayout.addWidget(self.lcb_r, 1, 1)
        self.langopt.setLayout(llayout)

        # Run layout
        self.runl = QtWidgets.QGroupBox()
        rlayout = QtWidgets.QHBoxLayout()
        self.rb = QtWidgets.QPushButton("Run")
        self.rb.setStyleSheet('QPushButton {background-color: #46ab13; color: #ffffff; max-width: 80px; max-height: 30px;}')
        self.rb.setFocusPolicy(Qt.NoFocus)
        rlayout.addWidget(self.rb)
        self.runl.setLayout(rlayout)

        # File Buttons + Language + Run layout
        self.null_layout = QtWidgets.QGroupBox()
        nulllayout = QtWidgets.QHBoxLayout()
        nulllayout.addWidget(QLabel(f'git version: {git_version.decode()}'))
        self.null_layout.setLayout(nulllayout)
        self.right_layout = QtWidgets.QGroupBox()
        lrl = QtWidgets.QGridLayout()
        lrl.addWidget(self.opopt, 0, 0)
        lrl.addWidget(self.langopt, 0, 1)
        lrl.addWidget(self.null_layout, 1, 0)
        lrl.addWidget(self.runl, 1, 1)
        self.right_layout.setLayout(lrl)

        # StatusBar
        self.sbar = QStatusBar()
        self.setStatusBar(self.sbar)
        self.sbarll = self.statusbarlanguagelabel()
        self.sbar.addWidget(self.sbarll)

        # Button click dynamics
        self.tabwidget = QTabWidget()
        self.tabwidget.setTabsClosable(True)
        self.pb.clicked.connect(self.onclickopenb)
        self.nb.clicked.connect(self.onclicknewb)
        self.sb.clicked.connect(self.onclicksaveb)
        self.rb.clicked.connect(self.onclickrunb)

        # Main layout
        main = QVBoxLayout()
        main.addWidget(self.right_layout)
        main.addWidget(self.tabwidget)
        self.tabwidget.tabCloseRequested.connect(self.onclosetab)

        # Setting up the window
        self.dial_ = QWidget()
        self.dial_.setLayout(main)
        self.setCentralWidget(self.dial_)

    @Slot()
    def onclickrunb(self):
        cur_tab = self.tabwidget.currentWidget()
        code_ = cur_tab.toPlainText()
        if len(self.lcb_w.currentText()) > 0:
            lang_ = self.lcb_w.currentText()
        else:
            lang_ = 'en'
        self.rb.setEnabled(False)
        ai = Interpreter()
        res_ = ai.run(code_, lang=lang_)
        print(res_)
        self.rb.setEnabled(True)

    @Slot()
    def onclickopenb(self):
        file_ = QFileDialog.getOpenFileName()
        try:
            with open(file_[0], 'r') as f_:
                code_ = f_.read()
            ccode = CodeEditor()
            short_name = '.../' + file_[0].split('/')[-1]
            if len(self.lcb_w.currentText()) > 0:
                lang_ = self.lcb_w.currentText()
                code_ = map_code2lang(code_, self.lcb_w.currentText())
            else:
                lang_ = 'en'

            a = CdagSyntax(ccode.document(), lang_)
            a.rehighlight()
            ccode.insertPlainText(code_)

            cursor_ = QTextCursor(ccode.textCursor())
            self.tabwidget.addTab(ccode, short_name)
            self.tabwidget.setCurrentWidget(ccode)
            idx = self.tabwidget.currentIndex()
            self.fname_list.append({'path': file_[0], 'short': short_name})
            self.cur_data.append(code_)
            self.lang_list.append(lang_)
            cursor_.movePosition(QTextCursor.Start)
            ccode.setTextCursor(cursor_)

            self.tabwidget.currentWidget().textChanged.connect(self.onchangetext)
            self.setsbar()
        except FileNotFoundError as error:
            pass

    @Slot()
    def onclicknewb(self):
        new_tab = CodeEditor()
        self.tabwidget.addTab(new_tab, '* untitled.c†')
        self.tabwidget.setCurrentWidget(new_tab)
        fname = 'untitled'
        new_idx = self.tabwidget.currentIndex()
        self.tabnum += 1
        fname = fname + str(self.tabnum) + '.c†'
        self.fname_list.append({'path': '', 'short': fname})
        self.cur_data.append('')
        if len(self.lcb_w.currentText()) > 0:
            lang_ = self.lcb_w.currentText()
        else:
            lang_ = 'en'
        self.tabwidget.setTabText(new_idx, '* ' + fname + f' [{lang_}]')
        self.lang_list.append(lang_)

        a = CdagSyntax(new_tab.document(), lang_)
        a.rehighlight()
        new_tab.insertPlainText('')

        cursor_ = QTextCursor(new_tab.textCursor())
        cursor_.movePosition(QTextCursor.Start)
        new_tab.setTextCursor(cursor_)
        self.tabwidget.currentWidget().textChanged.connect(self.onchangetext)
        self.setsbar()

    @Slot()
    def onclicksaveb(self):
        idx = self.tabwidget.currentIndex()
        fdirname = self.fname_list[idx]['path']
        if fdirname is not None:
            fdir = ''.join(fdirname.split('/')[:-1])
        else:
            fname = self.tabwidget.tabText(self.tabwidget.currentIndex()).strip('*').strip(' ')
            fdir = fname
        qfd = QFileDialog()
        qfd.setAcceptMode(QFileDialog.AcceptSave)
        text = self.tabwidget.currentWidget().toPlainText()
        qfd.setFileMode(QFileDialog.AnyFile)
        fres = qfd.getSaveFileName(caption='Save As...', dir=fdir, filter='C† file (*.c†)')
        sfls = fres[0].split('/')[-1]
        with open(fres[0], 'w') as f_:
            f_.write(text)
        self.tabwidget.setTabText(idx, '.../' + sfls)
        self.fname_list[idx].update({'path': fres[0], 'short': sfls})
        self.cur_data[idx] = self.tabwidget.currentWidget().toPlainText()

    def onclickstopb(self):
        pass

    @Slot()
    def onchangetext(self):
        idx = self.tabwidget.currentIndex()
        tab_ = self.tabwidget.currentWidget()
        text_content = tab_.toPlainText()
        tab_name = self.tabwidget.tabText(idx)
        if text_content != self.cur_data[idx] or self.cur_data[idx] == '':
            if '*' not in tab_name[0]:
                self.tabwidget.setTabText(idx, '* ' + tab_name + f' [{self.lang_list[idx]}]')
        else:
            if '*' in tab_name[0]:
                self.tabwidget.setTabText(idx, tab_name[2:] + f' [{self.lang_list[idx]}]')

    @Slot()
    def onclosetab(self, idx):
        self.tabwidget.removeTab(idx)
        self.fname_list.pop(idx)
        self.cur_data.pop(idx)
        self.lang_list.pop(idx)
        if self.tabwidget.count() == 0:
            self.onclicknewb()

    @Slot()
    def movingcursor(self):
        print(self.tabwidget.currentWidget().textCursor().position())
        print(self.cursor1.positionInBlock(), self.cursor1.blockNumber())

    @Slot()
    def statusbarlanguagelabel(self):
        return QLabel(f'lang: {"en" if self.lcb_w.currentText() == "" else self.lcb_w.currentText()}')

    @Slot()
    def setsbar(self):
        self.sbar.removeWidget(self.sbarll)
        self.sbarll = self.statusbarlanguagelabel()
        self.sbar.addWidget(self.sbarll)

    def statusbar(self):
        pass

    @Slot()
    def savedialog(self, idx):
        pass


if __name__ == '__main__':
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    editor = MainDialog()
    editor.show()
    sys.exit(app.exec_())
