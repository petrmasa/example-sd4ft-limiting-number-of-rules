# DEMONSTRATION OF ALGORITHM TO FIND REQUIRED NUMBER OF RULES FOR CLEVERMINER PROCEDURE SD4ft-Miner, dataset Adults
# (c) 2022-2023 Petr Masa, allrights reserved

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



features = ["Age", "Workclass", "fnlwgt", "Education", "Education_Num", "Martial_Status",
        "Occupation", "Relationship", "Race", "Sex", "Capital_Gain", "Capital_Loss",
        "Hours_per_week", "Country", "Target"]



edu_cat = ["Preschool","1st-4th", "5th-6th", "7th-8th","9th","10th","11th","12th","HS-grad","Some-college","Assoc-voc","Assoc-acdm","Bachelors","Masters","Prof-school","Doctorate"]
edu_cat_type =CategoricalDtype(categories=edu_cat, ordered=True)


# Comment this two lines of code and uncomment following 2 if you have downloaded files locally
train_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data'
test_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.test'


#train_url = 'w:\\development\\cleverminer\\_data\\adult.data'
#test_url = 'w:\\development\\cleverminer\\_data\\adult.test'



original_train = pd.read_csv(train_url, names=features, sep=r'\s*,\s*',
                             engine='python', na_values="?")
original_test = pd.read_csv(test_url, names=features, sep=r'\s*,\s*',
                            engine='python', na_values="?", skiprows=1)

original_test.Target = original_test.Target.str.replace('.','')


original = pd.concat([original_train, original_test])

original['Education'] = original['Education'].astype('category').cat.reorder_categories(edu_cat,ordered=True)

age_bins=[10,20,30,40,50,60,70,90]
original['Age_b'] = pd.cut(original['Age'], include_lowest=True, bins = age_bins, labels = getlabels(age_bins), ordered=True)
hpw_bins=[0,10,20,30,40,50,60,70,100]
original['Hours_per_week_b'] = pd.cut(original['Hours_per_week'], include_lowest=True, bins = hpw_bins, labels = getlabels(hpw_bins), ordered=True)
cl_bins=[-1,0,1500,1600,1700,1800,1900,2000,2100,2200,2300,2400,2500,4400]
original['Capital_Loss_b'] = pd.cut(original['Capital_Loss'], include_lowest=True, bins = cl_bins,labels = getlabels(cl_bins), ordered=True)
cg_bins = [-1,0,2000,3000,4000,5000,7000,10000,20000,99000,100000]
original['Capital_Gain_b'] = pd.cut(original['Capital_Gain'], include_lowest=True, bins = cg_bins , labels = getlabels(cg_bins), ordered=True)

original['Income']=original['Target']

df = original[['Income','Capital_Gain_b','Capital_Loss_b','Hours_per_week_b','Occupation','Martial_Status','Relationship','Age_b','Education','Sex','Country','Race','Workclass','Target']]



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
                              {'name': 'Martial_Status', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                              {'name': 'Relationship', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                              {'name': 'Education', 'type': 'seq', 'minlen': 1, 'maxlen': 4},
                              {'name': 'Age_b', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                              {'name': 'Occupation', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                              {'name': 'Hours_per_week_b', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                          ], 'minlen': 1, 'maxlen': 6, 'type': 'con'},
                      succ={
                          'attributes': [
                              {'name': 'Income', 'type': 'one', 'value': '>50K'},
                          ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                      frst={
                          'attributes': [
                              {'name': 'Sex', 'type': 'lcut', 'minlen': 1, 'maxlen': 1}
                          ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                      scnd={
                          'attributes': [
                              {'name': 'Sex', 'type': 'rcut', 'minlen': 1, 'maxlen': 1}
                          ], 'minlen': 1, 'maxlen': 1, 'type': 'con'}
                      )

    a_file = open("w:\\development\\cleverminer\\logs\\result"+str(step)+".json", "w")
    json.dump(clm.result, a_file)
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





