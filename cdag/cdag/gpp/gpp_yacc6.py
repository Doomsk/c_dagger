# currently used
import cdag.gpp.yacc as yacc
from cdag.gpp.gpp_lex import tokens, actions


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
        print('sentence (2)', p[1])
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1] + p[2]
        print('sentence (3)', p[0])
    else:
        print('sentence passou')


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
        print('subject (5)', p[0])
    elif len(p) == 4:
        p[0] = nonull({'subject': p[1]}) + nonull(p[3])
        print('subject (4)', p[0])
    else:
        print('subject passou')


def p_action0(p):
    """action : actionlabels lbracket superobject rbracket
                | actionlabels lbracket superobject rbracket action
                """
    if len(p[3]) == 1:
        p[3] = tuple(p[3])

    if len(p) == 5:
        p[0] = nonull({'action': (p[1],), 'object': p[3]})
        print('action0 (5)', p[0])
    elif len(p) == 6:
        p[0] = nonull({'action': (p[1],), 'object': p[3]}) + p[5]
        print('action0 (6)', p[0])
    else:
        print('action0 passou')


def p_action1(p):
    """action : extendaction lbracket superobject rbracket
                | extendaction lbracket superobject rbracket action
                | extendaction lbracket superobject rbracket loop1
                | extendaction lbracket superobject rbracket loop1 action
                | extendaction lbracket superobject rbracket as attrX
                | extendaction lbracket superobject rbracket as attrX action
                | extendaction lbracket superobject rbracket loop1 as attrX
                | extendaction lbracket superobject rbracket loop1 as attrX action
                | extendaction lbracket superobject rbracket loop1 as attrX loop1
                | extendaction lbracket superobject rbracket loop1 as attrX loop1 action"""
    if len(p[3]) == 1:
        p[3] = tuple(p[3])
    print('action?')
    if len(p) == 5:
        p[0] = nonull({'action': p[1], 'object': p[3]})
        print('action1 (5)', p[0])
    elif len(p) == 6:
        print('---(6) here?')
        if isinstance(p[5], tuple):
            if len(p[5]) > 1:
                if len(p[5][1]) == 4 and isinstance(p[5][1], tuple):
                    if p[5][1][0] == '_':
                        p[0] = nonull({'action': p[1], 'object': p[3], 'obj_loop': p[5][1]})
                    else:
                        print('no _ on 5-1-0')
                else:
                    print('no tuple 5-1', p[5])
                    p[0] = ({'action': p[1], 'object': p[3]},) + p[5]
            else:
                print('len p[5] == 1', p[5])
                print(p[1], p[3], p[5])
                p[0] = ({'action': p[1], 'object': p[3]},) + p[5]
        else:
            p[0] = nonull({'action': p[1], 'object': p[3]}) + p[5]
        print('action1 (6)', p[0])
    elif len(p) == 7:
        print('---(7) here?')
        if p[5] == 'as':
            if not isinstance(p[6], tuple):
                p[6] = (p[6],)
            p[0] = nonull({'action': p[1], 'object': p[3], 'attr': p[6]})
        elif isinstance(p[5], tuple):
            if p[5][0] == 'loop':
                p[0] = ({'action': p[1], 'object': p[3], 'obj_loop': p[5][1]},) + p[6]
        print('action1 (7)', p[0])
    elif len(p) == 8:
        if p[5] == 'as':
            if not isinstance(p[6], tuple):
                p[6] = (p[6],)
                p[0] = nonull({'action': p[1], 'object': p[3], 'attr': p[6]}) + p[7]
            else:
                if len(p[6]) == 2:
                    if isinstance(p[6][1], dict):
                        if 'attr_loop' in p[6][1].keys():
                            print('attrloop')
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
            p[0] = nonull({'action': p[1], 'object': p[3], 'obj_loop': p[5][1], 'attr': p[7]})
        print('action1 (8)', p[0])
    elif len(p) == 9:
        if isinstance(p[5], tuple) and len(p[5][1]) == 4 and p[5][1][0] == '_':
            print('fac91')
            if not isinstance(p[7], tuple):
                print('7notuple')
                p[7] = (p[7],)
                p[0] = nonull(
                        {'action': p[1], 'object': p[3], 'obj_loop': p[5][1], 'attr': p[7]}) + p[8]
            else:
                print('7tuple')
                if len(p[7]) == 2:
                    if isinstance(p[7][1], dict):
                        if 'attr_loop' in p[7][1].keys():
                            print('attrloop')
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
                    print('fac92')
                    p[0] = nonull({'action': p[1], 'object': p[3], 'obj_loop': p[5], 'attr': (p[7],), 'attr_loop': p[8][1]})
                else:
                    print('fac93')
                    p[0] = nonull({'action': p[1], 'object': p[3], 'obj_loop': p[5], 'attr': (
                    p[7],), 'attr_loop': p[8]})
            else:
                print('fac94')
                p[0] = nonull(
                    {'action': p[1], 'object': p[3], 'obj_loop': p[5], 'attr': (p[7],)}) + p[8]
        print('action1 (9)', p[0])
    elif len(p) == 10:
        p[0] = nonull({'action': p[1], 'object': p[3], 'obj_loop': p[5][1], 'attr': (p[7],), 'attr_loop': p[8][1]}) + p[9]
        print('action1 (10)', p[0])
    else:
        print('action1 passou')


