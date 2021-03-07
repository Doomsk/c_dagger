import gpp.yacc as yacc
from gpp.gpp_lex import tokens, actions


check_action = None


def nonull(*x):
    r_ = tuple([i for i in x if i is not None])
    if r_:
        return r_
    else:
        return


def p_sentence(p):
    """sentence : subject
                | subject sup_sentence
                """
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1] + p[2]


def p_sup_sentence(p):
    """sup_sentence : where subject
                    | where subject sup_sentence
                    | """
    if len(p) == 3:
        p[0] = (p[1],) + p[2]
    elif len(p) == 4:
        p[0] = (p[1],) + p[2] + p[3]


def p_subject(p):
    """subject : superid3 ':' action
                | superid3 ':' action sup_sentence
                """
    if len(p) == 5:
        if p[4] is not None:
            p[0] = nonull({'subject': p[1]}) + nonull(p[3]) + p[4]
        else:
            p[0] = nonull({'subject': p[1]}) + nonull(p[3])
    elif len(p) == 4:
        p[0] = nonull({'subject': p[1]}) + nonull(p[3])


def p_action0(p):
    """action : actionlabels lbracket superobject rbracket
                | actionlabels lbracket superobject rbracket action
                """
    if len(p[3]) == 1:
        p[3] = tuple(p[3])
    if len(p) == 5:
        p[0] = nonull({'action': p[1], 'object': p[3]})
    elif len(p) == 6:
        p[0] = nonull({'action': p[1], 'object': p[3]}) + p[5]


def p_action1(p):
    """action : extendaction lbracket superobject rbracket
                | extendaction lbracket superobject rbracket action
                | extendaction lbracket superobject rbracket loop1
                | extendaction lbracket superobject rbracket as attr
                | extendaction lbracket superobject rbracket as attr action
                | extendaction lbracket superobject rbracket loop1 as attr
                | extendaction lbracket superobject rbracket loop1 as attr action
                | extendaction lbracket superobject rbracket loop1 as attr loop1
                | extendaction lbracket superobject rbracket loop1 as attr loop1 action"""
    if len(p[3]) == 1:
        p[3] = tuple(p[3])
    if len(p) == 5:
        p[0] = nonull({'action': p[1], 'object': p[3]})
    elif len(p) == 6:
        if isinstance(p[5], tuple):
            if len(p[5]) > 1:
                if len(p[5][1]) == 4 and isinstance(p[5][1], tuple):
                    if p[5][1][0] == '_':
                        p[0] = nonull({'action': p[1], 'object': p[3], 'obj_loop': p[5][1]})
                else:
                    p[0] = ({'action': p[1], 'object': p[3]},) + p[5]
            else:
                p[0] = ({'action': p[1], 'object': p[3]},) + p[5]
        else:
            p[0] = nonull({'action': p[1], 'object': p[3]}) + p[5]
    elif len(p) == 7:
        if p[5] == 'as':
            if not isinstance(p[6], tuple):
                p[6] = (p[6],)
            p[0] = nonull({'action': p[1], 'object': p[3], 'attr': p[6]})
    elif len(p) == 8:
        if p[5] == 'as':
            if not isinstance(p[6], tuple):
                p[6] = (p[6],)
                p[0] = nonull({'action': p[1], 'object': p[3], 'attr': p[6]}) + p[7]
            else:
                if len(p[6]) == 2:
                    if isinstance(p[6][1], dict):
                        if 'attr_loop' in p[6][1].keys():
                            x_ = {'action': p[1], 'object': p[3], 'attr': (p[6][0],)}
                            x_.update(p[6][1])
                            p[0] = (x_,) + p[7]
                        else:
                            p[0] = nonull({'action': p[1], 'object': p[3], 'attr': p[6]}) + p[7]
                    else:
                        p[0] = nonull({'action': p[1], 'object': p[3], 'attr': p[6]}) + p[7]
                else:
                    p[0] = nonull({'action': p[1], 'object': p[3], 'attr': p[6]}) + p[7]
        else:
            p[0] = nonull({'action': p[1], 'object': p[3], 'obj_loop': p[5][1], 'attr': (p[7],)})
    elif len(p) == 9:
        if isinstance(p[5], tuple) and len(p[5][1]) == 4 and p[5][1][0] == '_':
            if not isinstance(p[7], tuple):
                p[7] = (p[7],)
                p[0] = nonull(
                        {'action': p[1], 'object': p[3], 'obj_loop': p[5][1], 'attr': p[7]}) + p[8]
            else:
                if len(p[7]) == 2:
                    if isinstance(p[7][1], dict):
                        if 'attr_loop' in p[7][1].keys():
                            x_ = {'action': p[1], 'object': p[3], 'obj_loop': p[5][1], 'attr': (
                            p[7][0],)}
                            x_.update(p[7][1])
                            p[0] = (x_,) + p[8]
                        else:
                            p[0] = nonull(
                                {'action': p[1], 'object': p[3], 'obj_loop': p[5][1], 'attr': p[
                                    7]}) + p[8]
                    else:
                        p[0] = nonull(
                            {'action': p[1], 'object': p[3], 'obj_loop': p[5][1], 'attr': p[7]}) + \
                               p[8]
                else:
                    p[0] = nonull(
                        {'action': p[1], 'object': p[3], 'obj_loop': p[5][1], 'attr': p[7]}) + p[8]
        else:
            if isinstance(p[8], tuple) and len(p[8]) == 4:
                if isinstance(p[8][1], tuple) and p[8][1][0] == '_':
                    p[0] = nonull({'action': p[1], 'object': p[3], 'obj_loop': p[5], 'attr': (p[7],), 'attr_loop': p[8][1]})
                else:
                    p[0] = nonull({'action': p[1], 'object': p[3], 'obj_loop': p[5], 'attr': (
                    p[7],), 'attr_loop': p[8]})
            else:
                p[0] = nonull(
                    {'action': p[1], 'object': p[3], 'obj_loop': p[5], 'attr': (p[7],)}) + p[8]
    elif len(p) == 10:
        p[0] = nonull({'action': p[1], 'object': p[3], 'obj_loop': p[5][1], 'attr': (p[7],), 'attr_loop': p[8][1]}) + p[9]


