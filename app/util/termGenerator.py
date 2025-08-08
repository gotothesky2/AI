from datetime import datetime

def default_term() -> int:
    """현재 월이 1~6월이면 1학기, 7~12월이면 2학기 반환"""
    month = datetime.now().month
    return 1 if month < 7 else 2