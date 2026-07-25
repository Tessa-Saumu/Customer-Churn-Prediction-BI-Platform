"""
generate_model_comparison_csv.py

Reads Latifah's evaluation/model_comparison.md (Issue #11 deliverable) and
produces evaluation/model_comparison.csv for Power BI consumption (Issue #12).

This script does not modify model_comparison.md. It only reads it.
Re-run this any time model_comparison.md changes upstream.
"""
import re
import csv
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

SOURCE_MD = Path("evaluation/model_comparison.md")
OUTPUT_CSV = Path("evaluation/model_comparison.csv")


def parse_confusion_matrix(raw: str) -> tuple[int, int, int, int]:
    """Parses '[[973, 62], [54, 320]]' -> (TN, FP, FN, TP)."""
    nums = [int(n) for n in re.findall(r"-?\d+", raw)]
    if len(nums) != 4:
        raise ValueError(f"Expected 4 values in confusion matrix, got: {raw}")
    tn, fp, fn, tp = nums
    return tn, fp, fn, tp


def parse_table(md_text: str) -> list[dict[str, str]]:
    """Extracts the markdown comparison table rows into row dicts."""
    lines = [l for l in md_text.splitlines() if l.strip().startswith("|")]
    if len(lines) < 3:
        raise ValueError("Could not find a markdown table with data rows.")

    header_cells = [c.strip() for c in lines[0].strip("|").split("|")]
    data_lines = lines[2:]  # skip header + separator row

    rows = []
    for line in data_lines:
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != len(header_cells):
            logger.warning("Skipping malformed row: %s", line)
            continue
        rows.append(dict(zip(header_cells, cells)))
    return rows


def build_csv_rows(table_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    out = []
    for row in table_rows:
        tn, fp, fn, tp = parse_confusion_matrix(row["confusion_matrix"])
        out.append({
            "Model": row["model_name"],
            "Accuracy": row["accuracy"],
            "Precision": row["precision"],
            "Recall": row["recall"],
            "ROC_AUC": row["roc_auc"],
            "True_Negatives": tn,
            "False_Positives": fp,
            "False_Negatives": fn,
            "True_Positives": tp,
        })
    return out


def main() -> None:
    if not SOURCE_MD.exists():
        raise FileNotFoundError(f"{SOURCE_MD} not found. Run this from the repo root.")

    md_text = SOURCE_MD.read_text(encoding="utf-8")
    table_rows = parse_table(md_text)
    csv_rows = build_csv_rows(table_rows)

    if not csv_rows:
        raise ValueError("No rows parsed from model_comparison.md — refusing to write an empty CSV.")

    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
        writer.writeheader()
        writer.writerows(csv_rows)

    logger.info("Wrote %d rows to %s", len(csv_rows), OUTPUT_CSV)


if __name__ == "__main__":
    main()