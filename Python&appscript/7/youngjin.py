class Unit:
    def __init__(self, name: str, hp: int, atk: int) -> None:
        self.name = name
        self.hp = hp
        self.atk = atk

    def dil(self, unit: 'Unit'):
        print(f"{self.name}(이)가 {unit.name}한테 피해를 입었다")
        self.hp -= unit.atk
        if self.hp <= 0:
            self.hp=0
            print(f"{self.name}은 쓰러졌다")
    @property
    def isDie(self):
        return self.hp==0
def title():
    return "스타크래프트 2"
