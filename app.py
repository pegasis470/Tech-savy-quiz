from flask import Flask,request ,render_template ,redirect ,session
from datetime import datetime as dt
import uuid 
import pytz
import pandas as pd 
import numpy as np
from Manage import *
import os


app=Flask(__name__)
app.secret_key = 'LNCT_BCA_TECHSAVY_QUIZ'
global active_req,all_req
active_req=set()
check_file()
all_req=list(pd.read_csv(os.path.join('files','data.csv'))['ID'].values)


def gen_ID():
    while True:
        new_id = uuid.uuid4().int % 900
        if new_id not in active_req and new_id not in all_req:
            active_req.add(new_id)
            return new_id


@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        name = request.form.get("name")
        section = request.form.get("sec")
        Enrolment= request.form.get("ENR")
        session['info']=f'{name},{section},{Enrolment}'
        return redirect(f'/quiz?name={name}&sec={section}&ENR={Enrolment}')
    return render_template('index.html')


@app.route('/quiz',methods=['GET','POST'])
def Quiz():
    if request.method == 'POST':
        write_list=[]
        ID=request.form.get("unique_id")
        write_list.append(ID)
        write_list.append(request.form.get("start"))
        write_list.append(dt.now(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f'))
        write_list.append(request.args.get('name'))
        write_list.append(request.args.get('sec'))
        write_list.append(request.args.get('ENR'))
        for i in range(1,len(read_file().columns)+1):
            write_list.append(request.form.get(f'{i}'))
        secq=[]
        for i in range(1,len(write_list)-5):
            secq.append(int(request.form.get(f'seq {i}')))
        marks,answers=publish_result(write_list[6:],secq)
        df=pd.read_csv(os.path.join('files','data.csv'))
        df.loc[len(df.index)+1] = write_list[:6]+answers+[marks]
        #df.loc[len(df.index)+1]=secq
        df.to_csv(os.path.join('files','data.csv'),index=False)
        return render_template('thankyou.html',uid=ID,mark=marks)
    ## GET request is handled here
    Data,seq_lst=make_data()
    ID=gen_ID()
    start=dt.now(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    return render_template('quiz.html',id=ID,unique_id=ID,start=start,data=Data,seq_list=seq_lst)

if __name__=='__main__':
    app.run(debug=True)
