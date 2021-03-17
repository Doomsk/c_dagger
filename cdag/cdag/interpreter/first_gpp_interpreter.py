#!/usr/bin/env python

import pika
import uuid
import gpp.gpp_yacc6 as g

class QTask:
    def __init__(self, action, objects):
        self.action = action
        self.objects = objects
    
    @staticmethod
    def adds(a):
        print("entrou no adds...")
        print(a)
        return sum(a)
    
    @staticmethod
    def loads(file):
        f = open(file, "r")
        print("entrou no loads...")
        return f.readline()
    @staticmethod
    def multiplies(myList):
        print("entrou no multiplies...", myList)
        result = 1
        for x in myList:
             result = result * x 
        return result 
        
    def execute(self):
        print("objects inside Qtask ", self.objects, type(self.objects), self.action )
        if self.action == "multiplies":
#            return self.multiplies([4,3])
            return self.multiplies(self.objects)
        elif self.action == "loads":
            return self.loads(self.objects)
        elif self.action == "adds":
            return self.adds(self.objects)

        return globals()[self.action](self.objects)

class QMemoryData:
    def __init__(self, name, value):
        self.value = value
        self.name  = name
        self.block = False

    def updateValue(self, value):
        if self.block:
            self.value = value

class QMemory:
    variables = dict()
    
    def __init__(self, variables):
        self.variables = variables
        
    def clearMemory(self):
        self.variables = dict()
        
    def insertVar(self, qmem):
        self.variables.insert(qmem)


class GPP_Interpreter(object):
    @staticmethod
    def loadingCMDS(qparse,qmem, subject = '', afterwhere=False):
        lstAction = []
        lstSub    = []

        print("Entrying loadingCMDS...")
        for i in qparse:
            if i == "where":
                print("Where foundded", i )
                break
            if afterwhere:
                pass
                print("afterwhere", type(i))
                print(i['action'][0], subject)
                qmem = GPP_Interpreter.executingAction(i,qmem,subject, qparse,i)

            elif isinstance(i,dict):
                nameSub = i['subject'][0] 
                lstAction.append(nameSub)
              #  print(i['subject'][0])
            if isinstance(i,tuple):
                for j in i:
                    if isinstance(j,dict):                  
                        qmem = GPP_Interpreter.executingAction(j,qmem, nameSub,qparse,i)
        print("Exiting loadingCMDS...")
        return qmem
    
    @staticmethod
    def executingAction(j,qmem, nameSub,qparse,i):
        lstObj = list()
        if j['action'][0] != "uses":
        #    print("Action ", j['action'])
            for iobj in j['object']:
                lstObj.append(iobj)
                pass
            if j['action'][0] != "maps":
                for iobj in j['attr']:
                    qmdata = QMemoryData(nameSub + "_" + iobj, 0) 
                    qmem[qmdata.name] = 0

            if j['action'][0] == "loads":
                vla = QTask(j['action'][0],lstObj[0].replace('"','')).execute()
                qmdata = QMemoryData(nameSub + "_" + iobj, vla)
                qmem[qmdata.name] = vla

            elif j['action'][0] == "applies":
                
                qmem = GPP_Interpreter.loadingCMDS(j['object'][1], qmem, j['object'][1][0]['subject'][0]) ### Version Jan14
                listingAction = GPP_Interpreter.findActions(qparse,j['object'][1][0]['subject'][0]) ## Version Jan14
                qmem = GPP_Interpreter.loadingCMDS(listingAction, qmem, j['object'][1][0]['subject'][0], True ) ## Jan14

#               qmem = GPP_Interpreter.loadingCMDS(j['object'][1][0], qmem, j['object'][1][0][0]['subject'][0]) ### Version Jan3
    
