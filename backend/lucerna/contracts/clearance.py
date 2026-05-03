from __future__ import annotations

_HEADER_NAME = "HTTP_X_LUCERNA_CLEARANCE"

_LABEL_TO_INT = {
    "unclassified": 0,
    "confidential": 1,
    "secret": 2,
    "top_secret": 3,
}

_INT_TO_LABEL = {v: k for k, v in _LABEL_TO_INT.items()}


def clearance_from_header(meta: dict) -> int | None:
    raw = meta.get(_HEADER_NAME)
    if raw is None:
        return None
    key = str(raw).strip().lower().replace(" ", "_")
    if key == "top secret":
        key = "top_secret"
    return _LABEL_TO_INT.get(key)


def clearance_label(value: int) -> str:
    return _INT_TO_LABEL.get(value, "unclassified")


def max_clearance_for_user(user) -> int | None:
    if user is None or not getattr(user, "is_authenticated", False):
        return None
    return int(getattr(user, "clearance_level", 0))
