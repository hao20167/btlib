# v
import os
from typing import List, Dict, Any

import pandas as pd
from dateutil import parser as date_parser

REQUIRED_CORE_COLUMNS = [
    "datetime",
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
]


class ValidationError(Exception):
    pass


def _check_required_columns(df: pd.DataFrame) -> List[str]:
    return [c for c in REQUIRED_CORE_COLUMNS if c not in df.columns]


def _check_datetime_parseable(df: pd.DataFrame) -> bool:
    try:
        sample = df["datetime"].head(50)
        _ = sample.apply(lambda x: date_parser.parse(str(x)))
        return True
    except Exception:
        return False


def _check_numeric(df: pd.DataFrame) -> List[str]:
    numeric_cols = ["Open", "High", "Low", "Close", "Volume"]
    bad = []
    for col in numeric_cols:
        try:
            _ = pd.to_numeric(df[col].head(50), errors="raise")
        except Exception:
            bad.append(col)
    return bad


def _check_sorted(df: pd.DataFrame) -> bool:
    ts = pd.to_datetime(df["datetime"])
    return ts.is_monotonic_increasing


def _check_ohlc_logic(df: pd.DataFrame) -> int:
    o = df["Open"].astype(float)
    h = df["High"].astype(float)
    l = df["Low"].astype(float)
    c = df["Close"].astype(float)
    max_oc = pd.concat([o, c], axis=1).max(axis=1)
    min_oc = pd.concat([o, c], axis=1).min(axis=1)
    bad_high = h < max_oc
    bad_low = l > min_oc
    return int((bad_high | bad_low).sum())


def _check_negative(df: pd.DataFrame) -> int:
    numeric_cols = ["Open", "High", "Low", "Close", "Volume"]
    cnt = 0
    for col in numeric_cols:
        cnt += int((df[col].astype(float) < 0).sum())
    return cnt


def _nan_ratio(df: pd.DataFrame) -> float:
    return float(df.isna().sum().sum()) / float(df.size)


def validate_dataframe(df: pd.DataFrame, strict: bool = True) -> Dict[str, Any]:
    report: Dict[str, Any] = {"ok": True, "errors": [], "warnings": [], "nan_ratio": 0.0}

    missing = _check_required_columns(df)
    if missing:
        report["errors"].append(f"Missing columns: {missing}")

    if "datetime" in df.columns and not _check_datetime_parseable(df):
        report["errors"].append("Column 'datetime' not parseable as datetime.")

    if all(c in df.columns for c in ["Open", "High", "Low", "Close", "Volume"]):
        bad_numeric = _check_numeric(df)
        if bad_numeric:
            report["errors"].append(f"Non-numeric OHLCV columns: {bad_numeric}")

    if "datetime" in df.columns and not _check_sorted(df):
        report["warnings"].append("Datetimes are not sorted ascending.")

    try:
        bad_ohlc = _check_ohlc_logic(df)
        if bad_ohlc > 0:
            report["warnings"].append(
                f"{bad_ohlc} rows violate OHLC logic (High < max(Open, Close) or Low > min(Open, Close))."
            )
    except Exception:
        pass

    try:
        negatives = _check_negative(df)
        if negatives > 0:
            report["warnings"].append(f"Found {negatives} negative values in OHLCV.")
    except Exception:
        pass

    nan_ratio = _nan_ratio(df)
    report["nan_ratio"] = nan_ratio
    if nan_ratio > 0.1:
        report["warnings"].append(f"NaN ratio is high ({nan_ratio:.2%}).")

    if report["errors"]:
        report["ok"] = False
        if strict:
            print(df.head(10))
            raise ValidationError("Invalid input data: " + "; ".join(report["errors"]))

    return report


def validate_input_file(path: str, strict: bool = True) -> Dict[str, Any]:
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    df = pd.read_csv(path)
    return validate_dataframe(df, strict=strict)
