# Installation
`poetry add git+https://github.com/SeniorK0tik/middleware_cls_decorator.git`

# Examples
Перед каждым вызовом метода класса будет происходить вызов `func_pre`
```python

def log_cls_methods(func: object, *args) -> None:
    logger.debug(
        f"{func.__name__} LOGGED")


@deco_cls_methods(
    func_pre=log_cls_methods
)
class TargetModel:
    async def do_first(self):
        ...
    
    async def do_second(self):
        ...
```