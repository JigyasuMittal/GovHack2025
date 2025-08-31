"""ETL for rulecards.

Rulecards define the steps users should follow for different intents.
This script reads the YAML file at the repository root, converts it
to JSON for storage, writes a processed CSV, and loads the data into
the `rulecards` table.
"""

import os
from pathlib import Path
import yaml
import pandas as pd
from sqlalchemy.orm import Session

from ..api.database import engine
from ..api.models import Rulecard


RAW_FILE = Path(__file__).resolve().parents[2] / "rulecards.yaml"
PROCESSED_FILE = Path(__file__).resolve().parents[2] / "data" / "processed" / "rulecards.csv"


def load_raw() -> dict:
    with open(RAW_FILE, "r") as f:
        return yaml.safe_load(f)


def transform(data: dict) -> pd.DataFrame:
    records = []
    for intent, content in data.items():
        record = {
            "intent": intent,
            "description": content.get("description"),
            "yaml_json": content,  # store full structure in JSON field
        }
        records.append(record)
    return pd.DataFrame(records)


def write_processed(df: pd.DataFrame) -> None:
    PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_FILE, index=False)


def load_to_db(df: pd.DataFrame) -> None:
    with engine.begin() as conn:
        conn.execute(Rulecard.__table__.delete())
        conn.execute(Rulecard.__table__.insert(), df.to_dict(orient="records"))


def main():
    data = load_raw()
    df = transform(data)
    write_processed(df)
    load_to_db(df)
    print(f"Loaded {len(df)} rulecards")


if __name__ == "__main__":
    main()