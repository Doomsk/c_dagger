import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import (QApplication, QDialog, QVBoxLayout, QComboBox, QPushButton, QTabBar,
                               QTabWidget, QFileDialog, QGridLayout)
from PySide6.QtCore import (Slot, Qt, QRect, QSize, QPoint, QSaveFile, QKeyCombination,
                            QRegularExpression, QRegularExpressionMatch,
                            QRegularExpressionMatchIterator)
from PySide6.QtGui import (QColor, QPainter, QTextFormat, QFont, QTextCursor,
                           QCloseEvent, QShortcutEvent, QShortcut, QKeySequence, QSyntaxHighlighter,
                           QTextCharFormat, QTextDocument)
from PySide6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit, QLabel
from interpreter.localization import (available_languages, from_code2lang, from_lang2code,
                                      map_lang2code, map_code2lang)
from interpreter.interp import Interpreter

#TODO:
# - get reserved keywords from gpp_lex not localization (more complete highlighting)
# - put different color highlights on different scopes


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
        self.setFont(QFont('Menlo', 13))

        self.setMinimumWidth(600)
        self.setMinimumHeight(600)

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
            line_color = QColor(Qt.yellow).lighter(160)
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
        tcf = QTextCharFormat()
        tcf.setFontWeight(QFont.DemiBold)
        tcf.setForeground(Qt.darkMagenta)
        for k, v in from_lang2code[self.lang].items():
            expr = rf'({k})(?!\w)'
            r = QRegularExpression(expr)
            a = QRegularExpressionMatchIterator(r.globalMatch(text))
            while a.hasNext():
                n = a.next()
                self.setFormat(n.capturedStart(), n.capturedLength(), tcf)


class MainDialog(QDialog):
    def __init__(self):
        super(MainDialog, self).__init__()

        self.setWindowTitle("C† Code Editor")
        self.fname_list = {}
        self.cur_data = {}
        self.itprtr = Interpreter()

        # Open/Save buttons as vertical layout
        self.opopt = QtWidgets.QGroupBox('File')
        vlayout = QtWidgets.QVBoxLayout()
        self.pb = QtWidgets.QPushButton("Open code file...")
        self.pb.setFocusPolicy(Qt.NoFocus)
        self.sb = QtWidgets.QPushButton("Save current file")
        self.sb.setFocusPolicy(Qt.NoFocus)
        vlayout.addWidget(self.pb)
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

        # Buttons + Language layout
        self.upper_layout = QtWidgets.QGroupBox('Menu')
        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.opopt, 0, 0)
        grid.addWidget(self.langopt, 0, 1)
        self.upper_layout.setLayout(grid)

        # Main layout
        main = QVBoxLayout()
        main.addWidget(self.upper_layout)

        # Editor tabs dynamics
        self.tabwidget = QTabWidget()
        self.tabwidget.setTabsClosable(True)
        self.pb.clicked.connect(self.onclickopenb)
        self.tabwidget.addTab(CodeEditor(), '* untitled.c†')
        self.fname_list.update({self.tabwidget.currentIndex(): {'path': None,
                                                                'short': 'untitled.c†'}})
        self.cur_data.update({self.tabwidget.currentIndex(): ''})
        main.addWidget(self.tabwidget)
        self.tabwidget.tabCloseRequested.connect(self.onclosetab)
        self.tabwidget.currentWidget().textChanged.connect(self.onchangetext)

        self.setLayout(main)

    @Slot()
    def savetext(self):
        pass


    @Slot()
    def onclickopenb(self):
        file_ = QFileDialog.getOpenFileName()
        with open(file_[0], 'r') as f_:
            code_ = f_.read()
        ccode = CodeEditor()
        short_name = '.../' + file_[0].split('/')[-1]
        if len(self.lcb_w.currentText()) > 0:
            lang_ = self.lcb_w.currentText()
            print('foi?')
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
        self.fname_list.update({idx: {'path': file_[0], 'short': short_name}})
        self.cur_data.update({idx: code_})
        cursor_.movePosition(QTextCursor.Start)
        ccode.setTextCursor(cursor_)

        self.tabwidget.currentWidget().textChanged.connect(self.onchangetext)

    def onclicksaveb(self):
        pass

    def onclickrunb(self):
        pass

    def onclickstopb(self):
        pass

    @Slot()
    def onchangetext(self):
        idx = self.tabwidget.currentIndex()
        text_content = self.tabwidget.currentWidget().toPlainText()
        tab_name = self.tabwidget.tabText(idx)
        if text_content != self.cur_data[idx]:
            if '*' not in tab_name[0]:
                self.tabwidget.setTabText(idx, '* ' + tab_name)
        else:
            if '*' in tab_name[0]:
                self.tabwidget.setTabText(idx, tab_name[2:])

    @Slot()
    def onclosetab(self, idx):
        self.tabwidget.removeTab(idx)
        self.fname_list.pop(idx)
        self.cur_data.pop(idx)
        if self.tabwidget.count() == 0:
            new_tab = CodeEditor()
            self.tabwidget.addTab(new_tab, '* untitled.c†')
            self.tabwidget.currentWidget().textChanged.connect(self.onchangetext)

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
