from datetime import datetime, timedelta
from typing import List, Dict, Optional

from .time_utils import timestamp_formatter

### for debugging ###
from src import setup_logger
log = setup_logger(__name__)

def insert_timestamp(history: List[Dict[str, str]], prompt_format: str) -> List[Dict[str, str]]:
    """
    Insert timestamp to the history record (as a system prompt).
    
    Args:
        history: The conversation history record.
        
    Returns:
        The updated history record with timestamp.
    """
    if not history:
        return history
    
    log.debug(f"Inserting timestamp to history: {history}")
    
    tmp_timestamp = datetime.fromisoformat(history[0]['timestamp'])
    formatted = [create_system_message(prompt_format.format(timestamp=timestamp_formatter(tmp_timestamp))), history[0]]
    for item in history[1:]:
        if item['timestamp']:
            time_delta = datetime.fromisoformat(item['timestamp']) - tmp_timestamp
            if time_delta > timedelta(minutes=5):
                tmp_timestamp = datetime.fromisoformat(item['timestamp'])
                formatted.append(create_system_message(prompt_format.format(timestamp=timestamp_formatter(tmp_timestamp))))

        formatted.append(item)
    
    return formatted

def create_system_message(system_prompt: str) -> Dict[str, str]:
    """
    Create a system message with the specified system prompt.
    
    Args:
        system_prompt: The system prompt to be included in the system message.
        
    Returns:
        The system message dictionary.
    """
    return {"role": "system", "content": system_prompt}