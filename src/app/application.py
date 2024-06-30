from fastapi import FastAPI

from src.app.views.v1.accounts import router as accounts_routers
from src.app.views.v1.books import router as books_routers
from src.app.views.v1.novelists import router as novelists_routers
from src.config.app.application import settings


class App(FastAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args,
            **kwargs,
            title=settings.PROJECT_TITLE,
            version=settings.PROJECT_VERSION,
        )
        self._include_routers()

    def _include_routers(self) -> None:
        self.include_router(accounts_routers)
        self.include_router(books_routers)
        self.include_router(novelists_routers)


app = App()