def p_action2(p):
    """action : defines lbracket str rbracket as attrX
                | defines lbracket str rbracket as attrX action"""
    if len(p) == 7:
        if not isinstance(p[6], tuple):
            p[6] = (p[6],)
        p[0] = nonull({'action': p[1], 'object': (p[3],), 'attr': (p[6],)})
        print('action2 (9)', p[0])
    elif len(p) == 11:
        if not isinstance(p[8], tuple):
            p[6] = (p[8],)
        p[0] = nonull({'action': p[1], 'object': (p[3],), 'attr': (p[8],)}) + p[10]
        print('action2 (11)', p[0])


def p_extended_actions(p):
    """extendaction : actlabelsX
                    | actlabelsX and extendaction"""
    if len(p) == 2:
        p[0] = (p[1],)
    elif len(p) == 4:
        p[0] = (p[1], p[2],) + p[3]


def p_actionX(p):
    """actlabelsX : at actlabels1
                  | actlabels1"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1] + p[2]


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
                    | moves
                    | resets
                    | names
                    | renames
                    | inputs
                    | invokes
                    | queues
                    | consumes
                    | produces
                    | compares
                    | loops
                    | parallels"""
    p[0] = p[1]
    if p[1] == 'sets':
        print(f'* "sets" genealogy: {p[-1], p[0], p[1]}')
    elif p[1] == 'applies':
        print(f'* "applies" genealogy: {p[-1], p[0], p[1]}')
    elif p[1] == 'loops':
        print(f'* "loops" genealogy: {p[-1], p[0], p[1:]}')


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
    print(f'--(!) superobject genealogy {p[-1], p[0], p[1:]}')
    if len(p) == 2:
        if isinstance(p[1], tuple):
            p[0] = p[1]
        else:
            p[0] = (p[1],)
        print('superobject (2)', p[0])
    elif len(p) == 3:
        p[0] = (p[1], p[2])
        #print(f'p[-2] {p[-2]}')
        #print(f'heritage p[-2] {check_action}')
        #print(f'p[0] {p[0]}')
        #result_ = adjust_object_for_action(check_action, p[0])
        #if not result_:
        #    p[0] = "Illegal syntax"
        print('superobject (3)', p[0])
    elif len(p) == 4:
        if p[2] == '&':
            p[2] = (p[2],)
        if not isinstance(p[3], tuple):
            p[3] = (p[3],)
        if not isinstance(p[1], tuple):
            p[1] = (p[1],)
        p[0] = p[1] + p[2] + p[3]
        print('superobject (4)', p[0])
    elif len(p) == 5:
        p[0] = (nonull(p[1], p[2]), p[3]) + (p[4],)
        #print(f'p[-2] {p[-2]}')
        #print(f'heritage p[-2] {check_action}')
        #print(f'p[0] {p[0]}')
        #result_ = adjust_object_for_action(check_action, p[0])
        #if not result_:
        #    p[0] = "Illegal syntax"
        print('superobject (5)', p[0])


