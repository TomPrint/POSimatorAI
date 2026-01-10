from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MANAGER = "MANAGER", "Manager"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MANAGER
    )

    def is_admin(self):
        return self.role == self.Role.ADMIN
    
    def save(self, *args, **kwargs):
    # jeśli użytkownik jest adminem, ustaw is_staff = True
        if self.role == self.Role.ADMIN:
            self.is_staff = True
        else:
            # np. manager nie jest staffem
            self.is_staff = False
        super().save(*args, **kwargs)