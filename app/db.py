import asyncpg
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

async def get_db():
    #establish connection to the database
    return await asyncpg.connect(DATABASE_URL)