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
gpp_yacc_file_name = "gpp_yacc8.py"
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
    new_x = ''.join(grammar.split(':')[1:]).split(' ')

    if not replace:
        func_header = f"""def p_{this_func}_{next_func_enum(this_func, num=num)}"""
    else:
        func_header = f"""def p_{this_func}_{num}"""

    code_, res, _ = recur9(rule_code)
    # if 'res ' not in code_:
    #    p0 = "p[0] = res2"
    # elif f'{tab}res = (){newl}' == code_:
    #    p0 = "pass"
    # else:
    #    p0 = "p[0] = res"
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


def check_values(params):
    find_floats = regex.findall(r'p\[\d+\.0\]', ''.join(params))
    print(params, find_floats)
    tab = ' ' * 4
    newl = '\n'
    text = ''
    for i0, i in enumerate(params):
        if len(find_floats) > 0:
            for k in find_floats:
                if k in i:
                    new_k = k.replace('.0', '')
                    new_i = i.replace('.0', '')
                    text += f'{tab}if {new_k} is not None:{newl}{tab}{tab}res += {new_i}{newl}'
                else:
                    text += f'{tab}res += {i}{newl}'
                break
        else:
            text = f"{tab}res = {' + '.join(params)}{newl}"
    return text


def recurser2(u, idx=0, ans=None):
    text = ''
    tab = ' ' * 4
    newl = '\n'
    res = None
    r_tmp = []
    t_tmp = ''
    a_tmp = None
    res_rec = []
    res_tmp = []
    res_dict = {}
    if isinstance(u, dict) or isinstance(u, set):
        if idx == 0:
            text += f'{tab}res = dict(){newl}'
        if isinstance(u, dict):
            v = u.items()
        elif isinstance(u, set):
            v = u
        else:
            v = u
        for i in v:
            if isinstance(u, dict):
                k, i = i[0], i[1]
            if isinstance(i, tuple):
                r_tmp, t_tmp, a_tmp = recurser2(i, idx=idx + 1, ans=ans)
                res_tmp.append(r_tmp)
            elif isinstance(i, list):
                r_tmp, t_tmp, a_tmp = recurser2(i, idx=idx + 1, ans=ans)
                res_tmp.append(r_tmp)
            elif isinstance(i, int) or isinstance(i, float):
                r_tmp, t_tmp, a_tmp = recurser2(i, idx=idx + 1, ans=ans)
                res_tmp.append(r_tmp)
            elif isinstance(i, dict):
                res_rec = recurser2(i, idx=1)
            elif isinstance(i, str):
                r_tmp, t_tmp, a_tmp = recurser2(i, idx=idx + 1, ans=ans)
                res_tmp.append(r_tmp)
            res_rec = ' + '.join(res_tmp)
            if isinstance(u, dict):
                if k in ['subject', 'type', 'init', 'fin', 'var_loop', 'prop', 'ref', 'init_lim',
                         'fin_lim']:
                    text += f'{tab}res.update([("{k}", ({res_rec},))]){newl}'
                else:
                    text += f'{tab}res.update([("{k}", {res_rec})]){newl}'
            else:
                text += f'{tab}res.update({t_tmp}){newl}'
            res_tmp = []
        if a_tmp != 'tuple':
            ans = 'dict'
        res = f"{str(res_dict)}"

    elif isinstance(u, tuple) or isinstance(u, list):
        if isinstance(u, tuple):
            ans = 'tuple'
        else:
            ans = None
        if idx == 0:
            if isinstance(u, tuple):
                text += f"{tab}res2 = (){newl}"
            elif isinstance(u, list):
                text = f'{tab}res = (){newl}'

        if len(u) > 1:
            for i in u:
                if isinstance(i, tuple):
                    r_tmp, t_tmp, a_tmp = recurser2(i, idx=idx + 1, ans=ans)
                    res_tmp.append(f"({r_tmp},)")
                    if ans is not None:
                        text += t_tmp
                elif isinstance(i, list):
                    r_tmp, t_tmp, a_tmp = recurser2(i, idx=idx + 1, ans=ans)
                    res_tmp.append(r_tmp)
                    text += t_tmp
                elif isinstance(i, int) or isinstance(i, float):
                    r_tmp, t_tmp, a_tmp = recurser2(i, idx=idx + 1, ans=ans)
                    res_tmp.append(r_tmp)
                    if a_tmp == 'dict':
                        text += f"{tab}res.update({t_tmp}){newl}"
                    elif a_tmp == 'tuple':
                        text += f"{tab}res2 += {t_tmp}{newl}"
                    else:
                        pass
                elif isinstance(i, dict) or isinstance(i, set):
                    text += f'{tab}res = dict(){newl}'
                    r_tmp, t_tmp, a_tmp = recurser2(i, idx=idx + 1, ans=ans)
                    res_tmp.append(r_tmp)
                    ans = a_tmp
                    text += t_tmp
                elif isinstance(i, str):
                    r_tmp, t_tmp, a_tmp = recurser2(i, idx=idx + 1, ans=ans)
                    res_tmp.append(r_tmp)

            if isinstance(u, tuple):
                if ans is None:
                    res = f"{' + '.join(res_tmp)}"
                elif ans == 'tuple':
                    res = f"{' + '.join(res_tmp)}"
                    if 'res = dict()' in text:
                        text += f"{tab}res = (res,) + res2{newl}"
                    else:
                        text += f"{tab}res = res2{newl}"
                elif ans == 'dict':
                    res = f"{' + '.join(res_tmp)}"
            elif isinstance(u, list):
                if ans is None:
                    ##### write here checking
                    # res = f"{' + '.join(res_tmp)}"
                    # print(u, res)
                    # text += f'{tab}res = {res}{newl}'
                    print('aeo', res_tmp)
                    text += check_values(res_tmp)
                    print(text)
                    res = text
                elif ans == 'tuple':
                    pass
                elif ans == 'dict':
                    res = f"{' + '.join(res_tmp)}"
        elif len(u) == 1 and isinstance(u, tuple):
            if isinstance(u[0], int):
                r_tmp, t_tmp, a_tmp = recurser2(u[0], idx=idx + 1, ans=ans)
                res_tmp.append(r_tmp)
                if a_tmp == 'tuple':
                    text += f"{tab}res2 += ({t_tmp},){newl}"
                else:
                    print('io', t_tmp)
                    text += f"{tab}res = {t_tmp}{newl}"
                res = f"{' + '.join(res_tmp)}"
            elif isinstance(u[0], float):
                r_tmp, t_tmp, a_tmp = recurser2(u[0], idx=idx + 1, ans=ans)
                res_tmp.append(r_tmp)
                # print(res_tmp, t_tmp)
                text += check_values(res_tmp)
            elif isinstance(u[0], str):
                r_tmp, t_tmp, a_tmp = recurser2(u[0], idx=idx + 1, ans=ans)
                res_tmp.append(r_tmp)
                res = f"{' + '.join(res_tmp)}"
            else:
                r_tmp, t_tmp, a_tmp = recurser2(u[0], idx=idx + 1, ans=ans)
                res_tmp.append(r_tmp)
                text += f"{t_tmp}{tab}res2 = (res,){newl}"
                res = f"{' + '.join(res_tmp)}"
        else:
            if ans == 'dict':
                text = f'{tab}res = dict(){newl}'
            else:
                text = f'{tab}res = (){newl}'
            res = text
            return res, text, ans
    elif isinstance(u, int) or isinstance(u, float):
        if idx == 0:
            return f"{tab}res = p[{u}]{newl}", f"{tab}res = p[{u}]{newl}", ans
        return f"p[{u}]", f"p[{u}]", ans
    elif isinstance(u, str):
        return f'"{u}"', f'"{u}"', ans
    else:
        print('woololo')
        return u, u, ''
    return res, text, ans


