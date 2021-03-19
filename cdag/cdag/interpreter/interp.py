from interpreter.actions import ActionsInterp
from interpreter.localization import map_lang2code, available_languages
import gpp.gpp_yacc as g
import hashlib
import time
import sys
import traceback as tb


class Interpreter(ActionsInterp):
    def __init__(self):
        super(Interpreter, self).__init__()

    def run(self, code, **kwargs):
        _lang = kwargs.get('lang', 'en')
        if _lang in available_languages:
            t_0 = time.process_time()
            code = map_lang2code(code, _lang)
            t_1 = time.process_time()
            if kwargs.get('time_delta', False):
                print(f'{round(t_1 - t_0, 9)}s')
            _r = {}
            t0 = time.process_time()
            _c = g.parse(code)
            if _c not in [None, -11]:
                code_hash = hashlib.md5(code.encode())
                code_id = code_hash.hexdigest()
                self.parse_details(code_id, _c)
                try:
                    _exec = self.execute_parse(code_id, _c, _c)
                except Exception as ee:
                    _e = sys.exc_info()[0]
                    err_ = ''.join(tb.format_exception(None, ee, ee.__traceback__))
                    print('* Error: ', _e, ee)
                    print(err_, '\n')
                    _exec = -1
                    _r.update({'error_msg': 'execute_parse error'})
                _r.update({'return_code': _exec})
                t1 = time.process_time()
                if kwargs.get('time_delta', False):
                    _r.update({'execution_time(s)': round(t1 - t0, 9)})
            else:
                t1 = time.process_time()
                _exec = _c
                if _exec == -11:
                    error_msg = 'parser error'
                elif _exec is None:
                    error_msg = 'probably lexer error'
                else:
                    error_msg = 'unknown error'
                _r.update({'return_code': _exec,
                           'execution_time(s)': round(t1 - t0, 9),
                           'error_msg': error_msg})
        else:
            _r = {'return_code': -1111, 'error_msg': 'language not available!'}
        return _r


if __name__ == '__main__':
    ai = Interpreter()

    code1 = """ main: sets [10 "hoi quantum!"] as v1 v7 
                     applies [with x: maps [v1 4] & with y: maps [v7]] as v2 v6 
                     adds [v2 5] as v3
                     outputs [v3 v6] 
               where x: sets [*v1 *v2] as v1 v2 
                        multiplies [10 v1 v2] as v3 
                        uses [v3]
               where y: sets [*v1] as v1 
                        adds [v1 " this" " is" " a" " test"] as v2 
                        uses [v2]"""
    r = ai.run(code1, time_delta=True)
    print(r)

    code2 = """ a: sets [3] as あ0 sets [$щ]_1...あ0 as か$n_1...あ0 adds [か$й]_1...あ0 as さ5 outputs [さ5]"""
    r2 = ai.run(code2, time_delta=True)
    print(r2)

    code3 = """ main: seta [10 "oi quântico!"] como v1 v7 
                         aplica [com x: mapeia [v1 4] & com y: mapeia [v7]] como v2 v6 
                         adiciona [v2 5] como v3
                         apresenta [v3 v6] 
                   onde x: seta [*v1 *v2] como v1 v2 
                            multiplica [10 v1 v2] como v3 
                            usa [v3]
                   onde y: seta [*v1] como v1 
                            adiciona [v1 " isso" " é" " um" " teste"] como v2 
                            usa [v2]"""
    r3 = ai.run(code3, time_delta=True, lang='pt')
    print(r3)

    code4 = """test: outputs ["insert your text here: "] inputs [string] as v1 adds ["ah! " v1] as v2 outputs [v2] """
    r4 = ai.run(code4, time_delta=True)
    print(r4)
