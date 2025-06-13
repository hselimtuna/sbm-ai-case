import os
from configparser import ConfigParser
from dotenv import load_dotenv

load_dotenv()

conf = ConfigParser()

conf["DB"] = {
    "USERNAME": os.getenv("DB_USER"),
    "PASSWORD": os.getenv("DB_PASS"),
    "HOST": os.getenv("DB_HOST"),
    "PORT": os.getenv("DB_PORT"),
    "DB_NAME": os.getenv("DB_NAME"),
}

conf["TOGETHER"] = {"KEY": os.getenv("TOGETHER_KEY")}