def init_recur8(tp, idx=0):
    p = ''
    if tp == tuple:
        p = '()'
    elif tp == dict:
        p = 'dict()'
    elif tp in [str, int, float, None]:
        # p = '""'
        return ""
    return f"{tab}res{idx} = {p}{newl}"


def type8(value):
    if value is None:
        return None
    else:
        return type(value)


def istp8(value, tp):
    return isinstance(value, tp)


def priority8(value):
    listtype = any([istp8(i, list) for i in value])
    tupletype = any([istp8(i, tuple) for i in value])
    dicttype = any([istp8(i, dict) for i in value])
    strtype = any([istp8(i, str) for i in value])
    if dicttype:
        return dict
    elif tupletype:
        return tuple
    elif strtype:
        return str
    else:
        return None


def super_sum8(value, idx, tp0, tp1, tp2, enum):
    pre_text = ""
    additive_sign = '' if enum == 0 else '+'
    full_text = ""
    if tp2 == float:
        pre_text = f"{tab}if {value} is not None:{newl}{tab}"
    # elif tp2 == tuple:
    #    value = f"({value},)"
    else:
        if tp2 not in [int, dict, list, tuple, str]:
            return full_text

    if (tp0 == list or tp0 is None) and tp1 == dict:
        text = f"{idx}.update({value})"
    elif tp0 == dict:
        text = f"{idx}.update({value})"
    elif (tp0 == tuple and tp1 == dict) or tp1 == tuple or tp1 == list or tp1 == int or tp1 == str:
        text = f"{idx} {additive_sign}= {value}"
    full_text = f"{pre_text}{tab}res{text}{newl}"
    return full_text


