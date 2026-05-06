import argparse
import logging
import sys
import time
from typing import List

import pandas as pd

from pipeline.loaders import load_all_datasets
from pipeline.reconstruction import reconstruct_record
from pipeline.enrichment import enrich_record
from pipeline.normalization import normalize_dataset
from pipeline.cleaning import clean_dataset
from pipeline.output import save_json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  [%(levelname)s]  %(name)s — %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("pipeline.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger("negarit.main")

def run_reconstruction_stage(df: pd.DataFrame) -> List[dict]:
    records = df.to_dict(orient="records")
    reconstructed = []
    for rec in records:
        reconstructed.append(reconstruct_record(rec))
    logger.info("Reconstruction complete — %d records", len(reconstructed))
    return reconstructed


def run_enrichment_stage(records: List[dict]) -> List[dict]:
    enriched = [enrich_record(r) for r in records]
    logger.info("Enrichment complete — %d records", len(enriched))
    return enriched

def run_pipeline(dataset_paths: dict, output_path: str) -> List[dict]:
    df = load_all_datasets(dataset_paths)
    logger.info("Loaded %d total rows across all datasets", len(df))
    print(f"  Records loaded: {len(df):,}")

    records = run_reconstruction_stage(df)

    records = run_enrichment_stage(records)

    records = normalize_dataset(records)
    print(f"  Records normalized: {len(records):,}")

    records = clean_dataset(records)
    print(f"  Records after cleaning: {len(records):,}")

    save_json(records, output_path)
    
    return records


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Negarit Dataset Pipeline",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--rc", "--resume-classification",
        dest="resume_classification",
        default="data/resume_classification.csv",
        help="Path to Resume Classification dataset CSV",
    )
    parser.add_argument(
        "--sr", "--structured-resume",
        dest="structured_resume",
        default="data/structured_resume.jsonl",
        help="Path to Structured Resume dataset (.jsonl format)",
    )
    parser.add_argument(
        "--jd", "--job-descriptions",
        dest="job_descriptions",
        default="data/jobs.csv",
        help="Path to Job Descriptions dataset CSV",
    )
    parser.add_argument(
        "--out",
        dest="output",
        default="negarit_dataset.json",
        help="Output path for the final JSON dataset",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()

    paths = {
        "resume_classification": args.resume_classification,
        "structured_resume":     args.structured_resume,
        "job_descriptions":      args.job_descriptions,
    }

    run_pipeline(dataset_paths=paths, output_path=args.output)
