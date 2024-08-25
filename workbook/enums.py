from enum import *


class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class ReservationStatus(BaseEnum):
    IN_PROGRESS = "in progress"
    REJECTED = "rejected"
    COMPLETED = "completed"


class MessageSender(BaseEnum):
    CUSTOMER = "customer"
    WORKER = "worker"


class UserType(BaseEnum):
    CUSTOMER = "customer"
    WORKER = "worker"
