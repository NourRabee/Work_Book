from enum import *


class ReservationStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class MessageSender(Enum):
    CUSTOMER = "CUSTOMER"
    WORKER = "WORKER"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class UserType(Enum):
    CUSTOMER = "CUSTOMER"
    WORKER = "WORKER"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
