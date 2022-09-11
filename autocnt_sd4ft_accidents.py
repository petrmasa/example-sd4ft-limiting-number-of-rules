# DEMONSTRATION OF ALGORITHM TO FIND REQUIRED NUMBER OF RULES FOR CLEVERMINER PROCEDURE SD4ft-Miner, dataset Accidents
# (c) 2022 Petr Masa, allrights reserved

import json

import pandas as pd

from sklearn.impute import SimpleImputer

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



df = pd.read_csv ('c:\\tmp\\accidents.txt ', encoding='cp1250', sep='\t')

df['Day_of_Week']=df['Day_of_Week s kody kategorii ']
df=df[['Driver_Age_Band','Driver_IMD','Sex','Journey','Hit_Objects_in','Hit_Objects_off','Casualties','Severity','Hour','Month','Year','Day_of_Week','Area','Manoeuvre','Light','Road_Type','Speed_limit','Vehicle_Age','Vehicle_Type','District','Police','Highway']]

imputer = SimpleImputer(strategy="most_frequent")
df = pd.DataFrame(imputer.fit_transform(df),columns = df.columns)

Driver_IMD_cat = [1.0, 2.0,3.0,4.0, 5.0, 6.0,7.0,8.0,9.0,10.0]
Driver_IMD_cat_type =CategoricalDtype(categories=Driver_IMD_cat, ordered=True)
df['Driver_IMD'] = df['Driver_IMD'].astype('category').cat.reorder_categories(Driver_IMD_cat,ordered=True)

Vehicle_Age_cat = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16-20','>20']
Vehicle_Age_cat_type =CategoricalDtype(categories=Vehicle_Age_cat, ordered=True)
df['Vehicle_Age'] = df['Vehicle_Age'].astype('category').cat.reorder_categories(Vehicle_Age_cat,ordered=True)

df['Hit_Objects_in']=df['Hit_Objects_in'].astype(float).astype(int).astype('category')

df['Hit_Objects_off']=df['Hit_Objects_off'].astype(float).astype(int).astype('category')

df['Hour']=df['Hour'].astype(float).astype(int).astype('category')


