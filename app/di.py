from typing import Any, Awaitable, Callable, ParamSpec, TypeVar
from contextvars import ContextVar
from dishka import AsyncContainer, Container, Scope
from dishka.integrations.base import wrap_injection
from telegram.ext import Application, CallbackContext, SimpleUpdateProcessor


CONTAINER_NAME = "dishka_container"


T = TypeVar("T")
P = ParamSpec("P")


def _get_container_from_context(context: CallbackContext) -> AsyncContainer:
    update_processor: ContainerUpdateProcessor = context._application._update_processor
    return update_processor.update_container.get()


def inject(func: Callable[P, T]) -> Callable[P, T]:
    return wrap_injection(
        func=func,
        is_async=True,
        container_getter=lambda args, _: _get_container_from_context(args[1]),
    )


class ContainerUpdateProcessor(SimpleUpdateProcessor):
    __slots__ = ("container", "update_container")

    def __init__(self, container: Container, max_concurrent_updates: int):
        super().__init__(max_concurrent_updates)
        self.container = container
        self.update_container = ContextVar(CONTAINER_NAME)

    async def do_process_update(
        self,
        update: object,
        coroutine: "Awaitable[Any]",
    ) -> None:
        async with self.container(scope=Scope.REQUEST) as update_container:
            token = self.update_container.set(update_container)
            await super().do_process_update(update, coroutine)
            self.update_container.reset(token)


def setup_dishka(container: Container, app: Application):
    app._update_processor = ContainerUpdateProcessor(container, max_concurrent_updates=1)
