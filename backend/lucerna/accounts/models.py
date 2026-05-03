from django.contrib.auth.models import AbstractUser
from django.db import models


class Clearance(models.IntegerChoices):
    UNCLASSIFIED = 0, "unclassified"
    CONFIDENTIAL = 1, "confidential"
    SECRET = 2, "secret"
    TOP_SECRET = 3, "top_secret"


class LucernaUser(AbstractUser):
    clearance_level = models.PositiveSmallIntegerField(
        choices=Clearance.choices,
        default=Clearance.UNCLASSIFIED,
        help_text="Highest compartment this user may read/write (RLS + API).",
    )

    class Meta:
        db_table = "accounts_user"
