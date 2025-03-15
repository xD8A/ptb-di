import random
from typing import Iterable
from dishka import Provider, Scope, provide


# app dependency logic
class MyProvider(Provider):
    @provide(scope=Scope.APP)
    def get_int(self) -> Iterable[int]:
        print("solve int")
        yield random.randint(0, 10000)
