from enum import *


class ReservationStatus(Enum):
    IN_PROGRESS = "in progress"
    REJECTED = "rejected"
    COMPLETED = "completed"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class MessageSender(Enum):
    CUSTOMER = "customer"
    WORKER = "worker"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class UserType(Enum):
    CUSTOMER = "customer"
    WORKER = "worker"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
