from fastapi import FastAPI,Request,Form
from fastapi.responses import HTMLResponse,FileResponse
from fastapi.templating import Jinja2Templates
tmp=Jinja2Templates(directory="templates")#templates폴더를 가져온다
app=FastAPI()
@app.get("/")
def index():
    return HTMLResponse("<h1>이건 파이썬과 HTML을 합친 사이트</h1>")
@app.get("/file")
def index():
    return FileResponse("index.html")
@app.get("/form")
def index():
    return FileResponse("Form.html")
@app.post("/result")
def index(request:Request,name:str=Form(...),sex:str=Form(...)):
    return tmp.TemplateResponse("result.html",{"request":request,#templates안에 있는 result.html을 가져온다
                                               "n":name,
                                               "sex":sex})
#시작 명령어 : uvicorn 파일명(main):Fastapi클래스명(app) --reload