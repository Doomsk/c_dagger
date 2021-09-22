import gpp.yacc as yacc
from gpp.gpp_lex import tokens, actions


def p_sentence_0(p):
    """ tale : root_sentence compl_sentence """
    res0 = p[1]
    if p[2] is not None:
        res0 += p[2]
    p[0] = res0


def p_sentence_1(p):
    """ root_sentence : subj ':' clause """
    res0 = ()
    res1 = dict()
    res2 = ()
    res2 += (p[1],)
    res1.update([("subject", res2)])
    res2 = ()
    res2 += ("root",)
    res1.update([("type", res2)])
    res0 += (res1,)
    res1 = ()
    res1 += (p[3],)
    res0 += (res1,)
    p[0] = res0


def p_sentence_2(p):
    """ obj_sentence : subj ':' clause """
    res0 = ()
    res1 = dict()
    res2 = ()
    res2 += (p[1],)
    res1.update([("subject", res2)])
    res2 = ()
    res2 += ("obj",)
    res1.update([("type", res2)])
    res0 += (res1,)
    res1 = ()
    res1 += (p[3],)
    res0 += (res1,)
    p[0] = res0


def p_sentence_3(p):
    """ next_sentence : clause next_sentence """
    res0 = p[1]
    if p[2] is not None:
        res0 += p[2]
    p[0] = res0


def p_sentence_4(p):
    """ next_sentence :  """
    pass
    

def p_sentence_5(p):
    """ compl_sentence : where sup_sentence compl_sentence """
    res0 = p[2]
    res0 += p[3]
    p[0] = res0


def p_sentence_6(p):
    """ compl_sentence :  """
    pass
    

def p_sentence_7(p):
    """ sup_sentence : subj ':' clause """
    res0 = ()
    res1 = dict()
    res2 = ()
    res2 += (p[1],)
    res1.update([("subject", res2)])
    res2 = ()
    res2 += ("aux",)
    res1.update([("type", res2)])
    res0 += (res1,)
    res1 = ()
    res1 += (p[3],)
    res0 += (res1,)
    p[0] = res0


def p_sentence_8(p):
    """ subj : subj_list """
    res0 = p[1]
    p[0] = res0


def p_sentence_9(p):
    """ clause : action obj_expr attr_expr next_sentence """
    res2 = dict()
    res2.update([("action", p[1])])
    res1 = res2
    res1.update(p[2])
    res1.update(p[3])
    res0 = res1
    if p[4] is not None:
        res0 += p[4]
    p[0] = res0


def p_sentence_10(p):
    """ clause : action obj_expr attr_expr """
    res1 = dict()
    res1.update([("action", p[1])])
    res0 = res1
    res0.update(p[2])
    res0.update(p[3])
    p[0] = res0


def p_sentence_11(p):
    """ clause : action obj_expr next_sentence """
    res2 = dict()
    res2.update([("action", p[1])])
    res1 = res2
    res1.update(p[2])
    res0 = res1
    if p[3] is not None:
        res0 += p[3]
    p[0] = res0


def p_sentence_12(p):
    """ clause : action obj_expr """
    res1 = dict()
    res1.update([("action", p[1])])
    res0 = res1
    res0.update(p[2])
    p[0] = res0


def p_sentence_13(p):
    """ action : action_list """
    res0 = p[1]
    p[0] = res0


def p_sentence_14(p):
    """ action : at action_list """
    res0 = ()
    res1 = "@"
    res1 += p[2]
    res0 += (res1,)
    p[0] = res0


def p_sentence_15(p):
    """ obj_expr : lbracket obj rbracket compl_obj """
    res1 = dict()
    res1.update([("object", p[2])])
    res0 = res1
    if p[4] is not None:
        res0.update(p[4])
    p[0] = res0


def p_sentence_16(p):
    """ obj : obj_subj """
    res0 = p[1]
    p[0] = res0


