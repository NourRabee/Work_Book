from enum import *


class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class ReservationStatus(BaseEnum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"
    IN_PROGRESS = "IN PROGRESS"
    COMPLETED = "COMPLETED"


class MessageSender(BaseEnum):
    CUSTOMER = "CUSTOMER"
    WORKER = "WORKER"


class UserType(BaseEnum):
    CUSTOMER = "CUSTOMER"
    WORKER = "WORKER"