def p_object(p):
    """object : superid
                | subject
                | superid object
                | num
                | num object
                | bool1
                | bool1 object
                | str
                | str object
                | superid loop1
                | bool1 loop1
                | bin
                | bin object
                | hex
                | hex object
                | qubinary
                | qubinary object
                | attrtypes
                | attrtypes object"""
    if len(p) == 2:
        if isinstance(p[1], tuple) and len(p[1]) > 1:
            # p[0] = (p[1],)
            p[0] = p[1]
        else:
            if not isinstance(p[1], tuple):
                p[1] = (p[1],)
            p[0] = p[1]
        print('object (2)', p[0])
    elif len(p) == 3:
        # p[0] = nonull(p[1], p[2])
        # if p[1] != 'with':
        #     p[0] = nonull(p[1]) + nonull(p[2])
        # else:
        #     p[0] = p[1] + p[2]
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
                                print('p[2] not str')
                                p[0] = (p[1],) + p[2]
                        else:
                            print('p[1] not ref in keys')
                            p[0] = (p[1],) + p[2]
                    else:
                        print('p[1] not dict')
                        p[0] = (p[1],) + p[2]
                else:
                    print('p[1] not len > 1', p[1], p[2])
                    if isinstance(p[2][0], str):
                        if p[2][0][0] == '"':
                            if isinstance(p[1][0], dict):
                                p[1][0].update({'after_loop': p[2]})
                                p[2] = ()
                            else:
                                pass
                        else:
                            pass
                    else:
                        # p[1] = p[1] + p[2]
                        pass
                    if isinstance(p[1][0], str):
                        if p[1][0][0] == '"':
                            if isinstance(p[2][0], dict):
                                p[2][0].update({'ref': p[1]})
                                p[1] = ()
                            else:
                                pass
                        else:
                            # p[1] = p[1] + p[2]
                            pass
                    else:
                        # p[1] = p[1] + p[2]
                        pass
                    p[0] = p[1] + p[2]
        else:
            if len(p[1]) > 1:
                p[0] = ((p[1],), p[2])
            else:
                print('- object 3 len(p[1])!=1')
                p[0] = p[1] + p[2]
        print('object (3)', p[0])


def p_attrtypes(p):
    """attrtypes : string
                 | real
                 | boolean
                 | hexadecimal
                 | binary
                 | qubin
                 | void"""
    p[0] = p[1]


def p_comp(p):
    """compl : with subject
            | with subject and superobject
            | if subject
            | if subject else action"""
    global check_action
    if p[-2] in actions:
        check_action = p[-2]
    elif check_action is not None:
        pass
    else:
        check_action = None

    if len(p) == 3:
        p[0] = (p[1], p[2])
        #print(f'compl p[-2] {p[-2]}')
        #print(f'compl heritage p[-2] {check_action}')
        #print(f'compl p[0] {p[0]}')
        #result_ = adjust_object_for_action(check_action, p[0])
        #if not result_:
        #    p[0] = "Illegal syntax"
        print('compl (3)', p[0])
    elif len(p) == 5:
        if p[1] == 'if':
            print('if!')
            p[0] = nonull(p[1], p[2], p[3], p[4],)
            #print(f'compl p[-2] {p[-2]}')
            #print(f'compl heritage p[-2] {check_action}')
            #print(f'compl p[0] {p[0]}')
            #result_ = adjust_object_for_action(check_action, p[0])
            #if not result_:
            #    p[0] = "Illegal syntax"
            print('compl (5)', p[0])
        elif p[1] == 'with':
            print('with!')
            p[0] = nonull(p[1], p[2], p[3],) + p[4]
            #print(f'compl p[-2] {p[-2]}')
            #print(f'compl heritage p[-2] {check_action}')
            #print(f'compl p[0] {p[0]}')
            #result_ = adjust_object_for_action(check_action, p[0])
            #if not result_:
            #    p[0] = "Illegal syntax"
            print('compl (5)', p[0])
        else:
            print('compl interno passou')
    else:
        print('compl passou')


