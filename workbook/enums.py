from enum import *


class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class ReservationStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"
    IN_PROGRESS = "IN PROGRESS"
    COMPLETED = "COMPLETED"


class MessageSender(Enum):
    CUSTOMER = "CUSTOMER"
    WORKER = "WORKER"


class UserType(Enum):
    CUSTOMER = "CUSTOMER"
    WORKER = "WORKER"
