import pandas as pd
from fastapi import FastAPI, UploadFile, Request, Form,Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
import hashlib
from datetime import datetime
import os

class GoogleSheet:
    @classmethod
    def GetBorder(cls):
        return pd.read_excel("https://docs.google.com/spreadsheets/d/1Qbs9FZqxnojF2BLyN_O_0_A4gR1i19aMpZMwyhBAsZA/export?format=xlsx")

    @classmethod
    def GetAppscript(cls):
        return "https://script.google.com/macros/s/AKfycbzRFTNSD9IouXDcwQU5IIrxSC7ukRtA7QDI-O9FE32srX2NAL09wB0zveSPqV6Agl6WcQ/exec"

# FastAPI 앱 초기화
app = FastAPI()

# 정적 파일 경로 설정
app.mount("/img", StaticFiles(directory="img"), name="img")

# 템플릿 설정
tmp = Jinja2Templates(directory="tmp")

def MakeDeleteBtn(id):
    return (f'''
    <form action="/delete" method="post" onsubmit="return passwordCheck('d{id}')">
        <input type="hidden" name="id" value="{id}">
        <input type="hidden" name="pw" id="pw_d{id}">
        <button type="submit">삭제하기</button>
    </form>
''').replace("\n","")
def MakeUpdateBtn(id):
    return f'''
    <form action="/updateform" method="post" onsubmit="return passwordCheck('u{id}')">
        <input type="hidden" name="id" value="u{id}">
        <input type="hidden" name="pw" id="pw_{id}">
        <button type="submit">수정하기</button>
    </form>'''.replace("\n","")
def MakeShowBtn(id):
    return f'''
<button onclick="window.location.href='/content?id={id}'">사진보기</button>
'''.replace("\n","")
# 메인 페이지 엔드포인트
@app.get("/")
def index(request: Request):
    df=GoogleSheet.GetBorder()
    df['사진보기']=df['아이디'].apply(MakeShowBtn)
    df['삭제하기']=df['아이디'].apply(MakeDeleteBtn)
    df['수정하기']=df['아이디'].apply(MakeUpdateBtn)
    df=df[['제목','닉네임','올린 날짜','사진보기','수정하기','삭제하기']]
    return tmp.TemplateResponse("index.html", {"request": request, "board": df.to_html(index=False,escape=False)})

# 업로드 폼 페이지 엔드포인트
@app.get("/uploadform")
def uploadform():
    return FileResponse("upload.html")

# 파일 업로드 처리 엔드포인트
@app.post("/upload")
async def upload(request: Request, title: str = Form(...), name: str = Form(...), img: UploadFile = Form(...), pw: str = Form(...)):
    df = GoogleSheet.GetBorder()
    if len(df) == 0:
        id = 1
    else:
        id = df['아이디'].values[-1] + 1

    # 파일 저장 경로 설정
    ext = img.filename.split('.')[-1]
    filename = f"{id}.{ext}"
    save_path = os.path.join("img", filename)

    # 파일 저장
    with open(save_path, "wb") as file:
        file.write(await img.read())

    # Google Apps Script에 데이터 추가 요청
    async with httpx.AsyncClient() as web:
        response = await web.post(GoogleSheet.GetAppscript(), data={
            "method": "append",
            "id": id,
            "pw":hashlib.sha384(pw.encode()).hexdigest(),
            "title": title,
            "name": name,
            "date": datetime.today().strftime("%Y-%m-%d"),
            "ext":ext
        })

    # 템플릿 응답 반환
    return tmp.TemplateResponse("alert.html", {'request': request, "msg": response.text})

@app.get("/content")
def content(request: Request,id:int=Query(...)):
    df = GoogleSheet.GetBorder()
    df=df[df['아이디']==id]
    if len(df)>0:
        return tmp.TemplateResponse('content.html',{'request':request,"title":df['제목'].values[0],"name":df['닉네임'].values[0], "id":id,"ext":df['확장자'].values[0]})
# 파일 업로드 처리 엔드포인트
@app.post("/update")
async def update(request: Request, id:int=Form(...),title: str = Form(...), name: str = Form(...), img: UploadFile = Form(...), pw: str = Form(...)):
    # 파일 저장 경로 설정
    ext = img.filename.split('.')[-1]
    filename = f"{id}.{ext}"
    save_path = os.path.join("img", filename)
    existing_files = os.listdir("img")
    for file in existing_files:
        if file.startswith(f"{id}."):
            os.remove(os.path.join("img", file))
        # 파일 저장
        with open(save_path, "wb") as file:
            file.write(await img.read())

    # Google Apps Script에 데이터 추가 요청
    async with httpx.AsyncClient() as web:
        response = await web.post(GoogleSheet.GetAppscript(), data={
            "method": "update",
            "id": id,
            "pw": hashlib.sha384(pw.encode()).hexdigest(),
            "title": title,
            "name": name,
            "ext":ext
        })

    # 템플릿 응답 반환
    return tmp.TemplateResponse("alert.html", {'request': request, "msg": response.text})
# 업로드 폼 페이지 엔드포인트
@app.post("/updateform")
def uploadform(request:Request,id:str=Form(...),pw:str=Form(...)):
    df=GoogleSheet.GetBorder()
    df=df[(df['아이디']==int(id))&(df['비밀번호']==hashlib.sha384(pw.encode()).hexdigest())]
    print(len(df))
    if len(df)==1:
        return tmp.TemplateResponse("update.html",{'request': request, "id": id,'title':df['제목'].values[0],'name':df['닉네임'].values[0]})
    else:
        return tmp.TemplateResponse("alert.html",{'request': request,'msg':'비밀번호가 틀렸습니다'})
#파일 삭제 앤드포인트
@app.post("/delete")
async def update(request: Request, id:str|int=Form(...),pw: str = Form(...)):
    df=GoogleSheet.GetBorder()
    df=df[(df['아이디']==int(id))&(df['비밀번호']==hashlib.sha384(pw.encode()).hexdigest())]
    result=""
    if len(df)==1:
        async with httpx.AsyncClient() as web:
            response = await web.post(GoogleSheet.GetAppscript(), data={
                "method": "delete",
                "id": id,
                "pw": hashlib.sha384(pw.encode()).hexdigest(),
            })
        os.remove(f"img/{id}.{df['확장자'].values[0]}")
        result=response.text
    else:
        result="비밀번호가 틀렸습니다"
    # 템플릿 응답 반환
    return tmp.TemplateResponse("alert.html", {'request': request, "msg":result})