def p_sentence_17(p):
    """ obj : pure_obj """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_18(p):
    """ obj2 : and obj """
    res1 = ()
    res1 += ("&",)
    res0 = res1
    res0 += p[2]
    p[0] = res0


def p_sentence_19(p):
    """ obj2 :  """
    pass
    

def p_sentence_20(p):
    """ pure_obj : obj_list """
    res0 = p[1]
    p[0] = res0


def p_sentence_21(p):
    """ pure_obj : obj_list pure_obj """
    res0 = p[1]
    res0 += p[2]
    p[0] = res0


def p_sentence_22(p):
    """ pure_obj : obj_list obj2 """
    res0 = p[1]
    if p[2] is not None:
        res0 += p[2]
    p[0] = res0


def p_sentence_23(p):
    """ obj_subj : with obj_sentence """
    res1 = ()
    res1 += ("with",)
    res0 = res1
    res0 += p[2]
    p[0] = res0


def p_sentence_24(p):
    """ obj_subj : with obj_sentence obj2 """
    res1 = ()
    res1 += ("with",)
    res0 = res1
    res0 += p[2]
    if p[3] is not None:
        res0 += p[3]
    p[0] = res0


def p_sentence_25(p):
    """ obj_subj : if obj_sentence obj2 """
    res1 = ()
    res1 += ("if",)
    res0 = res1
    res0 += p[2]
    if p[3] is not None:
        res0 += p[3]
    p[0] = res0


def p_sentence_26(p):
    """ obj_subj : if obj_sentence else next_sentence obj2 """
    res1 = ()
    res1 += ("if",)
    res0 = res1
    res0 += p[2]
    res1 = ()
    res1 += ("else",)
    res0 += res1
    res0 += p[4]
    if p[5] is not None:
        res0 += p[5]
    p[0] = res0


def p_sentence_27(p):
    """ compl_obj : obj_loop """
    res0 = dict()
    res1 = ()
    res1 += (p[1],)
    res0.update([("obj_loop", res1)])
    p[0] = res0


def p_sentence_28(p):
    """ compl_obj :  """
    pass
    

def p_sentence_29(p):
    """ obj_loop : loop obj_loop """
    res0 = p[1]
    if p[2] is not None:
        res0 += p[2]
    p[0] = res0


def p_sentence_30(p):
    """ obj_loop :  """
    pass
    

def p_sentence_31(p):
    """ attr_expr : as attr_vals """
    res0 = dict()
    res0.update([("attr", p[2])])
    p[0] = res0


def p_sentence_32(p):
    """ attr_vals : attr_group """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_33(p):
    """ attr_vals : attr_group attr_vals """
    res1 = ()
    res1 += (p[1],)
    res0 = res1
    res0 += p[2]
    p[0] = res0


def p_sentence_34(p):
    """ attr_group : attr_list """
    res0 = p[1]
    p[0] = res0


def p_sentence_35(p):
    """ attr_group : at attr_list """
    res0 = "@"
    res0 += p[2]
    p[0] = res0


def p_sentence_36(p):
    """ attr_group : attr_list loop """
    res0 = ()
    res2 = dict()
    res2.update([("attr_val", p[1])])
    res1 = res2
    res1.update(p[2])
    res0 += (res1,)
    p[0] = res0


def p_sentence_37(p):
    """ attr_group : at attr_list loop """
    res0 = ()
    res2 = dict()
    res3 = "@"
    res3 += p[2]
    res2.update([("attr_val", res3)])
    res1 = res2
    res1.update(p[3])
    res0 += (res1,)
    p[0] = res0


def p_sentence_38(p):
    """ attr : at attr_list """
    res0 = ()
    res1 = "@"
    res1 += p[2]
    res0 += (res1,)
    p[0] = res0


def p_sentence_39(p):
    """ attr : attr_list """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_40(p):
    """ attr : at attr_list attr """
    res1 = ()
    res2 = "@"
    res2 += p[2]
    res1 += (res2,)
    res0 = res1
    res0 += p[3]
    p[0] = res0


