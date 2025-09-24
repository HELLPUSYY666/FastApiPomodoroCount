import os

from dotenv import load_dotenv
from uvicorn.workers import UvicornWorker

bind = "0.0.0.0:8000"
workers = 4
worker_class = UvicornWorker

environment = os.getenv("ENVIRONMENT")
print(environment)
env = os.path.join(os.getcwd(), f".{environment}.env")
print(env, "file_path")
if os.path.exists(env):
    load_dotenv(env)
