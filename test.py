from pydantic import BaseModel

class X(BaseModel):
    a: int

print(X(a=5))
