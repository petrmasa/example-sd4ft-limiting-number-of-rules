import json

import pandas as pd


from cleverminer import cleverminer
from pandas.api.types import CategoricalDtype

def getlabels(s):
    lst = []
    for i in range(len(s)-1):
        j=i+1
        if (j==1):
            item = '<' + str(s[i]) + ','+ str(s[i+1]) + '>'
        else:
            item = '(' + str(s[i]) + ','+ str(s[i+1]) + '>'
        lst.append(item)

    print(s)
    print(lst)
    return lst



original=pd.read_csv("w:\\development\\cleverminer\\_data\\bmi_train.csv")

print(original.columns)
#exit(0)


to_qcut=['Height', 'Weight']


for varname in to_qcut:
    original[varname] = pd.qcut(original[varname], q=5)


df=original


print(df)

#CHANGE FOLLOWING 2 LINES TO SET REQUIRED RULE COUNT
hypo_lowerrange=30
hypo_upperrange=50

conf_mult = 1.2
base_mult = 2

last_way = 0
last_conf=0
last_base=0
last_hypo_cnt=0
act_conf=0
act_base=0
act_hypo_cnt=0
req_stop=0
req_ratioconf=1.5
req_base=1000
req_way = 0
act_way=0
lower_hypo_cnt=0
lower_conf=0
lower_base=0
upper_hypo_cnt=0
upper_conf=0
upper_base=0
approaching=0
finished=0
step=1
step_list = []


while not(req_stop):

    clm = cleverminer(df=df, proc='SD4ftMiner',
                      quantifiers={'Base1': req_base, 'Base2': req_base, 'Ratiopim': req_ratioconf},
                      ante={
                          'attributes': [
                              {'name': 'Height', 'type': 'seq', 'minlen': 1, 'maxlen': 3},
                              {'name': 'Weight', 'type': 'seq', 'minlen': 1, 'maxlen': 3},
                          ], 'minlen': 1, 'maxlen': 2, 'type': 'con'},
                      succ={
                          'attributes': [
                              {'name': 'Index', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                          ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                      frst={
                          'attributes': [
                              {'name': 'Gender', 'type': 'lcut', 'minlen': 1, 'maxlen': 1}
                          ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                      scnd={
                          'attributes': [
                              {'name': 'Gender', 'type': 'rcut', 'minlen': 1, 'maxlen': 1}
                          ], 'minlen': 1, 'maxlen': 1, 'type': 'con'}
                      )

    a_file = open("w:\\development\\cleverminer\\logs\\result"+str(step)+".json", "w")
    json.dump(str(clm.result), a_file)
    a_file.close()

    act_hypo_cnt= clm.get_rulecount() #len(clm.result.get("rules"))
    act_ratioconf=req_ratioconf
    act_base=req_base
    act_way=req_way
    step_details={}
    step_details['step_id'] = step
    step_details['rule_cnt']=act_hypo_cnt
    step_details['ratioconf']=act_ratioconf
    step_details['base']=act_base
    step_list.append(step_details)
    print(f"Step {step}, rules_count={act_hypo_cnt}, act_base = {req_base}, act_ratioconf = {req_ratioconf}")
#    print(f"Step {step}, rules_count={act_hypo_cnt}")
    if (act_hypo_cnt>=hypo_lowerrange and act_hypo_cnt<=hypo_upperrange):
        req_stop=1
        finished=1
        print(f"RESULT ACHIEVED. RatioConf = {act_ratioconf}, Base = {act_base}, Rules count = {act_hypo_cnt}")
        clm.print_hypolist()
    else:
        if(step==1):
            approaching=1
            if (act_hypo_cnt<hypo_lowerrange):
                req_way = +1
            else:
                req_way = -1
        elif(step>=100):
            print("Stopping at step #100")
            req_stop=1
        if (approaching==1):
            if (act_hypo_cnt<hypo_lowerrange and req_way==-1) or (act_hypo_cnt>hypo_upperrange and req_way==1):
                approaching=2 #stop approaching
                if (req_way==-1): #last lowering was enough
                    lower_hypo_cnt = act_hypo_cnt
                    lower_base = act_base
                    lower_ratioconf = act_ratioconf
                    upper_base = last_base
                    upper_ratioconf = last_ratioconf
                    upper_hypo_cnt = last_hypo_cnt
                else: #last uppering was enough
                    upper_hypo_cnt = act_hypo_cnt
                    upper_base = act_base
                    upper_ratioconf = act_ratioconf
                    lower_base = last_base
                    lower_ratioconf = last_ratioconf
                    lower_hypo_cnt = last_hypo_cnt
            elif (req_way==-1): #need to lower number of rules, still no upper boundary set
                req_base=req_base* base_mult
                req_ratioconf= req_ratioconf *conf_mult
            else: #need to increase number of rules
                req_base=req_base/base_mult
                req_ratioconf = (req_ratioconf-1) /conf_mult +1
        if (approaching>=2):
            if (approaching==3):
                if (act_hypo_cnt>hypo_upperrange):
                    upper_hypo_cnt = act_hypo_cnt
                    upper_base = act_base
                    upper_ratioconf = act_ratioconf
                else:
                    lower_hypo_cnt = act_hypo_cnt
                    lower_base = act_base
                    lower_ratioconf = act_ratioconf
            req_ratioconf = (lower_ratioconf+upper_ratioconf)/2
            req_base = (lower_base+upper_base)/2
            approaching=3

        last_base = act_base
        last_hypo_cnt = act_hypo_cnt
        last_ratioconf = act_ratioconf
        last_way=act_way
        step = step + 1

print(clm.result)
print(step_list)
a_file = open("w:\\development\\cleverminer\\logs\\step_list.json", "w")
json.dump(step_list, a_file)
a_file.close()

if (finished):
    print("RESULT ACHIEVED")
elif (step>=100 and approaching>=2) :
    print("MAXIMUM STEPS REACHED, CLOSE TO SOLUTION")
else:
    print("MAXIMUM/MINIMUM RULES ACHIEVED, NO SIGNIFICANTLY BETTER SOLUTION EXISTS")