def p_statements(p):
    """statements : lparen expression2 rparen loop2
                | lparen expression2 rparen loop2 logelem statements
                | lparen statements rparen loop2
                | lparen statements rparen loop2 logelem statements
                """
    print('statements new day', p[0:])
    if len(p) == 4:
        if p[2][0] != '(':
            print('nested statement')
            p[0] = (p[2],)
        else:
            p[0] = p[2]
        print('statements (4)', p[0])
    elif len(p) == 5:
        if isinstance(p[4], tuple):
            if p[4][0] == 'loop':
                p[0] = (p[2] + ({'obj_loop': p[4][1]},),)
            else:
                p[0] = (p[2],)
        else:
            if p[2][0] != '(':
                print('nested statement')
                p[0] = (p[2],)
            else:
                print('no nested statement')
                p[0] = (p[2],)
        print('statements (5)', p[0])
    elif len(p) == 6:
        if isinstance(p[5], tuple):
            if p[5][0] == 'loop':
                p[0] = (p[2] + ({'oper': p[3], 'obj_loop': p[5][1]},),)
            else:
                p[0] = (p[2],) + (p[4],) + p[5]
        else:
            p[0] = (p[2],) + (p[4],) + p[5]
        print('statements (6)', p[0])
    elif len(p) == 7:
        print('fin stt(7)')
        if not isinstance(p[5], tuple):
            p[5] = (p[5],)

        if p[4] is not None:
            print(f'p[2] is {p[2]}')
            print(f'p[5]= {p[5]}, p[6]= {p[6]}')
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
                print(p[2][0])
                print((p[2], {'obj_loop': p[4][1]},) + p[5] + p[6])
                p[0] = (p[2] + ({'obj_loop': p[4][1]},),) + p[5] + p[6]
        else:
            print('else stt(7)')
            p[0] = (p[2],) + p[5] + p[6]
        print('statements (7)', p[0])
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
        print('statements (8)', p[0])
    elif len(p) == 10:
        if isinstance(p[2], dict) and not isinstance(p[4], dict):
            p[2][0].update({'oper': p[5], 'obj_loop': p[7][1]})
            p[0] = p[2] + (p[3], p[4]) + (p[8],) + p[9]
        elif isinstance(p[4], dict) and not isinstance(p[2], dict):
            p[4][0].update({'oper': p[5], 'obj_loop': p[7][1]})
            p[0] = (p[2], p[3],) + p[4] + (p[8],) + p[9]
        else:
            p[0] = p[2] + (p[3],) + p[4] + ({'oper': p[5], 'obj_loop': p[7][1]},) + (p[8],) + p[9]
        print('statements (10)', p[0])
    else:
        print('statements passou')


def p_expression2(p):
    """expression2 : superid3 symbols1 superid4 logtmp
                    | superid4 logtmp"""
    print('expression2')
    if len(p) == 2:
        p[0] = p[1]
        print('expression2 (2)', p[0])
    elif len(p) == 3:
        if p[2] is not None:
            p[1][0].update({'oper': p[2]})
            p[0] = p[1]
        else:
            if isinstance(p[1][0], dict):
                p[1] = p[1][0]
            p[0] = p[1]
        print('expression2 (3)', p[0])
    elif len(p) == 4:
        if isinstance(p[1], tuple):
            p[0] = p[1] + (p[2],) + p[3]
        else:
            p[0] = (p[1], p[2], p[3],)
        print('expression2 (4)', p[0])
    elif len(p) == 5:
        if p[4] is not None:
            p[0] = (p[1], p[2], p[3], {'oper': p[4]},)
        else:
            p[0] = p[1] + (p[2],) + p[3]
        print('expression2 (5)', p[0])


def p_symbols1(p):
    """symbols1 : equal
                | notequal
                | gt
                | gte
                | lt
                | lte"""
    p[0] = p[1]
    print('symbols', p[0])


def p_logtmp(p):
    """logtmp : logelem
                |"""
    if len(p) == 2:
        p[0] = p[1]


def p_logelem(p):
    """logelem : and
                | or"""
    p[0] = p[1]