def p_action2(p):
    """action : defines lbracket string rbracket as attr
                | defines lbracket string rbracket as attr action"""
    if len(p) == 7:
        if not isinstance(p[6], tuple):
            p[6] = (p[6],)
        p[0] = nonull({'action': p[1], 'object': (p[3],), 'attr': (p[6],)})
    elif len(p) == 11:
        if not isinstance(p[8], tuple):
            p[6] = (p[8],)
        p[0] = nonull({'action': p[1], 'object': (p[3],), 'attr': (p[8],)}) + p[10]


def p_extended_actions(p):
    """extendaction : actlabels1
                    | actlabels1 and extendaction"""
    if len(p) == 2:
        p[0] = (p[1],)
    elif len(p) == 4:
        p[0] = (p[1], p[2],) + p[3]


def p_action1_labels(p):
    """actlabels1 : applies
                    | maps
                    | sets
                    | divides
                    | powers
                    | adds
                    | multiplies
                    | roots
                    | keeps
                    | processes
                    | threads
                    | dequeues
                    | publishes
                    | checks
                    | uses
                    | reads
                    | loads
                    | names
                    | inputs
                    | invokes
                    | queues
                    | consumes
                    | produces
                    | compares
                    | loops
                    | parallels"""
    p[0] = p[1]


def p_action_names(p):
    """actionlabels : outputs
                    | brings
                    | starts
                    | calls
                    | waits
                    | repeats
                    | executes
                    | evaluates
                    | computes
                    | returns
                    | translates"""
    p[0] = p[1]