def p_sentence_41(p):
    """ attr : attr_list attr """
    res1 = ()
    res1 += (p[2],)
    res0 = res1
    res0 += p[3]
    p[0] = res0


def p_sentence_42(p):
    """ compl_attr : attr_loop """
    res0 = dict()
    res1 = ()
    res1 += (p[1],)
    res0.update([("attr_loop", res1)])
    p[0] = res0


def p_sentence_43(p):
    """ compl_attr :  """
    pass
    

def p_sentence_44(p):
    """ attr_loop : loop attr_loop """
    res0 = p[1]
    if p[2] is not None:
        res0 += p[2]
    p[0] = res0


def p_sentence_45(p):
    """ attr_loop :  """
    pass
    

def p_sentence_46(p):
    """ loop : underscore id dots left_cur loop_vals right_cur """
    res1 = dict()
    res2 = ()
    res2 += (p[2],)
    res1.update([("var_loop", res2)])
    res0 = res1
    res0.update(p[4])
    res0.update(p[5])
    res0.update(p[6])
    p[0] = res0


def p_sentence_47(p):
    """ left_cur : lbracket """
    res0 = dict()
    res1 = ()
    res1 += ("close",)
    res0.update([("init_lim", res1)])
    p[0] = res0


def p_sentence_48(p):
    """ left_cur : lparen """
    res0 = dict()
    res1 = ()
    res1 += ("open",)
    res0.update([("init_lim", res1)])
    p[0] = res0


def p_sentence_49(p):
    """ right_cur : rbracket """
    res0 = dict()
    res1 = ()
    res1 += ("close",)
    res0.update([("fin_lim", res1)])
    p[0] = res0


def p_sentence_50(p):
    """ right_cur : rparen """
    res0 = dict()
    res1 = ()
    res1 += ("open",)
    res0.update([("fin_lim", res1)])
    p[0] = res0


def p_sentence_51(p):
    """ loop_vals : loop_list """
    res0 = dict()
    res1 = ()
    res1 += (p[1],)
    res0.update([("single", res1)])
    p[0] = res0


def p_sentence_52(p):
    """ loop_vals : loop_list loop_list """
    res0 = dict()
    res1 = ()
    res1 += (p[1],)
    res0.update([("init", res1)])
    res1 = ()
    res1 += (p[2],)
    res0.update([("fin", res1)])
    p[0] = res0


def p_sentence_53(p):
    """ loop_vals : at loop_list loop_list """
    res0 = dict()
    res1 = ()
    res2 = "@"
    res2 += p[1]
    res1 += (res2,)
    res0.update([("init", res1)])
    res1 = ()
    res1 += (p[2],)
    res0.update([("fin", res1)])
    p[0] = res0


def p_sentence_54(p):
    """ loop_vals : loop_list at loop_list """
    res0 = dict()
    res1 = ()
    res1 += (p[1],)
    res0.update([("init", res1)])
    res1 = ()
    res2 = "@"
    res2 += p[2]
    res1 += (res2,)
    res0.update([("fin", res1)])
    p[0] = res0


def p_sentence_55(p):
    """ loop_vals : at loop_list at loop_list """
    res0 = dict()
    res1 = ()
    res2 = "@"
    res2 += p[1]
    res1 += (res2,)
    res0.update([("init", res1)])
    res1 = ()
    res2 = "@"
    res2 += p[2]
    res1 += (res2,)
    res0.update([("fin", res1)])
    p[0] = res0


