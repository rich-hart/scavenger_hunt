from django.db import models
from django.contrib.auth.models import User
from hunt.models import Base

class Profile(Base):
    """
    A project specific class for user info.
    """
    # NOTE Try not to overwrite User class. 
    # Use Profile instead
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='owner',
    )
    nick_name = models.CharField(max_length=2**6)
    def __str__(self):
        return '%s: %s %s' % (
            str(self.user.pk),
            self.user.first_name,
            self.user.last_name
        )


