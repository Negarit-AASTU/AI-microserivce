import json
import logging
import os
from collections import Counter
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def save_json(records: List[Dict[str, Any]], output_path: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(records, fh, ensure_ascii=False, indent=2)

    size_kb = os.path.getsize(output_path) / 1024
    logger.info("Dataset saved → %s  (%.1f KB, %d records)", output_path, size_kb, len(records))
    print(f"\n Saved {len(records):,} records → {output_path}  ({size_kb:.1f} KB)")

