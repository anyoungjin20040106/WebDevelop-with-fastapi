import numpy as np
result=np.random.randint(1,100)
for i in range(10):
    a=int(input(f"{i+1}회차 숫자를 맞춰보세요(범위 : 1~100)"))
    if a==result:
        print("축하합니다 정답을 맞추셨습니다")
        break
    elif a<result:
        print(f"{a}는 제가 생각한 숫자보다 작습니다")
    elif a<result:
        print(f"{a}는 제가 생각한 숫자보다 큽니다")
if(a!=result):
    print(f"정답은 {result}였습니다")