def p_sentence_56(p):
    """ action_list : names """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_57(p):
    """ action_list : renames """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_58(p):
    """ action_list : loads """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_59(p):
    """ action_list : inputs """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_60(p):
    """ action_list : outputs """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_61(p):
    """ action_list : reads """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_62(p):
    """ action_list : applies """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_63(p):
    """ action_list : starts """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_64(p):
    """ action_list : divides """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_65(p):
    """ action_list : powers """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_66(p):
    """ action_list : maps """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_67(p):
    """ action_list : adds """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_68(p):
    """ action_list : multiplies """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_69(p):
    """ action_list : keeps """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_70(p):
    """ action_list : publishes """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_71(p):
    """ action_list : invokes """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_72(p):
    """ action_list : dequeues """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_73(p):
    """ action_list : queues """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_74(p):
    """ action_list : parallels """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_75(p):
    """ action_list : processes """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_76(p):
    """ action_list : threads """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_77(p):
    """ action_list : produces """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_78(p):
    """ action_list : consumes """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_79(p):
    """ action_list : uses """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_80(p):
    """ action_list : roots """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_81(p):
    """ action_list : sets """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_82(p):
    """ action_list : brings """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_83(p):
    """ action_list : calls """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_84(p):
    """ action_list : waits """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_85(p):
    """ action_list : moves """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_86(p):
    """ action_list : resets """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_87(p):
    """ action_list : repeats """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_88(p):
    """ action_list : executes """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_89(p):
    """ action_list : checks """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_90(p):
    """ action_list : evaluates """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_91(p):
    """ action_list : computes """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_92(p):
    """ action_list : defines """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_93(p):
    """ action_list : compares """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_94(p):
    """ action_list : loops """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_95(p):
    """ action_list : returns """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_96(p):
    """ action_list : translates """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_97(p):
    """ action_list : amplifies """
    res0 = ()
    res0 += (p[1],)
    p[0] = res0


def p_sentence_98(p):
    """ subj_list : id """
    res0 = p[1]
    p[0] = res0


def p_sentence_99(p):
    """ subj_list : dollar id """
    res0 = dict()
    res1 = ()
    res1 += (p[2],)
    res0.update([("var_loop", res1)])
    p[0] = res0


def p_sentence_100(p):
    """ subj_list : id dollar id """
    res0 = dict()
    res1 = ()
    res1 += (p[1],)
    res0.update([("ref", res1)])
    res1 = ()
    res1 += (p[3],)
    res0.update([("var_loop", res1)])
    p[0] = res0


def p_sentence_101(p):
    """ subj_list : id period id """
    res0 = dict()
    res1 = ()
    res1 += (p[1],)
    res0.update([("ref", res1)])
    res1 = ()
    res1 += (p[3],)
    res0.update([("prop", res1)])
    p[0] = res0


def p_sentence_102(p):
    """ subj_list : dollar id period id """
    res0 = dict()
    res1 = ()
    res1 += (p[2],)
    res0.update([("var_loop", res1)])
    res1 = ()
    res1 += (p[4],)
    res0.update([("prop", res1)])
    p[0] = res0


def p_sentence_103(p):
    """ subj_list : id dollar id period id """
    res0 = dict()
    res1 = ()
    res1 += (p[1],)
    res0.update([("ref", res1)])
    res1 = ()
    res1 += (p[3],)
    res0.update([("var_loop", res1)])
    res1 = ()
    res1 += (p[5],)
    res0.update([("prop", res1)])
    p[0] = res0


def p_sentence_104(p):
    """ obj_list : id """
    res0 = p[1]
    p[0] = res0


def p_sentence_105(p):
    """ obj_list : dollar id """
    res0 = dict()
    res1 = ()
    res1 += (p[2],)
    res0.update([("var_loop", res1)])
    p[0] = res0


def p_sentence_106(p):
    """ obj_list : id dollar id """
    res0 = dict()
    res1 = ()
    res1 += (p[1],)
    res0.update([("ref", res1)])
    res1 = ()
    res1 += (p[3],)
    res0.update([("var_loop", res1)])
    p[0] = res0


def p_sentence_107(p):
    """ obj_list : str """
    res0 = p[1]
    p[0] = res0