def p_superobject(p):
    """superobject : object
                    | object and superobject
                    | compl
                    | statements"""
    global check_action
    if p[-2] in actions:
        check_action = p[-2]
    elif check_action is not None:
        pass
    else:
        check_action = None

    if len(p) == 2:
        if isinstance(p[1], tuple):
            p[0] = p[1]
        else:
            p[0] = (p[1],)
    elif len(p) == 3:
        p[0] = (p[1], p[2])
    elif len(p) == 4:
        if p[2] == '&':
            p[2] = (p[2],)
        if not isinstance(p[3], tuple):
            p[3] = (p[3],)
        if not isinstance(p[1], tuple):
            p[1] = (p[1],)
        p[0] = p[1] + p[2] + p[3]
    elif len(p) == 5:
        p[0] = (nonull(p[1], p[2]), p[3]) + (p[4],)


def p_object(p):
    """object : superid
                | subject
                | superid object
                | num
                | num object
                | bool1
                | bool1 object
                | string
                | string object
                | superid loop1
                | bool1 loop1
                | binary
                | binary object
                | hexadecimal
                | hexadecimal object"""
    if len(p) == 2:
        if isinstance(p[1], tuple) and len(p[1]) > 1:
            # p[0] = (p[1],)
            p[0] = p[1]
        else:
            if not isinstance(p[1], tuple):
                p[1] = (p[1],)
            p[0] = p[1]
    elif len(p) == 3:
        if not isinstance(p[1], tuple):
            p[1] = (p[1],)
        if not isinstance(p[2], tuple):
            p[2] = (p[2],)
        if isinstance(p[2], tuple):
            if p[2][0] == 'loop':
                p[2] = {'obj_loop': p[2][1]}
                p[1][0].update(p[2])
                p[0] = (p[1],)
            else:
                if len(p[1]) > 1:
                    if isinstance(p[1], dict):
                        if 'ref' in p[1].keys():
                            if isinstance(p[2], str):
                                if p[2][0] == '"':
                                    p[0] = (p[1].update({'after_loop': p[2]}))
                                else:
                                    p[0] = (p[1],) + p[2]
                            else:
                                p[0] = (p[1],) + p[2]
                        else:
                            p[0] = (p[1],) + p[2]
                    else:
                        p[0] = (p[1],) + p[2]
                else:
                    if isinstance(p[2][0], str):
                        if p[2][0][0] == '"':
                            if isinstance(p[1][0], dict):
                                p[1][0].update({'after_loop': p[2]})
                                p[2] = ()
                    if isinstance(p[1][0], str):
                        if p[1][0][0] == '"':
                            if isinstance(p[2][0], dict):
                                p[2][0].update({'ref': p[1]})
                                p[1] = ()
                    p[0] = p[1] + p[2]
        else:
            if len(p[1]) > 1:
                p[0] = ((p[1],), p[2])
            else:
                p[0] = p[1] + p[2]


def p_comp(p):
    """compl : with object
            | with object and superobject
            | if subject
            | if subject else action"""
    global check_action
    if p[-2] in actions:
        check_action = p[-2]
    else:
        check_action = None

    if len(p) == 3:
        p[0] = (p[1], p[2])
    elif len(p) == 5:
        if p[1] == 'if':
            p[0] = nonull(p[1], p[2], p[3], p[4],)
        elif p[1] == 'with':
            p[0] = nonull(p[1], p[2], p[3],) + p[4]


