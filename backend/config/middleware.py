from __future__ import annotations

from django.conf import settings
from django.db import connection, transaction

from contracts.clearance import clearance_from_header, max_clearance_for_user


class RequestClearanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_level = max_clearance_for_user(getattr(request, "user", None))
        header_level = clearance_from_header(request.META)
        if getattr(request.user, "is_authenticated", False) and user_level is not None:
            request.clearance_level = int(user_level)
        elif header_level is not None:
            request.clearance_level = int(header_level)
        else:
            request.clearance_level = int(getattr(settings, "LUCERNA_DEFAULT_CLEARANCE", 2))
        return self.get_response(request)


class PostgresRlsMiddleware:
    """
    Runs each request inside atomic() and sets a transaction-local GUC for RLS policies.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if connection.vendor != "postgresql":
            return self.get_response(request)

        clearance = int(getattr(request, "clearance_level", 0))
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT set_config('lucerna.clearance_level', %s, true)",
                    [str(clearance)],
                )
            response = self.get_response(request)
            if response.status_code >= 400:
                transaction.set_rollback(True)
            return response
