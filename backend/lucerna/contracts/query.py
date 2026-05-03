from __future__ import annotations

from django.db import connection
from django.db.models import QuerySet


def apply_clearance(qs: QuerySet, clearance_level: int) -> QuerySet:
    """
    When not using PostgreSQL RLS, enforce the same visibility rule in the ORM.
    """
    if connection.vendor == "postgresql":
        return qs
    return qs.filter(clearance_required__lte=clearance_level)
