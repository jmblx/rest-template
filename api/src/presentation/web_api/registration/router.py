from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from domain.services.user.user_service_interface import UserServiceInterface
from presentation.web_api.registration.schemas import UserRegistration, UserLogin

router = APIRouter(route_class=DishkaRoute, tags=["reg", "auth"])


@router.post("/user")
async def registration(data: UserRegistration, user_service: FromDishka[UserServiceInterface], login_data: FromDishka[UserLogin]) -> str:
    combined_data = {**data.dict(), **login_data.dict()}
    return await user_service.create_user_with_achievements(combined_data)
