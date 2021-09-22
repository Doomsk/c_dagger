import os
import regex
import json
import pathlib
from gpp.gpp_lex import actions, complements, numeric_expr, attr_types
import gpp_yacc8 as g8


fff = os.path.abspath(os.getcwd())
fff2 = os.path.basename(__file__)
fff3 = pathlib.Path(__file__).parent.absolute()
fff4 = os.path.dirname(os.path.abspath(__file__))
gpp_yacc_file_name = os.path.join(fff4, "gpp_yacc8.py")
lcbracket = '{'
rcbracket = '}'
tab = ' ' * 4
newl = '\n'


class YACC8Maker:
    def __init__(self):
        pass


def next_func_enum(func_name, num=None):
    try:
        with open(gpp_yacc_file_name, 'r') as f:
            code_ = f.read()
    except FileNotFoundError:
        if num is not None:
            vals = 0
        else:
            vals = num
    else:
        res = regex.findall(rf'{func_name}_[0-9]+', code_)
        vals = int(sorted(res, reverse=True)[0][-1])
        vals += 1
    return vals


def generator(grammar, rule_code, this_func='sentence', replace=False, num=None):
    tab = ' ' * 4
    newl = '\n'

    if not replace:
        func_header = f"""def p_{this_func}_{next_func_enum(this_func, num=num)}"""
    else:
        func_header = f"""def p_{this_func}_{num}"""

    code_, res, _ = recur(rule_code)
    if 'pass' in code_:
        p0 = ""
    else:
        p0 = f"p[0] = res0{newl}"
    r = f"""{func_header}(p):{newl}{tab}\"\"\" {grammar} \"\"\"{newl}{code_}"""
    if len(code_) > 0:
        r += f"{tab}{p0}{newl}{newl}"
    else:
        r += f"{tab}pass{newl}{newl}{newl}"
    return r


def check_type(value):
    if value is None:
        return None
    else:
        return type(value)


def is_type(value, tp):
    return isinstance(value, tp)


def priority(value):
    types = [dict, tuple, str]
    for i in value:
        for y in types:
            if is_type(i, y):
                return y
    return None


def init(tp):
    if tp == dict:
        return "dict()"
    elif tp == tuple:
        return "()"
    elif tp == str:
        return "\"\""


def inc(value, tp):
    if tp == dict:
        return f".update({value})"
    else:
        return f" += {value}"


def recur(u, idx=0):
    res = ''
    text = ''
    ans = check_type(u)
    if not is_type(u, int) and not is_type(u, float) and not is_type(u, list):
        text = f"{tab}res{idx} = {init(ans)}{newl}"
    if is_type(u, list):
        ktype = priority(u)
        for i0, k in enumerate(u):
            ttmp, rtmp, atmp = recur(k, idx + 1)
            text += ttmp
            value = rtmp
            res = f"res{idx}"
            if i0 == 0:
                text += f"{tab}{res} = {value}{newl}"
            else:
                text += f"{tab}{res}{inc(value, ktype)}{newl}"
    elif is_type(u, tuple):
        if len(u) > 0:
            for k in u:
                ktype = check_type(k)
                ttmp, rtmp, atmp = recur(k, idx + 1)
                text += ttmp
                value = f"({rtmp},)"
                res = f"res{idx}"
                text += f"{tab}{res}{inc(value, ans)}{newl}"
        else:
            text = f"{tab}pass{newl}"
    elif is_type(u, dict):
        for k, v in u.items():
            vtype = check_type(v)
            ttmp, rtmp, atmp = recur(v, idx + 1)
            text += ttmp
            value = f"[(\"{k}\", {rtmp})]"
            res = f"res{idx}"
            text += f"{tab}{res}{inc(value, ans)}{newl}"
    elif is_type(u, str):
        res = f"\"{u}\""
        if idx == 0:
            text = f"{tab}res0 = {res}{newl}"
        else:
            text = ''
    elif is_type(u, int):
        res = f"p[{u}]"
        if idx == 0:
            text = f"{tab}res0 = {res}{newl}"
        else:
            text = ''
    elif is_type(u, float):
        res = f"p[{int(u)}]"
        if idx == 0:
            text = f"{tab}res0 = {res}{newl}"
        else:
            text = f"{tab}if {res} is not None:{newl}{tab}"
    else:
        pass
    return text, res, ans


