import gpp.gpp_lex as lex
import regex

#TODO:
# - loop block on actions


class ActionsInterp:
    def __init__(self):
        self.actions_dict = {'sets': self.action_sets2,
                             'maps': self.action_maps2,
                             'applies': self.action_applies2,
                             'uses': self.action_uses2,
                             'returns': self.action_returns2,
                             'inputs': self.action_inputs2,
                             'adds': self.action_adds2,
                             'multiplies': self.action_multiplies2,
                             'outputs': self.action_outputs2,
                             'loops': self.action_loops2
                             }
        self.count_mem1 = 0
        self.pointer1 = {}
        self.mem1 = {}
        self.code_info = {}

    ###########################
    ###########################
    # FUNCTION COMPLEMENTS
    ###########################
    ###########################

    # define hex, bin and null as reserved attribute-like strings
    @staticmethod
    def define_reserved(x):
        if isinstance(x, str) and len(x) > 2:
            if x[0:2] in ['0x', '0b']:
                return True
            elif x in lex.void:
                return True
        return False

    # check if object is attribute or not
    def check_obj(self, x):
        if isinstance(x, str):
            if '"' in x or self.define_reserved(x):
                return False
            return True
        elif isinstance(x, tuple):
            return self.check_obj(x[0])
        else:
            return False

    # get mem1 key value
    def recur_pointer(self, x):
        if 'mem' in self.pointer1[x].keys():
            return self.pointer1[x]['mem']
        else:
            if 'pointer' in self.pointer1[x].keys():
                if isinstance(self.pointer1[x]['pointer'], tuple):
                    for i in self.pointer1[x]['pointer']:
                        return self.recur_pointer(i)
                else:
                    return self.recur_pointer(self.pointer1[x]['pointer'])

    # get actual value in mem1
    def recur_value(self, x):
        if 'mem' in self.pointer1[x].keys():
            return self.mem1[self.pointer1[x]['mem']]['value']
        else:
            if 'pointer' in self.pointer1[x].keys():
                if isinstance(self.pointer1[x]['pointer'], tuple):
                    for i in self.pointer1[x]['pointer']:
                        return self.recur_value(i)
                else:
                    return self.recur_value(self.pointer1[x]['pointer'])

    # check data type
    @staticmethod
    def check_type(x):
        if isinstance(x, str):
            if len(x) > 2:
                if x[0:2] == '0x':
                    return 'hex'
                elif x[0:2] == '0b':
                    return 'bin'
                elif 'qubit' in x:
                    return 'qubin'
                else:
                    return 'str'
        elif isinstance(x, int):
            return 'int'
        elif isinstance(x, float):
            return 'float'
        elif isinstance(x, list):
            return 'list'
        elif isinstance(x, tuple):
            return 'tuple'
        else:
            return 'notype'

    # check each data type inside a list
    def obj_list_type(self, code_id, subj, obj):
        res = []
        for o in obj:
            if not self.check_obj(o):
                res.append(self.check_type(o))
            else:
                ref_o = '_'.join([code_id, 'attr', subj, o])
                res.append(self.check_type(self.recur_value(ref_o)))
        return res

    @staticmethod
    def isfloat(x):
        return all([[any([i.isnumeric(), i in ['.', 'e']]) for i in x], len(x.split('.')) == 2])

    def input_handler(self, x):
        new_x = x
        rfa = regex.findall(lex.t_str, x)
        for i in rfa:
            new_x = new_x.replace(i, '')
        new_x = new_x.split(' ')
        new_x = [i for i in new_x if len(i) > 0]
        new_x.extend(rfa)
        res = []
        for i in new_x:
            if i[0] == '"':
                res.append(('string', i))
            elif i[0:2] == '0b':
                res.append(('binary', i))
            elif i[0:2] == '0x':
                res.append(('hexadecimal', i))
            elif i.lower() in ['true', 'false']:
                res.append(('boolean', i.lower()))
            else:
                if self.isfloat(i):
                    res.append(('real', float(i)))
                else:
                    if i.isnumeric():
                        res.append(('real', int(i)))
                    else:
                        res.append(('string', i))
        return res

    ###########################
    ###########################
    # ACTIONS FUNCTIONS
    ###########################
    ###########################

    def action_sets2(self, code_id, prev_subj, subj, next_subj, obj, attr, pos_attr):
        if len(obj) == len(attr):
            for o, a in zip(obj, attr):
                ref_a = '_'.join([code_id, 'attr', subj, a])
                if self.check_obj(o):
                    ref_o = '_'.join([code_id, 'attr', subj, str(o)])
                    if ref_o in self.pointer1.keys():
                        self.pointer1.update({ref_a: {'pointer': ref_o}})
                else:
                    self.count_mem1 += 1
                    self.pointer1.update({ref_a: {'mem': self.count_mem1}})
                    self.mem1.update({self.count_mem1: {'value': o}})

    def action_maps2(self, code_id, prev_subj, subj, next_subj, obj, attr, pos_attr):
        ref_s = '_'.join([code_id, 'subj', subj])
        cinfo = self.code_info.get(ref_s, None)
        if cinfo:
            ext_attr = cinfo.get('external_attr', None)
            if ext_attr:
                if len(obj) == len(ext_attr):
                    for o, a in zip(obj, ext_attr):
                        ref_ea = '_'.join([code_id, 'attr', subj, a])
                        if self.check_obj(o):
                            ref_o = '_'.join([code_id, 'attr', prev_subj, o])
                            self.pointer1.update({ref_ea: {'pointer': ref_o}})
                        else:
                            self.count_mem1 += 1
                            self.pointer1.update({ref_ea: {'mem': self.count_mem1}})
                            self.mem1.update({self.count_mem1: {'value': o}})

    def action_applies2(self, code_id, prev_subj, subj, next_subj, obj, attr, pos_attr):
        if next_subj is not None:
            num_objs = [obj[o1 + 1][0]['subject'][0] for o1, o in enumerate(obj) if o == 'with']
            if len(num_objs) == len(attr):
                for a, n in zip(attr, num_objs):
                    ref_r = '_'.join([code_id, 'attr', n, 'return'])
                    ref_a = '_'.join([code_id, 'attr', subj, a])
                    self.count_mem1 += 1
                    self.pointer1.update({ref_a: {'mem': self.count_mem1}})
                    self.mem1.update({self.count_mem1: {'value': {}}})
                    self.pointer1.update({ref_r: {'pointer': ref_a}})
            else:
                p_ref_list = tuple()
                for n in num_objs:
                    ref_r = '_'.join([code_id, 'attr', n, 'return'])
                    ref_a = '_'.join([code_id, 'attr', subj, attr[0]])
                    self.count_mem1 += 1
                    self.pointer1.update({ref_a: {'mem': self.count_mem1}})
                    self.mem1.update({self.count_mem1: {'value': {}}})
                    p_ref_list += (ref_a,)
                self.pointer1.update({ref_r: {'pointer': p_ref_list}})

    def action_returns2(self, code_id, prev_subj, subj, next_subj, obj, attr, pos_attr):
        self.action_uses2(code_id, prev_subj, subj, next_subj, obj, attr, pos_attr)

    def action_uses2(self, code_id, prev_subj, subj, next_subj, obj, attr, pos_attr):
        ref_a = '_'.join([code_id, 'attr', subj, 'return'])
        ref_p = self.pointer1.get(ref_a, None)
        if ref_p:
            ref_pointer = ref_p['pointer']
            if isinstance(ref_pointer, tuple) and isinstance(obj, tuple):
                if len(obj) == len(ref_pointer):
                    for o, p in zip(obj, ref_pointer):
                        if self.check_obj(o):
                            o_f = '_'.join([code_id, 'attr', subj, o])
                            m_f = self.recur_value(o_f)
                        else:
                            m_f = o
                        self.mem1[self.pointer1[p]['mem']].update({'value': m_f})
                else:
                    if self.check_obj(obj):
                        o_f = '_'.join([code_id, 'attr', subj, obj])
                        m_f = self.recur_value(o_f)
                    else:
                        m_f = obj
                    self.mem1[self.recur_pointer(ref_pointer)].update({'value': m_f})
            else:
                if self.check_obj(obj):
                    o_r = str(obj[0]) if isinstance(obj, tuple) else str(obj)
                    o_f = '_'.join([code_id, 'attr', subj, o_r])
                    m_f = self.recur_value(o_f)
                else:
                    m_f = obj
                self.mem1[self.recur_pointer(ref_pointer)].update({'value': m_f})

    def action_adds2(self, code_id, prev_subj, subj, next_subj, obj, attr, pos_attr):
        ref_a = '_'.join([code_id, 'attr', subj, attr[0]])
        obj_types = self.obj_list_type(code_id, subj, obj)
        if 'tuple' in obj_types or 'list' in obj_types:
            res = []
            for o in obj:
                if self.check_obj(o):
                    ref_o = '_'.join([code_id, 'attr', subj, o])
                    res.append(self.recur_value(ref_o))
                else:
                    res.append(o)
        elif 'str' in obj_types:
            res = ''
            for o in obj:
                if self.check_obj(o):
                    ref_o = '_'.join([code_id, 'attr', subj, o])
                    res += str(self.recur_value(ref_o)).strip('"')
                else:
                    res += str(o).strip('"')
            res = '"' + res + '"'
        elif 'hex' in obj_types and 'float' not in obj_types:
            res = 0
            for o in obj:
                if self.check_obj(o):
                    ref_o = '_'.join([code_id, 'attr', subj, o])
                    new_o = self.recur_value(ref_o)
                    if isinstance(new_o, str):
                        res += int(new_o, 16)
                    else:
                        res += new_o
                else:
                    if isinstance(o, str):
                        res += int(o, 16)
                    else:
                        res += o
            res = hex(res)
        elif 'bin' in obj_types and 'float' not in obj_types:
            res = 0
            for o in obj:
                if self.check_obj(o):
                    ref_o = '_'.join([code_id, 'attr', subj, o])
                    new_o = self.recur_value(ref_o)
                    if isinstance(new_o, str):
                        res += int(new_o, 2)
                    else:
                        res += new_o
                else:
                    if isinstance(o, str):
                        res += int(o, 16)
                    else:
                        res += o
            res = bin(res)
        elif 'int' in obj_types or 'float' in obj_types:
            res = 0
            for o in obj:
                if self.check_obj(o):
                    ref_o = '_'.join([code_id, 'attr', subj, o])
                    new_o = self.recur_value(ref_o)
                    res += new_o
                else:
                    res += o
        else:
            res = []
            for o in obj:
                if self.check_obj(o):
                    ref_o = '_'.join([code_id, 'attr', subj, o])
                    res.append(self.recur_value(ref_o))
                else:
                    res.append(o)

        self.count_mem1 += 1
        self.pointer1.update({ref_a: {'mem': self.count_mem1}})
        self.mem1.update({self.count_mem1: {'value': res}})

    def action_multiplies2(self, code_id, prev_subj, subj, next_subj, obj, attr, pos_attr):
        obj_types = self.obj_list_type(code_id, subj, obj)
        if all([i == 'int' or i == 'float' for i in obj_types]):
            mult = 1
            for o in obj:
                if self.check_obj(o):
                    ref_o = '_'.join([code_id, 'attr', subj, o])
                    mult *= self.recur_value(ref_o)
                else:
                    mult *= o
            self.count_mem1 += 1
            ref_a = '_'.join([code_id, 'attr', subj, attr[0]])
            self.pointer1.update({ref_a: {'mem': self.count_mem1}})
            self.mem1.update({self.count_mem1: {'value': mult}})

    def action_outputs2(self, code_id, prev_subj, subj, next_subj, obj, attr, pos_attr):
        res = []
        for o in obj:
            if self.check_obj(o):
                ref_o = '_'.join([code_id, 'attr', subj, o])
                res.append(str(self.recur_value(ref_o)))
            else:
                res.append(o)
        print(' '.join(res))

    def action_inputs2(self, code_id, prev_subj, subj, next_subj, obj, attr, pos_attr):
        answer = input()
        w_list = self.input_handler(answer)
        if len(w_list) == len(obj) and len(obj) == len(attr):
            for o, w, a in zip(obj, w_list, attr):
                if w[0] == o:
                    ref_a = '_'.join([code_id, 'attr', subj, a])
                    self.count_mem1 += 1
                    self.pointer1.update({ref_a: {'mem': self.count_mem1}})
                    self.mem1.update({self.count_mem1: {'value': w[1]}})
        else:
            if len(attr) == 1 and len(obj) == 1:
                ref_a = '_'.join([code_id, 'attr', subj, attr])
                self.count_mem1 += 1
                self.pointer1.update({ref_a: {'mem': self.count_mem1}})
                self.mem1.update({self.count_mem1: {'value': answer}})

    def action_loops2(self, code_id, prev_subj, subj, next_subj, obj, attr, pos_attr):
        pass

    ###########################
    ###########################
    # LOOP FUNCTIONS
    ###########################
    ###########################

    def check_loop_expr(self, code_id, subj, x):
        val_p = ''
        if isinstance(x[-1], tuple):
            if self.check_obj(x[-1][0]):
                ref_v = '_'.join([code_id, 'attr', subj, x[-1][0]])
                val_f = self.recur_value(ref_v)
            else:
                val_f = x[-1][0]
            if x[-1][1] == '%':
                val_p = 'mod'
        else:
            if self.check_obj(x[-1]):
                ref_v = '_'.join([code_id, 'attr', subj, x[-1]])
                val_f = self.recur_value(ref_v)
            else:
                val_f = x[-1]
        if self.check_obj(x[1]):
            ref_v = '_'.join([code_id, 'attr', subj, x[1]])
            val_i = self.recur_value(ref_v)
        else:
            val_i = x[1]
        return val_i, val_f, val_p

    def define_obj_loop(self, code_id, subj, obj_to_loop=None, obj_loop=None):
        if obj_to_loop is not None and obj_loop is not None:
            oloop = self.check_loop_expr(code_id, subj, obj_loop)
            if isinstance(obj_to_loop, tuple):
                var = ''
                ref = ''
                _v = ()
                res = []
                for o in obj_to_loop:
                    if isinstance(o, str):
                        res.append(o)
                    elif isinstance(o, dict):
                        if 'ref' in o.keys():
                            ref = o['ref'][0]
                            _v += (ref,)
                        if 'var_loop' in o.keys():
                            var = o['var_loop'][0]
                            _v += (var,)
                new_res = []
                for ol in range(oloop[0], oloop[1] + 1, oloop[2] or 1):
                    if len(_v) == 2:
                        new_res.append(_v[0] + str(ol))
                    else:
                        new_res.append(ol)
                new_res.extend(res)
                return new_res
        return []

    ###########################
    ###########################
    # INTERPRETER METHODS
    ###########################
    ###########################

    # code details extract from the parser
    def parse_details(self, code_id, x, main_subj=None, cur_subj=None, act=None, obj=None,
                      attr=None,
                      inside=False):
        for i0, i in enumerate(x):
            if isinstance(i, tuple):
                self.parse_details(code_id, i, main_subj, cur_subj, act, obj, attr, True)
            if isinstance(i, dict):
                if i.get('subject', None):
                    if not inside:
                        if i0 != 0:
                            t = 'aux'
                            cur_subj = i['subject'][0]
                            s_s = '_'.join([code_id, 'subj', str(cur_subj)])
                            self.code_info.update({s_s: {'pos': i0, 'type': t}})
                        else:
                            t = 'main'
                            main_subj = i['subject'][0]
                            s_m = '_'.join([code_id, 'subj', str(main_subj)])
                            cur_subj = i['subject'][0]
                            s_s = '_'.join([code_id, 'subj', str(cur_subj)])
                            self.code_info.update({s_m: {'pos': i0, 'type': t}})
                    else:
                        t = 'aux'
                        cur_subj = i['subject'][0]
                        s_s = '_'.join([code_id, 'subj', str(cur_subj)])
                        self.code_info.update({s_s: {'pos': i0, 'type': t}})
                elif i.get('action', None):
                    s_s = '_'.join([code_id, 'subj', str(cur_subj)])
                    s_m = '_'.join([code_id, 'subj', str(main_subj)])
                    act = i['action'][0]
                    obj = i['object']
                    if len(obj) > 1 and obj[0] in ['with', 'if']:
                        self.parse_details(code_id, obj, main_subj, cur_subj, act, None, None, True)
                    attr = i.get('attr', None)
                    s_cval = self.code_info.get(s_s, None)
                    s_mval = self.code_info.get(s_m, None)
                    if s_cval or s_mval:
                        for o in obj:
                            if isinstance(o, str):
                                if act == 'sets':
                                    if o[0] == '*':
                                        s_cval.update({'external_attr': i.get('object',
                                                                              None), 'assign_attr': i.get(
                                            'attr', None)})

    # executing the parse "the interpreter" function
    def execute_parse(self, code_id,
                      x,
                      full_x,
                      prev_subj=None,
                      subj=None,
                      next_subj=None,
                      act=None,
                      attr=None,
                      obj=None,
                      pos_attr=None,
                      var_loop=None,
                      loop_vals=None,
                      inside_loop=False,
                      deep=0,
                      aux=False):
        for i0, i in enumerate(x):
            if isinstance(i, tuple):
                r = self.execute_parse(code_id, i, full_x, prev_subj, subj, next_subj, act, attr,
                                       obj,
                                       pos_attr, var_loop, loop_vals, inside_loop,
                                       deep + 1, aux)
            elif isinstance(i, dict):
                if 'subject' in i.keys():
                    prev_subj = subj
                    subj = i['subject'][0]
                elif 'action' in i.keys():
                    act = i['action'][0]
                    attr = i.get('attr', (None,))
                    obj = i['object']
                    if act != 'loops':
                        if 'obj_loop' in i.keys():
                            obj = self.define_obj_loop(code_id, subj, obj, i['obj_loop'])
                        if 'attr_loop' in i.keys():
                            attr = self.define_obj_loop(code_id, subj, attr, i['attr_loop'])
                    else:
                        var_loop = obj[1]['subject'][0]['var_loop'][0]
                        loop_vals = i['obj_loop']
                        inside_loop = True
                    if len(obj) > 0:
                        if obj[0] in ['with', 'if']:
                            if act in self.actions_dict.keys():
                                next_subj = obj[1][0]["subject"][0]
                                self.actions_dict[act](code_id, prev_subj, subj, next_subj, obj,
                                                       attr, pos_attr)
                            aux = True
                            obj_subj = [o1 + 1 for o1, o in enumerate(obj) if o in ['with', 'if']]
                            if len(obj_subj) == len(attr):
                                # print('len obj_subj == len attr')
                                pass
                            for idx, sa in enumerate(zip(obj_subj, attr)):
                                next_subj = obj[sa[0]][0]["subject"][0]
                                r = self.execute_parse(code_id, obj[sa[0]], full_x, prev_subj, subj,
                                                       next_subj,
                                                       act,
                                                       sa[1], obj, idx, var_loop, loop_vals,
                                                       inside_loop, deep + 1, aux)
                            aux = False
                            idx = None
                        else:
                            if act in self.actions_dict.keys():
                                self.actions_dict[act](code_id, prev_subj, subj, next_subj, obj,
                                                       attr, pos_attr)
                        if next_subj is not None and aux:
                            sb = '_'.join([code_id, 'subj', next_subj])
                            if self.code_info[sb]['type'] != 'main':
                                aux = False
                                r = self.execute_parse(code_id,
                                                       full_x[self.code_info[sb]['pos'] + 1],
                                                       full_x,
                                                       prev_subj,
                                                       subj,
                                                       None, None, None, None, pos_attr, var_loop,
                                                       loop_vals, inside_loop, deep + 1,
                                                       aux=True)
                    inside_loop = False
                    var_loop = None
                    loop_vals = None
            if i == 'where':
                break
        return 0
