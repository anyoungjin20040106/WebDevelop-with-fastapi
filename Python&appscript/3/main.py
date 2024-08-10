x=1
isSuccess=False
while True:
    y=0
    while x<=y:
        print(f"{x}+{y}={x+y}")
        if x**2+100*y==500:
            isSuccess=True
            break
        y+=1
    if isSuccess:
        break
    else:
        x+=1
x,y