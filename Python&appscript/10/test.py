from fastapi import FastAPI,Form
import hashlib
from fastapi.responses import HTMLResponse,FileResponse

app=FastAPI()
@app.get("/")
def index():
    return FileResponse("test.html")
@app.post("/result")
def index(id:str=Form(...),pw:str=Form(...)):
    return HTMLResponse(f"""
아이디 : {id}<br>
비밀번호 : {hashlib.sha224(pw.encode()).hexdigest()}""")

