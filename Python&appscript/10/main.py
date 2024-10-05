from fastapi import FastAPI,Form,Request
import hashlib
import httpx
import pandas as pd
from datetime import datetime
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
import os
def getUserTable():
    return pd.read_excel(os.getenv("comedu_sheet"))
app=FastAPI()
tmp=Jinja2Templates(directory="tmp")
@app.get("/")
def index():
    return FileResponse("index.html")
@app.get("/signupform")
def index():
    return FileResponse("signup.html")

@app.post("/signup")
async def signup(request:Request,name:str=Form(...),id: str = Form(...),pw: str = Form(...),sex: str = Form(...),date: datetime = Form(...),ph1: str = Form(...),ph2: str = Form(...),ph3: str = Form(...),m1: str = Form(...),m2: str = Form(...),m3: str = Form(...),m4: str = Form(...)):
    df=getUserTable()
    ph="-".join([ph1,ph2,ph3])
    if len(df[(df['아이디']==id)|(df['전화번호']==ph)])==0:
        pw = hashlib.sha256(pw.encode()).hexdigest()
        print({
            "method":"insert",
            "id":id,
            "pw":pw,
            "name":name,
            "sex":sex,
            "date":date.strftime("%Y-%m-%d"),
            "ph":ph,
            "mbti":m1+m2+m3+m4
        })
        async with httpx.AsyncClient() as client:
            response=await client.post(os.getenv("comedu_system"),data={
            "method":"insert",
            "id":id,
            "pw":pw,
            "name":name,
            "sex":sex,
            "date": date.strftime("%Y-%m-%d"),
            "ph":ph,
            "mbti":m1+m2+m3+m4
        })
        return tmp.TemplateResponse('err.html',{'request':request,"mes":response.text})
    else:
         return tmp.TemplateResponse('err.html',{'request':request,"mes":"이미 존재하는 아이디나 전화번호 입니다"})
@app.post("/login")
async def index(request:Request,id:str=Form(...),pw:str=Form(...)):
    df=getUserTable()
    rf=df[(df['아이디']==id)&(df['비밀번호']==hashlib.sha256(pw.encode()).hexdigest())]
    if len(rf)==1:
        return tmp.TemplateResponse('user.html',{'request':request,'id':rf.values[0][0],'name':rf.values[0][2],'sex':rf.values[0][3],'year':rf.values[0][4],'month':rf.values[0][5],'day':rf.values[0][6],'ph':rf.values[0][7],'mbti':rf.values[0][8]})
    else:
         return tmp.TemplateResponse('err.html',{'request':request,"mes":"아이디와 비밀번호를 다시 확인해주세요"})