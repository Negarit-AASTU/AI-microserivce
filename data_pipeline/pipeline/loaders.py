import ast
import logging
import os

import pandas as pd

logger = logging.getLogger(__name__)

UNIFIED_COLUMNS = ["name", "category", "skills", "experience", "education", "raw_text"]

def _safe_read_file(path: str, **kwargs) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Dataset not found at: {path}\n"
            "Download from Kaggle and place in the data/ directory."
        )
    logger.info(f"Loading: {path}")
    if path.lower().endswith(".jsonl"):
        return pd.read_json(path, lines=True, **kwargs)
    return pd.read_csv(path, **kwargs)

_safe_read_csv = _safe_read_file


def _col(df: pd.DataFrame, candidates: list, default="") -> pd.Series:
    for c in candidates:
        if c in df.columns:
            return df[c]
    return pd.Series([default] * len(df))


def _parse_list_field(value) -> list:
    if isinstance(value, list):
        return value
    if pd.isna(value) or value == "":
        return []
    if isinstance(value, str):
        value = value.strip()
        if value.startswith("["):
            try:
                result = ast.literal_eval(value)
                if isinstance(result, list):
                    return [str(x).strip() for x in result]
            except (ValueError, SyntaxError):
                pass
        return [x.strip() for x in value.split(",") if x.strip()]
    return [str(value)]

def load_resume_classification(path: str) -> pd.DataFrame:
    
    df = _safe_read_file(path)
    logger.info(f"Resume Classification raw shape: {df.shape}")

    unified = pd.DataFrame()
    unified["name"] = ""                                          
    unified["category"] = _col(df, ["Category", "category"]).fillna("").str.lower().str.strip()
    unified["skills"] = "[]"                                     
    unified["experience"] = "[]"
    unified["education"] = "[]"
    unified["raw_text"] = (
        _col(df, ["Resume_str", "Resume", "resume_str", "text"])
        .fillna("")
        .astype(str)
        .str.strip()
    )

    logger.info(f"Resume Classification unified shape: {unified.shape}")
    return unified


def _jsonl_col_to_str(series: pd.Series) -> pd.Series:
    """
    Convert a column that may contain Python lists/dicts (common in JSONL
    files) into JSON-string representations that _parse_list_field can handle.
    """
    import json

    def _convert(val):
        if isinstance(val, (list, dict)):
            return json.dumps(val, ensure_ascii=False)
        return val

    return series.apply(_convert)


def load_structured_resume(path: str) -> pd.DataFrame:
    is_jsonl = path.lower().endswith(".jsonl")
    df = _safe_read_file(path)
    logger.info(f"Structured Resume raw shape: {df.shape}")

    unified = pd.DataFrame()
    unified["name"] = _col(df, ["name", "Name", "full_name", "candidate_name"]).fillna("")
    unified["category"] = (
        _col(df, ["Category", "category", "domain", "field", "job_category"])
        .fillna("")
        .astype(str)
        .str.lower()
        .str.strip()
    )

    skills_raw = _col(df, ["skills", "Skills", "skill_set", "technical_skills"]).fillna("[]")
    exp_raw    = _col(df, ["experience", "Experience", "work_experience"]).fillna("[]")
    edu_raw    = _col(df, ["education", "Education", "educational_background"]).fillna("[]")

    if is_jsonl:
        skills_raw = _jsonl_col_to_str(skills_raw)
        exp_raw    = _jsonl_col_to_str(exp_raw)
        edu_raw    = _jsonl_col_to_str(edu_raw)

    unified["skills"]     = skills_raw
    unified["experience"] = exp_raw
    unified["education"]  = edu_raw
    unified["raw_text"] = (
        _col(df, ["Resume_str", "resume", "Resume", "text", "raw_text"])
        .fillna("")
        .astype(str)
        .str.strip()
    )

    logger.info(f"Structured Resume unified shape: {unified.shape}")
    return unified

def load_job_descriptions(path: str) -> pd.DataFrame:
    df = _safe_read_file(path)
    logger.info(f"Job Descriptions raw shape: {df.shape}")

    title_col = _col(df, ["Job Title", "job_title", "title", "Position", "Role"]).fillna("")
    desc_col = _col(df, ["Job Description", "description", "Description", "details"]).fillna("")
    skills_col = _col(df, ["skills", "Skills", "required_skills", "key_skills"]).fillna("[]")

    unified = pd.DataFrame()
    unified["name"] = ""
    unified["category"] = title_col.astype(str).str.lower().str.strip()
    unified["skills"] = skills_col
    unified["experience"] = "[]"
    unified["education"] = "[]"
    unified["raw_text"] = (title_col.astype(str) + " " + desc_col.astype(str)).str.strip()

    logger.info(f"Job Descriptions unified shape: {unified.shape}")
    return unified

def load_all_datasets(paths: dict) -> pd.DataFrame:
    frames = []

    loaders = {
        "resume_classification": load_resume_classification,
        "structured_resume": load_structured_resume,
        "job_descriptions": load_job_descriptions,
    }

    for key, loader_fn in loaders.items():
        path = paths.get(key)
        if not path:
            logger.warning(f"No path provided for '{key}' — skipping.")
            continue
        try:
            df = loader_fn(path)
            df["_source"] = key          
            frames.append(df)
        except FileNotFoundError as e:
            logger.warning(str(e))

    if not frames:
        raise RuntimeError("No datasets were loaded. Provide at least one dataset path.")

    merged = pd.concat(frames, ignore_index=True)
    for col in UNIFIED_COLUMNS:
        if col not in merged.columns:
            merged[col] = ""

    logger.info(f"Total merged records: {len(merged)}")
    return merged[UNIFIED_COLUMNS + ["_source"]]
