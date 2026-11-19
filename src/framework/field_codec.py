"""Decode the JSON inside /soccer/field_info's std_msgs/String.data."""

from __future__ import annotations

import json
import math
from dataclasses import fields

from .types import FieldDimensions


def field_dimensions_from_json(data: str) -> FieldDimensions:
    try:
        payload = json.loads(data)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid field info JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("field info JSON must be an object")
    version = payload.get("schema_version")
    if type(version) is not int or version != 1:
        raise ValueError("field info schema_version must be 1")
    dimensions = payload.get("dimensions")
    if not isinstance(dimensions, dict):
        raise ValueError("field info dimensions must be an object")

    values = {}
    for item in fields(FieldDimensions):
        value = dimensions.get(item.name)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"dimensions.{item.name} must be a number")
        try:
            number = float(value)
        except OverflowError as exc:
            raise ValueError(f"dimensions.{item.name} is too large") from exc
        if not math.isfinite(number) or number <= 0.0:
            raise ValueError(f"dimensions.{item.name} must be finite and positive")
        values[item.name] = number
    return FieldDimensions(**values)