def p_attrx(p):
    """attrX : at attr
             | attr"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        if isinstance(p[2], tuple):
            if isinstance(p[2][0], dict):
                p[2][0].update({'@': True})
                p[0] = p[2]
            elif isinstance(p[2][0], str):
                new_p2 = ('@' + p[2][0],)
                new_p2 = new_p2 + p[2][1:]
                p[0] = new_p2
        elif isinstance(p[2], str):
            p[0] = '@' + p[2]


def p_attr(p):
    """attr : id
            | superid
            | superid loop1
            | id attrX"""
    print(f'--(!) start attr {p[-1], p[0], p[1:]}')
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        if p[2][0] == 'loop':
            if isinstance(p[1], dict):
                p[0] = p[1].update({'attr_loop': p[2][1]})
            elif isinstance(p[1], tuple):
                for d0, d in enumerate(p[1]):
                    if isinstance(d, dict):
                        p[1][d0].update({'attr_loop': p[2][1]})
                        p[0] = p[1]
                        break
                if p[0] is None:
                    p[0] = p[1] + ({'attr_loop': p[2][1]},)
            else:
                p[0] = p[1] + ({'attr_loop': p[2][1]},)
        else:
            if not isinstance(p[2], tuple):
                p[2] = (p[2],)
            p[0] = (p[1],) + p[2]
    print('attr', p[0])


def p_loop1(p):
    """loop1 : underscore realnum dots lastloopterm
             | underscore id dots lastloopterm"""
    p[0] = ('loop', nonull(p[1], p[2], p[3], p[4]))
    print('loop1 here', p[0])


def p_loop2(p):
    """loop2 : underscore realnum dots lastloopterm
             | underscore id dots lastloopterm
             |"""
    if len(p) == 5:
        p[0] = ('loop', nonull(p[1], p[2], p[3], p[4]))
    print('loop2 here', p[0])


def p_loopterm1(p):
    """lastloopterm : realnum
                    | id
                    | realnum mod lastloopterm
                    | id mod lastloopterm"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = (p[1], p[2], p[3])


def p_superid(p):
    """superid : id
                | str
                | num
                | id period superid
                | id dollar superid
                | dollar superid"""
    if len(p) == 2:
        p[0] = (p[1],)
        print('superid (2)', p[0])
    elif len(p) == 3:
        if p[1] == '$':
            p[0] = ({'var_loop': p[2]},)
        else:
            p[0] = (p[1], p[2])
        print('superid (3)', p[0])
    elif len(p) == 4:
        if p[2] == '.':
            p[0] = (p[1], p[2]) + p[3]
        else:
            if not isinstance(p[1], tuple):
                p[1] = (p[1],)
            p[0] = ({'ref': p[1], 'var_loop': p[3]},)
        print('superid (4)', p[0])


def p_superid4(p):
    """superid4 : superid3
                | nulls"""
    p[0] = p[1]
    print(f'superid4', p[0])


def p_superid3(p):
    """superid3 : id
                | num
                | bin
                | hex
                | str
                | qubinary
                | id period superid3
                | id dollar superid3
                | dollar superid3"""
    if len(p) == 2:
        p[0] = (p[1],)
        print('superid3 (2)', p[0])
    elif len(p) == 3:
        if p[1] == '$':
            p[0] = ({'var_loop': p[2]},)
        else:
            p[0] = (p[1], p[2])
        print('superid3 (3)', p[0])
    elif len(p) == 4:
        if p[2] == '.':
            p[0] = (p[1], p[2]) + p[3]
        else:
            p[0] = ({'ref': p[1], 'var_loop': p[3]},)
        print('superid3 (4)', p[0])


def p_qubinary(p):
    """qubinary : qubit lparen superid3 rparen
                | qubit lparen superid3 loop1 rparen"""
    if len(p) == 5:
        p[0] = {'qubit': p[3]}
    elif len(p) == 6:
        p[3][0].update({'qubit_loop': p[4][1]})
        p[0] = {'qubit': p[3]}
    print('qubinary', p[0])


def p_bool1(p):
    """bool1 : bool"""
    p[0] = p[1]
    print(f'bool', p[0])


def p_nums_realnum(p):
    """num : realnum"""
    p[0] = p[1]
    print(f'number', p[0])


def p_null1(p):
    """nulls : null
            | none
            | void"""
    p[0] = p[1]
    print(f'void', p[0])


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
    # IPython.embed()
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
