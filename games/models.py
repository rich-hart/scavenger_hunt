from django.db import models
from users.models import Profile
from hunt.models import Base

class Player(Base):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
    )