#                listingAction = GPP_Interpreter.findActions(qparse,j['object'][1][0][0]['subject'][0]) ## Version Jan3
 
    #              qmem = GPP_Interpreter.loadingCMDS(listingAction, qmem, j['object'][1][0][0]['subject'][0], True ) ## Jan3
    
    

                for ii,iatt in enumerate(j['attr']):
                        qmem[nameSub + "_" + iatt] =  qmem[j['object'][1][0]['subject'][0] + "_returnValue_" + str(ii)] ## Jan14
#                        qmem[nameSub + "_" + iatt] =  qmem[j['object'][1][0][0]['subject'][0] + "_returnValue_" + str(ii)] ## Jan3


    #            qmem[nameSub + "_" + j['attr'][0]] =  qmem[j['object'][1][0][0]['subject'][0] + "_returnValue_0"]

            elif j['action'][0] == "multiplies":
                lstParams = list()

                for iobj in j['object']:
                    if isinstance(iobj, str):
                        print("deve ser v2 ", nameSub + "_" + iobj)
                        lstParams.append(qmem[nameSub + "_" + iobj])
                    elif isinstance(iobj, int):
                        lstParams.append(iobj)
              #  print(lstParams)
                print(qmem)
                print("lstParams --> ", lstParams)

                qqq = QTask('multiplies',lstParams)

                print("multiplies !!! ", qqq.execute())

                ## Needs to test if there are more attr
                qmem[nameSub + "_" + j['attr'][0]] = qqq.execute()


            elif j['action'][0] == "adds":
                lstParams = list()

                for iobj in j['object']:
                    if isinstance(iobj, str):
                            lstParams.append(qmem[nameSub + "_" + iobj])
                    ## Needs to check if there are other values basides string as objects
    #                                else
    #                                        lstParams.append(qmem[nameSub + "_" + str(iobj)] )

                qqq = QTask('adds',lstParams)
                ## Needs to test if there are more attr
                qmem[nameSub + "_" + j['attr'][0]] = qqq.execute()

             #   print("adds !!! ", qqq.execute())
            elif j['action'][0] == "maps":
                pos = 0
                for iobj in j['object']:
                    qmdata = QMemoryData(nameSub + "_waitUses_" + str(pos), i)
                    qmem[qmdata.name] = int(iobj)
                 #   print("No maps !!Object ", iobj)
                    pos = pos + 1
            elif j['action'][0] == "sets":
                print("Sets", nameSub)
                pos = 0
                for iatt in j['attr']:
                    qmdata  = QMemoryData(nameSub + "_" + iatt, 0)
                    qmem[qmdata.name] = qmem[nameSub + "_waitUses_" + str(pos)]
                    pos = pos + 1
              #      print("Sets .. ", iatt)

        else:
            # Returning only one value ....it needs to check more returned values
            print("Action ", j['action'], j['object'] )
            for ii,iobj in enumerate(j['object']):
                print(nameSub, qmem[nameSub + "_" + j['object'][0]] )
                qmem[nameSub + "_returnValue_" + str(ii)] = qmem[nameSub + "_" + iobj]
          #  print(j)
    #                      print("Object ", j['object'][0])
        return qmem
    @staticmethod
    def findActions(qparse, subject):
        prox = True
        lstAction = []
        for i in qparse:
            if prox:
                if isinstance(i,dict):
                    if i['subject'][0] == subject:
                        prox = False
            else:
                prox = True
                for j in i:
                    lstAction.append(j)
        return lstAction

if __name__ == "__main__":
    code = """main: loads ["exemplo1.txt"] as v1
          applies [with soma: maps [1 3]] as v2
          multiplies [3 v2] as v3
          uses [v1 v3]
    where       
    soma: sets [*v1 *v2] as v1 v2
          adds [v1 v2] as v3
          uses [v3]
          """
    qmem = dict()

    ex2 = g.parse(code)
    print("#############")
    print(ex2)
    print("#############")
    #lst = findActions(ex2, 'soma')
    qmem = GPP_Interpreter.loadingCMDS(ex2,qmem)
    #lst
    import json
    print(json.dumps(qmem, indent = 4))