def p_sentence_108(p):
    """ obj_list : str dollar id """
    res0 = dict()
    res1 = ()
    res1 += (p[1],)
    res0.update([("ref", res1)])
    res1 = ()
    res1 += (p[3],)
    res0.update([("var_loop", res1)])
    p[0] = res0


def p_sentence_109(p):
    """ obj_list : bin """
    res0 = p[1]
    p[0] = res0


def p_sentence_110(p):
    """ obj_list : bool """
    res0 = p[1]
    p[0] = res0


def p_sentence_111(p):
    """ obj_list : hex """
    res0 = p[1]
    p[0] = res0


def p_sentence_112(p):
    """ obj_list : qubit """
    res0 = p[1]
    p[0] = res0


def p_sentence_113(p):
    """ obj_list : realnum """
    res0 = p[1]
    p[0] = res0


def p_sentence_114(p):
    """ obj_list : string """
    res0 = p[1]
    p[0] = res0


def p_sentence_115(p):
    """ obj_list : real """
    res0 = p[1]
    p[0] = res0


def p_sentence_116(p):
    """ obj_list : boolean """
    res0 = p[1]
    p[0] = res0


def p_sentence_117(p):
    """ obj_list : binary """
    res0 = p[1]
    p[0] = res0


def p_sentence_118(p):
    """ obj_list : hexadecimal """
    res0 = p[1]
    p[0] = res0


def p_sentence_119(p):
    """ obj_list : qubin """
    res0 = p[1]
    p[0] = res0


def p_sentence_120(p):
    """ obj_list : null """
    res0 = p[1]
    p[0] = res0


def p_sentence_121(p):
    """ obj_list : none """
    res0 = p[1]
    p[0] = res0


def p_sentence_122(p):
    """ obj_list : void """
    res0 = p[1]
    p[0] = res0


def p_sentence_123(p):
    """ attr_list : id """
    res0 = p[1]
    p[0] = res0


def p_sentence_124(p):
    """ attr_list : dollar id """
    res0 = dict()
    res1 = ()
    res1 += (p[2],)
    res0.update([("var_loop", res1)])
    p[0] = res0


def p_sentence_125(p):
    """ attr_list : id dollar id """
    res0 = dict()
    res1 = ()
    res1 += (p[1],)
    res0.update([("ref", res1)])
    res1 = ()
    res1 += (p[3],)
    res0.update([("var_loop", res1)])
    p[0] = res0


def p_sentence_126(p):
    """ attr_list : id period id """
    res0 = dict()
    res1 = ()
    res1 += (p[1],)
    res0.update([("ref", res1)])
    res1 = ()
    res1 += (p[3],)
    res0.update([("prop", res1)])
    p[0] = res0


def p_sentence_127(p):
    """ attr_list : dollar id period id """
    res0 = dict()
    res1 = ()
    res1 += (p[2],)
    res0.update([("var_loop", res1)])
    res1 = ()
    res1 += (p[4],)
    res0.update([("prop", res1)])
    p[0] = res0


def p_sentence_128(p):
    """ attr_list : id dollar id period id """
    res0 = dict()
    res1 = ()
    res1 += (p[1],)
    res0.update([("ref", res1)])
    res1 = ()
    res1 += (p[3],)
    res0.update([("var_loop", res1)])
    res1 = ()
    res1 += (p[5],)
    res0.update([("prop", res1)])
    p[0] = res0


def p_sentence_129(p):
    """ loop_list : id """
    res0 = p[1]
    p[0] = res0


def p_sentence_130(p):
    """ loop_list : realnum """
    res0 = p[1]
    p[0] = res0


def p_sentence_131(p):
    """ loop_list : str """
    res0 = p[1]
    p[0] = res0


parser = yacc.yacc()


def parse(data, debug=0):
    parser.error = 0
    p = parser.parse(data, debug=debug)
    if p is None:
        return -11
    return p

    