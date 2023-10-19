from fastapi import APIRouter

router = APIRouter(
    prefix="/api/recommand",
)

@router.get("/hello")
def hello():
    return "Hello World!"