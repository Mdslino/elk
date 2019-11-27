from decouple import config as get_env

access_log = "-"
error_log = "-"
loglevel = get_env("GUNICORN_LOG_LEVEL", "DEBUG")
bind = f"{get_env('HOST', 'localhost')}:{get_env('PORT', 8000)}"
workers = get_env("GUNICORN_WORKERS", default=1, cast=int)
