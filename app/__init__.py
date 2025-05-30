import logging.config
import os

from datetime import date

import yaml

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI

from app.auth import auth_router
from app.pdf import pdf_router

load_dotenv(find_dotenv())


def setup_logging():
    today = date.today().strftime("%Y-%m-%d")
    log_path = f"logs/{today}.log"
    os.makedirs("logs", exist_ok=True)

    with open("config/log_config.yml") as f:
        config = yaml.safe_load(f)

    # Dynamically inject log file name
    if "handlers" in config and "file" in config["handlers"]:
        config["handlers"]["file"]["filename"] = log_path

    logging.config.dictConfig(config)


# Setup logging before app starts
setup_logging()


def create_app():
    app = FastAPI()

    app.include_router(auth_router())
    app.include_router(pdf_router())

    return app
