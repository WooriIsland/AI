from fastapi import FastAPI

from domain.manage_schedule import manage_router
from domain.recommand_event import recommand_router

app = FastAPI()

app.include_router(manage_router.router)
app.include_router(recommand_router.router)