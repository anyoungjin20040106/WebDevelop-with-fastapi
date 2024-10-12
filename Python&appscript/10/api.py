from fastapi import FastAPI,Form

app=FastAPI()
@app.post("/")
def index(r:str=Form(...)):
    try:
        r=float(r)
        return f"반지름은 : {r**2}π 입니다"
    except Exception as e:
        return f"에러 : {e}"
        