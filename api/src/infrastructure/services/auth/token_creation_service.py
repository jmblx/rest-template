from datetime import timedelta

from application.auth.services.token_creation import TokenCreationService
from application.auth.token_types import AccessToken, RefreshTokenData
from domain.entities.user.model import User
from domain.services.auth.jwt_service import JWTService
from uuid import uuid4

from infrastructure.services.auth.config import JWTSettings


class TokenCreationServiceImpl(TokenCreationService):
    """Реализация сервиса создания токенов с использованием JWTService."""

    def __init__(self, jwt_settings: JWTSettings, jwt_service: JWTService):
        self.jwt_service = jwt_service
        self.jwt_settings = jwt_settings

    def create_access_token(self, user: User) -> AccessToken:
        jwt_payload = {
            "sub": str(user.id),
            "email": user.email.value,
            "role_id": user.role_id.value,
        }
        encoded_token = self.jwt_service.encode(
            payload=jwt_payload,
            expire_minutes=self.jwt_settings.access_token_expire_minutes,
        )
        return AccessToken(encoded_token["token"])

    async def create_refresh_token(
        self, user: User, fingerprint: str
    ) -> RefreshTokenData:
        jti = str(uuid4())
        jwt_payload = {"sub": str(user.id), "jti": jti}
        encoded_token = self.jwt_service.encode(
            payload=jwt_payload,
            expire_timedelta=timedelta(
                days=self.jwt_settings.refresh_token_expire_days
            ),
        )
        refresh_token_data = RefreshTokenData(
            token=encoded_token["token"],
            user_id=user.id,
            jti=jti,
            fingerprint=fingerprint,
            created_at=encoded_token["created_at"],
        )
        return refresh_token_data
