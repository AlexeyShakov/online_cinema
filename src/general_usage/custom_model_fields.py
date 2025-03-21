from sqlalchemy import types
from datetime import datetime, timezone

from typing import Any


class DateTimeWithTZ(types.TypeDecorator):
    """Custom DateTime type for proper ISO 8601 format and timezone handling."""
    impl = types.Text

    def process_bind_param(self, value: Any, dialect: Any) -> Any:
        """Convert datetime object to ISO format string before inserting into DB."""
        if value is None:
            return None
        if isinstance(value, str):
            return value
        if isinstance(value, datetime):
            if value.tzinfo is None:
                value = value.replace(tzinfo=timezone.utc)  # Ensure UTC timezone
            return value.strftime("%Y-%m-%d %H:%M:%S.%f+00")  # Convert to DB format
        raise TypeError("Invalid type for DateTimeWithTZ. Expected datetime or string.")

    def process_result_value(self, value: Any, dialect: Any) -> Any:
        """Convert stored string back to datetime object with timezone."""
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f+00").replace(tzinfo=timezone.utc)
        raise TypeError("Invalid type for DateTimeWithTZ. Expected string or datetime.")