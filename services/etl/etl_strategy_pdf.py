"""ETL for Services Australia Automation & AI Strategy PDF.

This script downloads the Automation and AI Strategy 2025–27 PDF from
Services Australia, extracts the high-level principle headings, and
writes them to a YAML file for inclusion in rulecards and citations.
Due to the complexity of reliably parsing PDFs, this implementation
focuses on downloading and storing the PDF. Manual extraction of
headings may be performed outside the pipeline and checked into the
repository. The provenance entry in `data/provenance.json` should
record the download timestamp and file path.
"""

import os
from pathlib import Path
import requests
from datetime import datetime
import yaml


STRATEGY_URL = "https://www.servicesaustralia.gov.au/sites/default/files/2025-05/automation-and-ai-strategy-2025-27.pdf"
RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"


def download_pdf() -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path = RAW_DIR / "strategy.pdf"
    if pdf_path.exists():
        return pdf_path
    response = requests.get(STRATEGY_URL, timeout=30)
    response.raise_for_status()
    with open(pdf_path, "wb") as f:
        f.write(response.content)
    return pdf_path


def extract_principles(pdf_path: Path) -> list[str]:
    """
    Placeholder for PDF parsing logic. In a full implementation,
    use pdfminer.six to extract headings matching principles or
    guardrails. For now, return an empty list.
    """
    # TODO: implement with pdfminer.six if necessary
    return []


def write_yaml(principles: list[str]) -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    yaml_path = PROCESSED_DIR / "strategy_principles.yaml"
    with open(yaml_path, "w") as f:
        yaml.safe_dump({"principles": principles}, f)


def main():
    pdf_path = download_pdf()
    principles = extract_principles(pdf_path)
    write_yaml(principles)
    print(f"Downloaded strategy PDF to {pdf_path} and extracted {len(principles)} principles")


if __name__ == "__main__":
    main()