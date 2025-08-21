# Gunicorn 설정 파일
import multiprocessing

# 서버 소켓 설정
bind = "0.0.0.0:8081"
backlog = 2048

# 워커 프로세스 설정
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# 타임아웃 설정 - AI 리포트 생성 시간을 고려하여 충분히 설정
timeout = 600  # 10분 (AI 리포트 생성에 충분한 시간)
keepalive = 2
graceful_timeout = 60

# 로깅 설정
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# 프로세스 설정
preload_app = True
reload = False

# 보안 설정
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
