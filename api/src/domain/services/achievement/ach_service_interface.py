from domain.services.entity_service import EntityService
from infrastructure.db.models import Achievement


class AchievementServiceInterface(EntityService[Achievement]): ...