def p_statements(p):
    """statements : lparen expression2 rparen loop2
                | lparen expression2 rparen loop2 logelem statements
                | lparen statements rparen loop2
                | lparen statements rparen loop2 logelem statements
                """
    if len(p) == 4:
        if p[2][0] != '(':
            p[0] = (p[2],)
        else:
            p[0] = p[2]
    elif len(p) == 5:
        if isinstance(p[4], tuple):
            if p[4][0] == 'loop':
                p[0] = (p[2] + ({'obj_loop': p[4][1]},),)
            else:
                p[0] = (p[2],)
        else:
            if p[2][0] != '(':
                p[0] = (p[2],)
            else:
                p[0] = (p[2],)
    elif len(p) == 6:
        if isinstance(p[5], tuple):
            if p[5][0] == 'loop':
                p[0] = (p[2] + ({'oper': p[3], 'obj_loop': p[5][1]},),)
            else:
                p[0] = (p[2],) + (p[4],) + p[5]
        else:
            p[0] = (p[2],) + (p[4],) + p[5]
    elif len(p) == 7:
        if not isinstance(p[5], tuple):
            p[5] = (p[5],)
        if p[4] is not None:
            if len(p[2]) == 3 and not isinstance(p[2], dict):
                if isinstance(p[2][0], dict) and isinstance(p[2][2], dict):
                    p[0] = (p[2] + ({'obj_loop': p[4][1]},),) + p[5] + p[6]
                elif isinstance(p[2][0], dict) and not isinstance(p[2][2], dict):
                    p[2][0].update({'obj_loop': p[4][1]})
                    p[0] = ((p[2],),) + p[5] + p[6]
                elif not isinstance(p[2][0], dict) and isinstance(p[2][2], dict):
                    p[2][2].update({'obj_loop': p[4][1]})
                    p[0] = ((p[2],),) + p[5] + p[6]
                else:
                    p[0] = (p[2] + ({'obj_loop': p[4][1]},),) + p[5] + p[6]
            elif len(p[2][0]) == 3 and not isinstance(p[2][0], dict):
                if isinstance(p[2][0][0], dict) and isinstance(p[2][0][2], dict):
                    p[0] = (p[2], {'obj_loop': p[4][1]},) + p[5] + p[6]
                elif isinstance(p[2][0][0], dict) and not isinstance(p[2][0][2], dict):
                    p[2][0][0].update({'obj_loop': p[4][1]})
                    p[0] = ((p[2],),) + p[5] + p[6]
                elif not isinstance(p[2][0][0], dict) and isinstance(p[2][0][2], dict):
                    p[2][0][2].update({'obj_loop': p[4][1]})
                    p[0] = ((p[2],),) + p[5] + p[6]
                else:
                    p[0] = (p[2] + ({'obj_loop': p[4][1]},),) + p[5] + p[6]
            else:
                p[0] = (p[2] + ({'obj_loop': p[4][1]},),) + p[5] + p[6]
        else:
            p[0] = (p[2],) + p[5] + p[6]
    elif len(p) == 8:
        if p[5][0] == 'loop':
            p[0] = (p[2] + ({'oper': p[3], 'obj_loop': p[5][1]},),) + (p[6],) + p[7]
        else:
            if isinstance(p[2], dict) and not isinstance(p[4], dict):
                p[2][0].update({'oper': p[5], 'obj_loop': p[7][1]})
                p[0] = p[2] + (p[3], p[4])
            elif isinstance(p[4], dict) and not isinstance(p[2], dict):
                p[4][0].update({'oper': p[5], 'obj_loop': p[7][1]})
                p[0] = (p[2], p[3],) + p[4]
            else:
                p[0] = p[2] + (p[3],) + p[4] + ({'oper': p[5], 'obj_loop': p[7][1]},)
    elif len(p) == 10:
        if isinstance(p[2], dict) and not isinstance(p[4], dict):
            p[2][0].update({'oper': p[5], 'obj_loop': p[7][1]})
            p[0] = p[2] + (p[3], p[4]) + (p[8],) + p[9]
        elif isinstance(p[4], dict) and not isinstance(p[2], dict):
            p[4][0].update({'oper': p[5], 'obj_loop': p[7][1]})
            p[0] = (p[2], p[3],) + p[4] + (p[8],) + p[9]
        else:
            p[0] = p[2] + (p[3],) + p[4] + ({'oper': p[5], 'obj_loop': p[7][1]},) + (p[8],) + p[9]