full_grammar = {"tale : root_sentence compl_sentence": [1, 2.0],
                "root_sentence : subj ':' clause": (
                    {'subject': (1,), 'type': ('root',)}, (3,)),
                "obj_sentence : subj ':' clause": ({'subject': (1,), 'type': ('obj',)}, (3,)),
                "next_sentence : clause next_sentence": [1, 2.0],
                "next_sentence : ": (),
                "compl_sentence : where sup_sentence compl_sentence": [2, 3],
                "compl_sentence : ": (),
                "sup_sentence : subj ':' clause": ({'subject': (1,), 'type': ('aux',)}, (3,)),
                "subj : subj_list": 1,
                "clause : action obj_expr attr_expr next_sentence": [[{'action': 1}, 2, 3], 4.0],
                "clause : action obj_expr attr_expr": [{'action': 1}, 2, 3],
                "clause : action obj_expr next_sentence": [[{'action': 1}, 2], 3.0],
                "clause : action obj_expr": [{'action': 1}, 2],
                "action : action_list": 1,
                "action : at action_list": (['@', 2],),
                "obj_expr : lbracket obj rbracket compl_obj": [{'object': 2}, 4.0],
                "obj : obj_subj": 1,
                "obj : pure_obj": (1,),
                "obj2 : and obj": [('&',), 2],
                "obj2 : ": (),
                "pure_obj : obj_list": 1,
                "pure_obj : obj_list pure_obj": [1, 2],
                "pure_obj : obj_list obj2": [1, 2.0],
                "obj_subj : with obj_sentence": [('with',), 2],
                "obj_subj : with obj_sentence obj2": [('with',), 2, 3.0],
                "obj_subj : if obj_sentence obj2": [('if',), 2, 3.0],
                "obj_subj : if obj_sentence else next_sentence obj2": [('if',), 2, ('else',), 4,
                                                                       5.0],
                "compl_obj : obj_loop": {'obj_loop': (1,)},
                "compl_obj : ": (),
                "obj_loop : loop obj_loop": [1, 2.0],
                "obj_loop : ": (),
                "attr_expr : as attr_vals": {'attr': 2},
                "attr_vals : attr_group": (1,),
                "attr_vals : attr_group attr_vals": [(1,), 2],
                "attr_group : attr_list": 1,
                "attr_group : at attr_list": ["@", 2],
                "attr_group : attr_list loop": ([{'attr_val': 1}, 2],),
                "attr_group : at attr_list loop": ([{'attr_val': ["@", 2]}, 3],),
                "attr : at attr_list": (['@', 2],),
                "attr : attr_list": (1,),
                "attr : at attr_list attr": [(['@', 2],), 3],
                "attr : attr_list attr": [(2,), 3],
                "compl_attr : attr_loop": {'attr_loop': (1,)},
                "compl_attr : ": (),
                "attr_loop : loop attr_loop": [1, 2.0],
                "attr_loop : ": (),
                "loop : underscore id dots left_cur loop_vals right_cur": [{'var_loop': (2,)}, 4, 5,
                                                                           6],
                "left_cur : lbracket": {'init_lim': ('close',)},
                "left_cur : lparen": {'init_lim': ('open',)},
                "right_cur : rbracket": {'fin_lim': ('close',)},
                "right_cur : rparen": {'fin_lim': ('open',)},
                "loop_vals : loop_list": {'single': (1,)},
                "loop_vals : loop_list loop_list": {'init': (1,), 'fin': (2,)},
                "loop_vals : at loop_list loop_list": {'init': (['@', 1],), 'fin': (2,)},
                "loop_vals : loop_list at loop_list": {'init': (1,), 'fin': (['@', 2],)},
                "loop_vals : at loop_list at loop_list": {'init': (['@', 1],), 'fin': (['@', 2],)}}