Month_cat = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
Month_cap_type =CategoricalDtype(categories=Month_cat, ordered=True)
df['Month'] = df['Month'].astype('category').cat.reorder_categories(Month_cat,ordered=True)


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


    ## REPLACE FOLLOWING COMMAND WITH COMMAND AFTER exit(0) - commands are labelled by section number

    clm = cleverminer(df=df, proc='SD4ftMiner',
                      quantifiers={'Base1': req_base, 'Base2': req_base, 'Ratiopim': req_ratioconf},
                      ante={
                          'attributes': [
                              {'name': 'District', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                              {'name': 'Highway', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                              {'name': 'Police', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                          ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                      succ={
                          'attributes': [
                              {'name': 'Severity', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                          ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                      frst={
                          'attributes': [
                              {'name': 'Driver_Age_Band', 'type': 'rcut', 'minlen': 1, 'maxlen': 4}
                          ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                      scnd={
                          'attributes': [
                              {'name': 'Driver_Age_Band', 'type': 'lcut', 'minlen': 1, 'maxlen': 4}
                          ], 'minlen': 1, 'maxlen': 1, 'type': 'con'}
                      )

    a_file = open("c:\\tmp\\result"+str(step)+".json", "w")
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

#print(clm.result)
#print(step_list)
a_file = open("c:\\tmp\\step_list.json", "w")
json.dump(step_list, a_file)
a_file.close()

if (finished):
    print("RESULT ACHIEVED")
elif (step>=100 and approaching>=2) :
    print("MAXIMUM STEPS REACHED, CLOSE TO SOLUTION")
else:
    print("MAXIMUM/MINIMUM RULES ACHIEVED, NO SIGNIFICANTLY BETTER SOLUTION EXISTS")





exit(0)

#7.2
clm = cleverminer(df=df, proc='SD4ftMiner',
                  quantifiers={'Base1': req_base, 'Base2': req_base, 'Ratiopim': req_ratioconf},
                  ante={
                      'attributes': [
                          {'name': 'Hour', 'type': 'seq', 'minlen': 1, 'maxlen': 2},
                          {'name': 'Day_of_Week', 'type': 'seq', 'minlen': 1, 'maxlen': 1},
                          {'name': 'Month', 'type': 'seq', 'minlen': 1, 'maxlen': 1},
                          {'name': 'Year', 'type': 'seq', 'minlen': 1, 'maxlen': 1}
                      ], 'minlen': 1, 'maxlen': 2, 'type': 'con'},
                  succ={
                      'attributes': [
                          {'name': 'Severity', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  frst={
                      'attributes': [
                          {'name': 'Driver_Age_Band', 'type': 'lcut', 'minlen': 1, 'maxlen': 4}
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  scnd={
                      'attributes': [
                          {'name': 'Driver_Age_Band', 'type': 'rcut', 'minlen': 1, 'maxlen': 4}
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'}
                  )

#7.3
clm = cleverminer(df=df, proc='SD4ftMiner',
                  quantifiers={'Base1': req_base, 'Base2': req_base, 'Ratiopim': req_ratioconf},
                  ante={
                      'attributes': [
                          {'name': 'Sex', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                          {'name': 'Journey', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                          {'name': 'Driver_IMD', 'type': 'seq', 'minlen': 1, 'maxlen': 3}
                      ], 'minlen': 1, 'maxlen': 2, 'type': 'con'},
                  succ={
                      'attributes': [
                          {'name': 'Severity', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  frst={
                      'attributes': [
                          {'name': 'Driver_Age_Band', 'type': 'lcut', 'minlen': 1, 'maxlen': 4}
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  scnd={
                      'attributes': [
                          {'name': 'Driver_Age_Band', 'type': 'rcut', 'minlen': 1, 'maxlen': 4}
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'}
                  )

#7.4

clm = cleverminer(df=df, proc='SD4ftMiner',
                  quantifiers={'Base1': req_base, 'Base2': req_base, 'Ratiopim': req_ratioconf},
                  ante={
                      'attributes': [
                          {'name': 'Area', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                          {'name': 'Light', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                          {'name': 'Manoeuvre', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                          {'name': 'Road_Type', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                          {'name': 'Speed_limit', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                      ], 'minlen': 1, 'maxlen': 5, 'type': 'con'},
                  succ={
                      'attributes': [
                          {'name': 'Severity', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  frst={
                      'attributes': [
                          {'name': 'Driver_Age_Band', 'type': 'lcut', 'minlen': 1, 'maxlen': 4}
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  scnd={
                      'attributes': [
                          {'name': 'Driver_Age_Band', 'type': 'rcut', 'minlen': 1, 'maxlen': 4}
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'}
                  )


#7.5

clm = cleverminer(df=df, proc='SD4ftMiner',
                  quantifiers={'Base1': req_base, 'Base2': req_base, 'Ratiopim': req_ratioconf},
                  ante={
                      'attributes': [
                          {'name': 'Vehicle_Age', 'type': 'seq', 'minlen': 1, 'maxlen': 5},
                          {'name': 'Vehicle_Type', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  succ={
                      'attributes': [
                          {'name': 'Severity', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  frst={
                      'attributes': [
                          {'name': 'Driver_Age_Band', 'type': 'lcut', 'minlen': 1, 'maxlen': 4}
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  scnd={
                      'attributes': [
                          {'name': 'Driver_Age_Band', 'type': 'rcut', 'minlen': 1, 'maxlen': 4}
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'}
                  )

#7.6

clm = cleverminer(df=df, proc='SD4ftMiner',
                  quantifiers={'Base1': req_base, 'Base2': req_base, 'Ratiopim': req_ratioconf},
                  ante={
                      'attributes': [
                          {'name': 'District', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                          {'name': 'Highway', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                          {'name': 'Police', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  succ={
                      'attributes': [
                          {'name': 'Severity', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  frst={
                      'attributes': [
                          {'name': 'Driver_Age_Band', 'type': 'lcut', 'minlen': 1, 'maxlen': 4}
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  scnd={
                      'attributes': [
                          {'name': 'Driver_Age_Band', 'type': 'rcut', 'minlen': 1, 'maxlen': 4}
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'}
                  )

#8.2
clm = cleverminer(df=df, proc='SD4ftMiner',
                  quantifiers={'Base1': req_base, 'Base2': req_base, 'Ratiopim': req_ratioconf},
                  ante={
                      'attributes': [
                          {'name': 'Hour', 'type': 'seq', 'minlen': 1, 'maxlen': 2},
                          {'name': 'Day_of_Week', 'type': 'seq', 'minlen': 1, 'maxlen': 1},
                          {'name': 'Month', 'type': 'seq', 'minlen': 1, 'maxlen': 1},
                          {'name': 'Year', 'type': 'seq', 'minlen': 1, 'maxlen': 1}
                      ], 'minlen': 1, 'maxlen': 2, 'type': 'con'},
                  succ={
                      'attributes': [
                          {'name': 'Severity', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  frst={
                      'attributes': [
                          {'name': 'Driver_Age_Band', 'type': 'rcut', 'minlen': 1, 'maxlen': 4}
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  scnd={
                      'attributes': [
                          {'name': 'Driver_Age_Band', 'type': 'lcut', 'minlen': 1, 'maxlen': 4}
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'}
                  )

#8.3
clm = cleverminer(df=df, proc='SD4ftMiner',
                  quantifiers={'Base1': req_base, 'Base2': req_base, 'Ratiopim': req_ratioconf},
                  ante={
                      'attributes': [
                          {'name': 'Sex', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                          {'name': 'Journey', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                          {'name': 'Driver_IMD', 'type': 'seq', 'minlen': 1, 'maxlen': 3}
                      ], 'minlen': 1, 'maxlen': 2, 'type': 'con'},
                  succ={
                      'attributes': [
                          {'name': 'Severity', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  frst={
                      'attributes': [
                          {'name': 'Driver_Age_Band', 'type': 'rcut', 'minlen': 1, 'maxlen': 4}
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  scnd={
                      'attributes': [
                          {'name': 'Driver_Age_Band', 'type': 'lcut', 'minlen': 1, 'maxlen': 4}
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'}
                  )

#8.4

clm = cleverminer(df=df, proc='SD4ftMiner',
                  quantifiers={'Base1': req_base, 'Base2': req_base, 'Ratiopim': req_ratioconf},
                  ante={
                      'attributes': [
                          {'name': 'Area', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                          {'name': 'Light', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                          {'name': 'Manoeuvre', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                          {'name': 'Road_Type', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                          {'name': 'Speed_limit', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                      ], 'minlen': 1, 'maxlen': 5, 'type': 'con'},
                  succ={
                      'attributes': [
                          {'name': 'Severity', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  frst={
                      'attributes': [
                          {'name': 'Driver_Age_Band', 'type': 'rcut', 'minlen': 1, 'maxlen': 4}
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  scnd={
                      'attributes': [
                          {'name': 'Driver_Age_Band', 'type': 'lcut', 'minlen': 1, 'maxlen': 4}
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'}
                  )


#8.5

clm = cleverminer(df=df, proc='SD4ftMiner',
                  quantifiers={'Base1': req_base, 'Base2': req_base, 'Ratiopim': req_ratioconf},
                  ante={
                      'attributes': [
                          {'name': 'Vehicle_Age', 'type': 'seq', 'minlen': 1, 'maxlen': 5},
                          {'name': 'Vehicle_Type', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  succ={
                      'attributes': [
                          {'name': 'Severity', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  frst={
                      'attributes': [
                          {'name': 'Driver_Age_Band', 'type': 'rcut', 'minlen': 1, 'maxlen': 4}
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  scnd={
                      'attributes': [
                          {'name': 'Driver_Age_Band', 'type': 'lcut', 'minlen': 1, 'maxlen': 4}
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'}
                  )

#8.6

clm = cleverminer(df=df, proc='SD4ftMiner',
                  quantifiers={'Base1': req_base, 'Base2': req_base, 'Ratiopim': req_ratioconf},
                  ante={
                      'attributes': [
                          {'name': 'District', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                          {'name': 'Highway', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                          {'name': 'Police', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  succ={
                      'attributes': [
                          {'name': 'Severity', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  frst={
                      'attributes': [
                          {'name': 'Driver_Age_Band', 'type': 'rcut', 'minlen': 1, 'maxlen': 4}
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  scnd={
                      'attributes': [
                          {'name': 'Driver_Age_Band', 'type': 'lcut', 'minlen': 1, 'maxlen': 4}
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'}
                  )