def p_expression2(p):
    """expression2 : superid3 symbols1 superid4 logtmp
                    | superid4 logtmp"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        if p[2] is not None:
            p[1][0].update({'oper': p[2]})
            p[0] = p[1]
        else:
            if isinstance(p[1][0], dict):
                p[1] = p[1][0]
            p[0] = p[1]
    elif len(p) == 4:
        if isinstance(p[1], tuple):
            p[0] = p[1] + (p[2],) + p[3]
        else:
            p[0] = (p[1], p[2], p[3],)
    elif len(p) == 5:
        if p[4] is not None:
            p[0] = (p[1], p[2], p[3], {'oper': p[4]},)
        else:
            p[0] = p[1] + (p[2],) + p[3]


def p_symbols1(p):
    """symbols1 : equal
                | notequal
                | gt
                | gte
                | lt
                | lte"""
    p[0] = p[1]


def p_logtmp(p):
    """logtmp : logelem
                |"""
    if len(p) == 2:
        p[0] = p[1]


def p_logelem(p):
    """logelem : and
                | or"""
    p[0] = p[1]


def p_attr(p):
    """attr : id
            | superid loop1
            | id attr"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        if p[2][0] == 'loop':
            p[0] = p[1] + ({'attr_loop': p[2][1]},)
        else:
            if not isinstance(p[2], tuple):
                p[2] = (p[2],)
            p[0] = (p[1],) + p[2]


def p_loop1(p):
    """loop1 : underscore real dots lastloopterm
             | underscore id dots lastloopterm"""
    p[0] = ('loop', nonull(p[1], p[2], p[3], p[4]))


def p_loop2(p):
    """loop2 : underscore real dots lastloopterm
             | underscore id dots lastloopterm
             |"""
    if len(p) == 5:
        p[0] = ('loop', nonull(p[1], p[2], p[3], p[4]))


def p_loopterm1(p):
    """lastloopterm : real
                    | id
                    | real mod lastloopterm
                    | id mod lastloopterm"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = (p[1], p[2], p[3])


def p_superid(p):
    """superid : id
                | string
                | num
                | id period superid
                | id dollar superid
                | dollar superid"""
    if len(p) == 2:
        p[0] = (p[1],)
    elif len(p) == 3:
        if p[1] == '$':
            p[0] = ({'var_loop': p[2]},)
        else:
            p[0] = (p[1], p[2])
    elif len(p) == 4:
        if p[2] == '.':
            p[0] = (p[1], p[2]) + p[3]
        else:
            if not isinstance(p[1], tuple):
                p[1] = (p[1],)
            p[0] = ({'ref': p[1], 'var_loop': p[3]},)


def p_superid4(p):
    """superid4 : superid3
                | nulls"""
    p[0] = p[1]


def p_superid3(p):
    """superid3 : id
                | num
                | binary
                | hexadecimal
                | string
                | id period superid3
                | id dollar superid3
                | dollar superid3"""
    if len(p) == 2:
        p[0] = (p[1],)
    elif len(p) == 3:
        if p[1] == '$':
            p[0] = ({'var_loop': p[2]},)
        else:
            p[0] = (p[1], p[2])
    elif len(p) == 4:
        if p[2] == '.':
            p[0] = (p[1], p[2]) + p[3]
        else:
            p[0] = ({'ref': p[1], 'var_loop': p[3]},)


def p_bool1(p):
    """bool1 : bool"""
    p[0] = p[1]


def p_nums_real(p):
    """num : real"""
    p[0] = p[1]


def p_null1(p):
    """nulls : null
            | none
            | void"""
    p[0] = p[1]


##################
# YACC PARSER
##################
parser = yacc.yacc()


def parse(data, debug=0):
    parser.error = 0
    p = parser.parse(data, debug=debug)
    if parser.error:
        return None
    return p


###################
# EXTRA FUNCTIONS
###################
def read(x=1):
    with open(f'gpp/test{x}.c†', 'r') as f:
        p = f.read()
    return p


def test(x=1):
    p = read(x)
    return parse(p)


##############
# MAIN
##############
if __name__ == '__main__':
    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        if not s:
            continue
        if s == 'exit':
            break
        result = parser.parse(s)
        print(result)