def def_values_list(rule=None):
    if rule in ['subj_list', 'attr_list']:
        vals_list = ["id", "dollar id", "id dollar id", "id period id", "dollar id period id",
                     "id dollar id period id"]
    elif rule == 'obj_list':
        vals_list = ["id", "dollar id", "id dollar id", "str", "str dollar id", "bin", "bool",
                     "hex", "qubit", "realnum"]
        vals_list.extend(attr_types)
    elif rule == 'loop_list':
        vals_list = ["id", "realnum", "str"]
    elif rule == 'error_handler_list':
        vals_list = ["id period id", "dollar id period id", "id dollar id period id"]
    else:
        vals_list = []

    if len(vals_list) > 0:
        vals_grammar = {}
        for i in vals_list:
            i_vals = i.split(' ')
            if len(i_vals) == 1:
                vals_grammar.update({f"{rule} : {i}": 1})
            elif i_vals[0] == 'dollar':
                if 'period' in i_vals:
                    vals_grammar.update({f"{rule} : {i}": {'var_loop': (2,), 'prop': (4,)}})
                else:
                    vals_grammar.update({f"{rule} : {i}": {'var_loop': (2,)}})
            elif i_vals[1] == 'dollar':
                if 'period' in i_vals:
                    vals_grammar.update(
                        {f"{rule} : {i}": {'ref': (1,), 'var_loop': (3,), 'prop': (5,)}})
                else:
                    vals_grammar.update({f"{rule} : {i}": {'ref': (1,), 'var_loop': (3,)}})
            elif i_vals[1] == 'period':
                vals_grammar.update({f"{rule} : {i}": {'ref': (1,), 'prop': (3,)}})
    else:
        vals_grammar = {}

    return vals_grammar


actions_grammar = {f"action_list : {i}": (1,) for i in actions}
subj_grammar = def_values_list('subj_list')
obj_grammar = def_values_list('obj_list')
attr_grammar = def_values_list('attr_list')
loop_grammar = def_values_list('loop_list')
full_grammar.update(actions_grammar)
full_grammar.update(subj_grammar)
full_grammar.update(obj_grammar)
full_grammar.update(attr_grammar)
full_grammar.update(loop_grammar)


def big_wrapper(file_path=gpp_yacc_file_name, replace=True):
    c = "import gpp.yacc as yacc\nfrom gpp.gpp_lex import tokens, actions\n\n\n"
    for n, v in enumerate(full_grammar.items()):
        c += generator(grammar=v[0], rule_code=v[1], replace=replace, num=n)

    c += """parser = yacc.yacc()


def parse(data, debug=0):
    parser.error = 0
    p = parser.parse(data, debug=debug)
    if p is None:
        return -11
    return p

    """
    if replace:
        k = 'w'
    else:
        k = 'a'
    with open(file_path, k) as f:
        f.write(c)


def runny9():
    big_wrapper()
    c = []
    c.append("""a: sets [*v1]""")
    c.append("""b: sets [*v1 *v2]""")
    c.append("""c: sets [*v1] as v1""")
    c.append("""d: sets [*v1 *v2] as v1 v2""")
    c.append("""e: sets [*v$n]_n...[1 3] as v$k_k...(0 4)""")
    c.append("""f: sets [*v1] multiplies [4]""")
    c.append("""g: sets [*v1] multiplies [with f: maps [0]] where f: uses [5]""")
    c.append("""h: sets [*v1] as v1 multiplies [with f: maps [0] & with g: maps [v1]] where f: uses [5] where g: adds [$q]_q...[1 5]""")
    c.append("""i: sets [*v$k v$e]_k...[1 3]_e...[5 10]""")
    c.append("""j: sets [*v$k v$e]_k...[1 3]_e...[5 10] as v$c_c...(0 4) v$y_y...[5 11)""")

    for i0, i in enumerate(c):
        white_space = " "*(len(str(i0)) + 2)
        print(f'{i0}) code=\n{2*white_space}{i}')
        try:
            print(f'{white_space}parse=\n{2*white_space}{g8.parse(i)}\n{"-"*60}')
        except Exception as e:
            print(f'{white_space}parse=\n{2*white_space}*** Error: {e}\n{"-"*60}')


if __name__ == '__main__':
    runny9()

