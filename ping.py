from fastapi import APIRouter

router = APIRouter(
    prefix="/ping",
    tags=["PING"],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
async def ping():
    return {"message": "Pong!"}
