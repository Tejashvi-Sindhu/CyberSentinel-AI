"""Safe CSV upload helpers."""
from pathlib import Path
from io import BytesIO
import pandas as pd

class DataValidationError(ValueError):
    """Raised when a CSV upload is invalid."""

def validate_filename(name: str) -> None:
    if not name or Path(str(name)).name != str(name) or Path(name).suffix.lower() != ".csv":
        raise DataValidationError("Please provide a plain .csv filename.")

def read_csv_safe(source, max_bytes: int = 250 * 1024 * 1024) -> pd.DataFrame:
    validate_filename(Path(str(getattr(source, "name", "upload.csv"))).name)
    try:
        if hasattr(source, "getvalue"):
            raw = source.getvalue()
            if len(raw) > max_bytes:
                raise DataValidationError("CSV exceeds the 250 MB upload limit.")
            df = pd.read_csv(BytesIO(raw), low_memory=False)
        else:
            df = pd.read_csv(source, low_memory=False)
    except DataValidationError:
        raise
    except Exception as exc:
        raise DataValidationError(f"Could not parse CSV: {exc}") from exc
    if df.empty:
        raise DataValidationError("The CSV contains no data rows.")
    df.columns = [str(c).strip() for c in df.columns]
    if df.columns.duplicated().any():
        raise DataValidationError("The CSV has duplicate column names.")
    return df
