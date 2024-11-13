from domain.services.entity_service import EntityService
from infrastructure.db.models import Reward


class RewardServiceInterface(EntityService[Reward]): ...
