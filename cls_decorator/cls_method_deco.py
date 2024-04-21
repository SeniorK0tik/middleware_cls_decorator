from __future__ import annotations

import inspect
from functools import wraps
from typing import Any, AsyncGenerator, Callable, Tuple



def deco_cls_methods(  # noqa: C901
        func_pre: Callable | None = None,
        func_post: Callable | None = None,
        exception_methods_names: Tuple = ()

) -> Callable:
    """
    Оборачивает все пользовательские методы класса

    func_pre: Функция перед выполнением метода класса
    func_post: Функция после выполнением метода класса
    exception_methods_names: Имена методов исключений
    """
    def decorator(cls: object) -> object:  # noqa: C901
        @wraps(cls, updated=())
        class MiddlewareClass(cls):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)

            def __getattribute__(self, name: str) -> Callable:  # noqa: C901
                if name in exception_methods_names:
                    return super().__getattribute__(name)

                attr = super().__getattribute__(name)
                if callable(attr):
                    if inspect.iscoroutinefunction(attr):
                        async def wrapper(*args, **kwargs) -> Any:
                            func_pre(attr, args, kwargs) if func_pre else None
                            result = await attr(*args, **kwargs)
                            func_post(attr, args, kwargs) if func_post else None
                            return result

                    elif inspect.isasyncgenfunction(attr):
                        async def wrapper(*args, **kwargs) -> Any:
                            func_pre(attr, args, kwargs) if func_pre else None
                            async for item in attr(*args, **kwargs):
                                yield item
                            func_post(attr, args, kwargs) if func_post else None

                    elif inspect.isgeneratorfunction(attr):
                        def wrapper(*args, **kwargs) -> AsyncGenerator[Any, Any]:
                            func_pre(attr, args, kwargs) if func_pre else None
                            for item in attr(*args, **kwargs):
                                yield item
                            func_post(attr, args, kwargs) if func_post else None

                    else:
                        def wrapper(*args, **kwargs) -> Any:
                            func_pre(attr, args, kwargs) if func_pre else None
                            result = attr(*args, **kwargs)
                            func_post(attr, args, kwargs) if func_post else None
                            return result
                    return wrapper

                return attr
        return MiddlewareClass
    return decorator
