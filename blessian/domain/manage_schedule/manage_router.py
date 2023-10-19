from fastapi import APIRouter

router = APIRouter(
    prefix="/api/manage",
)

@router.get("/hello")
def hello():
    return "Hello World!"