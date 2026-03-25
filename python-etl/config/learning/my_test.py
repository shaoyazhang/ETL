# def add(a:float, b:float) -> float:
#     return a + b

import json


class Person:
    def __init__(self, name: str, age: int, address: str):
        self.name = name
        self.age = age
        self.address = address

    def to_csv(self, sep: str = ',') -> str:
        return f'{self.name}{sep}{self.age}{sep}{self.address}'
    
    def to_sql(self):
        return f"INSERT INTO person VALUES ('{self.name}', {self.age}, '{self.address}');"
    
jstr = """{"name": "Alice", "age": 30, "address": "123 Main St"}"""   
d = json.loads(jstr)
p1 = Person(d['name'], d['age'], d['address'])
print(p1.to_csv())  # 输出: Alice,30,123 Main St   
print(p1.to_sql())  # 输出: INSERT INTO person VALUES ('Alice', 30, '123 Main St'); 