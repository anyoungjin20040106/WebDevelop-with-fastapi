from fastapi import FastAPI,Form,Request
from fastapi.responses import FileResponse,HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
app=FastAPI()
tmp=Jinja2Templates(directory="./tmp")
@app.get("/")
def index():
    return FileResponse("index.html")
@app.post("/result")
def index(request:Request,id:str=Form(...),pw:str=Form(...)):
    msg=""
    df=pd.read_csv("gamedata.csv")
    rf=df[(df['아이디']==id)&(df['비밀번호']==pw)]
    
    if bool(len(rf)):
        return tmp.TemplateResponse("info.html",{"request":request,"id":id,"pw":pw,"tier":rf['티어'].values[0]})
    else:
        return tmp.TemplateResponse("tmp.html",{"request":request,"msg":"로그인 실패 아이디나 비밀번호를 확인하세요"})
@app.get("/admincheck")
def index():
    return FileResponse("admin.html")
@app.post("/admin")
def index(request:Request,pw=Form(...)):
    if pw=="123":
        df=pd.read_csv("gamedata.csv")
        return HTMLResponse(df.to_html(index=False))
    else:
        return tmp.TemplateResponse("tmp.html",{"request":request,"msg":"비밀번호를 확인하세요"})