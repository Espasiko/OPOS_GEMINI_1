import json
import os
import time
import logging
from typing import Dict, Any
from database.db import db

logger = logging.getLogger(__name__)

LOG_PATH = os.getenv("USAGE_LOG_FILE", os.path.join(os.path.dirname(__file__), "../data/usage_logs.jsonl"))

class UsageLogger:
    def __init__(self, log_path: str = LOG_PATH):
        self.log_path = os.path.abspath(log_path)
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def log(self, record: Dict[str, Any]):
        # Intentar DB primero
        try:
            with db.get_cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO usage_logs (
                        user_id, session_id, provider_id, model_name,
                        input_tokens, output_tokens, total_tokens,
                        input_cost_eur, output_cost_eur, total_cost_eur,
                        endpoint, request_type, request_duration_ms, success, error_message
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    [
                        record.get('user_id'),
                        record.get('session_id'),
                        record.get('provider_id'),
                        record.get('model_name'),
                        record.get('input_tokens'),
                        record.get('output_tokens'),
                        record.get('total_tokens'),
                        record.get('input_cost_eur'),
                        record.get('output_cost_eur'),
                        record.get('total_cost_eur'),
                        record.get('endpoint'),
                        record.get('request_type'),
                        record.get('request_duration_ms'),
                        record.get('success', True),
                        record.get('error_message')
                    ]
                )
                return
        except Exception as e:
            logger.warning(f"DB logging failed, falling back to file: {e}")
        # Fallback file
        try:
            with open(self.log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception as fe:
            logger.error(f"Failed to write usage log file: {fe}")

    def summary(self) -> Dict[str, Any]:
        summary = {
            'totalRequests': 0,
            'totalTokens': 0,
            'totalCost': 0.0,
            'byProvider': {}
        }
        if not os.path.exists(self.log_path):
            return summary
        try:
            with open(self.log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        rec = json.loads(line)
                        summary['totalRequests'] += 1
                        summary['totalTokens'] += rec.get('total_tokens', 0)
                        summary['totalCost'] += rec.get('total_cost_eur', 0.0)
                        p = rec.get('provider_id')
                        if p not in summary['byProvider']:
                            summary['byProvider'][p] = {'requests': 0, 'tokens': 0, 'cost': 0.0}
                        summary['byProvider'][p]['requests'] += 1
                        summary['byProvider'][p]['tokens'] += rec.get('total_tokens', 0)
                        summary['byProvider'][p]['cost'] += rec.get('total_cost_eur', 0.0)
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            logger.error(f"Error reading usage log file: {e}")
        return summary

usage_logger = UsageLogger()