def recur8(u, idx=0, ans=None):
    text = ''
    res = None
    if istp8(u, list):
        u_type = priority8(u)
    else:
        u_type = type8(u)
    text += init_recur8(u_type, idx)

    if istp8(u, tuple) or istp8(u, list):
        for i0, i in enumerate(u):
            ttmp, rtmp, atmp = recur8(i, idx + 1, type8(i))
            if atmp in [list, tuple]:  # , dict]:
                text += ttmp
                # if atmp == tuple or ans == tuple or type8(u) == tuple:
                if type8(u) == tuple or type(i) == tuple:
                    rtmp = f"({rtmp},)"
                if atmp != dict or u_type != dict:
                    text += f"{tab}res{idx} += {rtmp}{newl}"
                else:
                    text += f"{tab}res{idx}.update({rtmp}){newl}"
            elif atmp == dict:
                t_ = super_sum8(rtmp, idx, ans, type8(u), atmp, i0)
                text += t_
                if ans == dict:
                    text += f"{tab}res{idx}.update({rtmp}){newl}"
            else:
                if u_type == dict:
                    vtype = dict
                else:
                    vtype = type8(u)
                t_ = super_sum8(rtmp, idx, ans, vtype, atmp, i0)
                text += t_
        res = f"res{idx}"

    elif istp8(u, dict):
        for k, i in u.items():
            ttmp, rtmp, atmp = recur8(i, idx + 1, type8(i))
            text += ttmp
            if ans in [dict, None]:
                new_rtmp = f"[(\"{k}\", ({rtmp},))]"
                # print(new_rtmp, idx, ans, type8(u), atmp)
                text += super_sum8(new_rtmp, idx, ans, type8(u), atmp, None)
        res = f"res{idx}"
    elif istp8(u, str):
        res = f'"{u}"'
        if idx != 0:
            text = ''
        else:
            text = f"{tab}res0 = {res}{newl}"
        ans = type8(u)
    elif istp8(u, int):
        res = f"p[{u}]"
        if idx != 0:
            text = ''
        else:
            text = f"{tab}res0 = {res}{newl}"
        ans = type8(u)
    elif istp8(u, float):
        res = f"p[{int(u)}]"
        if idx != 0:
            text = ''
        else:
            text = f"{tab}res0 = {res}{newl}"
        ans = type8(u)
    else:
        print('woololo')

    if text == f'{tab}res0 = (){newl}':
        text = f'{tab}pass{newl}'
    return text, res, ans


def type9(value):
    if value is None:
        return None
    else:
        return type(value)


def istp9(value, tp):
    return isinstance(value, tp)


def priority9(value):
    types = [dict, tuple, str]
    for i in value:
        for y in types:
            if istp9(i, y):
                return y
    return None


def init9(tp):
    if tp == dict:
        return "dict()"
    elif tp == tuple:
        return "()"
    elif tp == str:
        return "\"\""


def inc9(value, tp):
    if tp == dict:
        return f".update({value})"
    else:
        return f" += {value}"


def recur9(u, idx=0):
    res = ''
    text = ''
    ans = type9(u)
    if not istp9(u, int) and not istp9(u, float) and not istp9(u, list):
        text = f"{tab}res{idx} = {init9(ans)}{newl}"
    if istp9(u, list):
        ktype = priority9(u)
        for i0, k in enumerate(u):
            ttmp, rtmp, atmp = recur9(k, idx + 1)
            text += ttmp
            value = rtmp
            res = f"res{idx}"
            if i0 == 0:
                text += f"{tab}{res} = {value}{newl}"
            else:
                text += f"{tab}{res}{inc9(value, ktype)}{newl}"
    elif istp9(u, tuple):
        if len(u) > 0:
            for k in u:
                ktype = type9(k)
                ttmp, rtmp, atmp = recur9(k, idx + 1)
                text += ttmp
                value = f"({rtmp},)"
                res = f"res{idx}"
                text += f"{tab}{res}{inc9(value, ans)}{newl}"
        else:
            text = f"{tab}pass{newl}"
    elif istp9(u, dict):
        for k, v in u.items():
            vtype = type9(v)
            ttmp, rtmp, atmp = recur9(v, idx + 1)
            text += ttmp
            value = f"[(\"{k}\", {rtmp})]"
            res = f"res{idx}"
            text += f"{tab}{res}{inc9(value, ans)}{newl}"
    elif istp9(u, str):
        res = f"\"{u}\""
        if idx == 0:
            text = f"{tab}res0 = {res}{newl}"
        else:
            text = ''
    elif istp9(u, int):
        res = f"p[{u}]"
        if idx == 0:
            text = f"{tab}res0 = {res}{newl}"
        else:
            text = ''
    elif istp9(u, float):
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
        print(i0, ';', i, '-->')
        try:
            print(json.dumps(g8.parse(i), indent=2))
        except Exception as e:
            print(f'*** Error: {e}')

