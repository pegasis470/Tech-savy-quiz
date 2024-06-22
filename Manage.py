import pandas as pd 
import random
import os


def read_file() -> pd.DataFrame:
    for i in os.listdir(os.path.join(os.getcwd(),'files')):
        ext=i.split('.')[-1]
        name = i.split('.')[0]
        if name == 'qustions':
            if ext =='xlsx':
                qus=pd.read_excel(os.path.join('files',"qustions.xlsx"))
                return qus
            elif ext== 'csv': 
                qus=pd.read_csv(os.path.join('files',"qustions.csv"))
                return qus
            else:
                raise FileNotFoundError("The format of your file is incompitable please convert it to .csv or .xlsx")
        else:
            pass
    raise FileNotFoundError('Your Qustions file is missing or misnamed please add it in the files dir and name it "qustions". ')

def check_file() -> None:
    try:
        f=open(os.path.join('files','data.csv'),'r')
        f.close()
    except FileNotFoundError:
        f=open(os.path.join('files','data.csv'),'w')
        f.write('ID,Start time,End time,name,section,enrolment,')
        for i in range(0,len(read_file().columns)-1):
            f.write(f'{i},')
        f.write(f'{len(read_file().columns)-1},Score')
        f.close()

def make_data() :
    qus=read_file()
    list_out=[]
    seq_list=[]
    qus_list=list(range(len(qus.columns)))
    for _ in range(len(qus.columns)):
        i=random.choice(qus_list)
        temp=dict()
        temp['qustion']=qus.iloc[0:1,i:i+1].values[0][0]
        temp['choice1']=qus.iloc[1:2,i:i+1].values[0][0]
        temp['choice2']=qus.iloc[2:3,i:i+1].values[0][0]
        temp['choice3']=qus.iloc[3:4,i:i+1].values[0][0]
        temp['choice4']=qus.iloc[4:5,i:i+1].values[0][0]
        list_out.append(temp)
        seq_list.append(i)
        qus_list.remove(i)
    return list_out,seq_list

def publish_result(write_list,secq) :
    ans_dict={secq[i]:write_list[i] for i in range(len(secq))}
    sort=list(ans_dict.keys())
    sort.sort()
    sorted_ans=[]
    for i in sort:
        sorted_ans.append(ans_dict.get(i))
    original_ans=open(os.path.join('files','answers.csv')).readline().strip('\n').split(',')
    marks=[]
    for i in range(len(original_ans)):
        if sorted_ans[i]==original_ans[i]:
            marks.append(1)
        else:
            marks.append(0)
    marks=sum(marks)
    return marks,sorted_ans
