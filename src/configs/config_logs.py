import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timezone


def setup_root_logger(logger_name, project_root_dir, log_level=logging.INFO, max_size_mb=10, backup_count=5):
    """
    루트 로거를 설정하여 모든 모듈이 하나의 로그 파일에 기록되도록 합니다.
    
    Args:
        log_level (int): 로깅 레벨 (기본: INFO)
        max_size_mb (int): 로그 파일 최대 크기 (MB 단위, 기본: 10MB)
        backup_count (int): 보관할 백업 파일 수 (기본: 5)
        
    Returns:
        logging.Logger: 루트 로거
    """
    log_dir = os.path.join(project_root_dir, 'logs')
    os.makedirs(log_dir, exist_ok=True)

    today = datetime.now(timezone.utc).strftime("%Y%m%d") # UTC time zone이라는 점 주의
    log_file = os.path.join(log_dir, f"{today}-{logger_name}.log")

    root_logger = logging.getLogger()  # 🔥 루트 로거 가져오기
    if isinstance(log_level, str):
        log_level = getattr(logging, log_level.upper(), logging.INFO)
    else: 
        root_logger.setLevel(log_level)

    if root_logger.hasHandlers():
        root_logger.handlers.clear() # 🔥 기존 핸들러 제거 

    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_size_mb * 1024 * 1024, backupCount=backup_count, encoding='utf-8'
    )
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    return root_logger  # 🔥 루트 로거 반환


def setup_logger(module_name):
    """
    서브 모듈용 로거 설정 (핸들러 추가 없이 루트 로거를 사용)
    
    Args:
        module_name (str): 모듈 이름 (로그에서 구분하는 용도)
        
    Returns:
        logging.Logger: 설정된 로거
    """
    logger = logging.getLogger(module_name)
    logger.propagate = True  # 🔥 부모 로거(루트 로거)로 로그를 전달하도록 설정
    return logger
