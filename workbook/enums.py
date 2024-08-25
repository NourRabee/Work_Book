from enum import *


class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class ReservationStatus(BaseEnum):
    IN_PROGRESS = "IN_PROGRESS"
    REJECTED = "REJECTED"
    COMPLETED = "COMPLETED"


class MessageSender(BaseEnum):
    CUSTOMER = "CUSTOMER"
    WORKER = "WORKER"


class UserType(BaseEnum):
    CUSTOMER = "CUSTOMER"
    WORKER = "WORKER"
