# -*- coding: utf-8 -*-
"""Parsing helpers for dates, results, and normal ranges; plus status/deviation."""
from datetime import datetime
import re


def parse_date(s):
    for fmt in ("%d/%m/%Y %H:%M", "%d-%m-%Y %H:%M:%S", "%d-%m-%Y %H:%M"):
        try:
            return datetime.strptime(s.strip(), fmt)
        except ValueError:
            pass
    return datetime(2000, 1, 1)


def parse_result(v):
    if isinstance(v, (int, float)):
        return float(v)
    m = re.match(r"[<>≤≥]?\s*([\d.]+)", str(v).strip())
    return float(m.group(1)) if m else None


def parse_range(s):
    """Returns (lo, hi). None means unbounded."""
    if not s or s.strip() in ("Not Specified", ""):
        return None, None
    s = s.strip()
    # "X - Y"
    m = re.match(r"^([\d.]+)\s*[-–]\s*([\d.]+)$", s)
    if m:
        return float(m.group(1)), float(m.group(2))
    # "< X" or "<= X"
    m = re.match(r"^[<≤]=?\s*([\d.]+)", s)
    if m:
        return 0.0, float(m.group(1))
    # "> X" or ">= X"
    m = re.match(r"^[>≥]=?\s*([\d.]+)", s)
    if m:
        return float(m.group(1)), None
    # "Up to X"
    m = re.match(r"[Uu]p\s+to\s+([\d.]+)", s)
    if m:
        return 0.0, float(m.group(1))
    # Complex ranges: PCT "Normal: 0.0-0.5, ..." or "Normal < 0.046, ..."
    m = re.search(r"Normal[:\s]+<\s*([\d.]+)", s, re.I)
    if m:
        return 0.0, float(m.group(1))
    m = re.search(r"Normal[:\s]+([\d.]+)\s*[-–]\s*([\d.]+)", s, re.I)
    if m:
        return float(m.group(1)), float(m.group(2))
    # HbA1c "Non diabetic < 5.8, ..."
    m = re.search(r"Non.diabetic\s*<\s*([\d.]+)", s, re.I)
    if m:
        return 0.0, float(m.group(1))
    return None, None


def classify(val, lo, hi):
    if val is None or (lo is None and hi is None):
        return "unknown"
    if lo is not None and val < lo:
        return "low"
    if hi is not None and val > hi:
        return "high"
    return "normal"


def fmt_num(v):
    """Number without trailing zeros so families don't misread 10.00 as 1000.
    10.00->'10', 10.50->'10.5', 0.046 stays '0.046'. '' for None."""
    return f"{float(v):g}" if v is not None else ""


def deviation(val, lo, hi):
    """Fractional distance outside normal range (0 if inside)."""
    if val is None or (lo is None and hi is None):
        return 0.0
    if lo is not None and val < lo and lo != 0:
        return (lo - val) / lo
    if hi is not None and val > hi and hi != 0:
        return (val - hi) / hi
    return 0.0
