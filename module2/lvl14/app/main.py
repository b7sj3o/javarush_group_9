import os

import psycopg
import redis
from fastapi import FastAPI

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")

cache = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    decode_responses=True,
)


@app.get("/")
def home():
    visits = cache.incr("visits")

    with psycopg.connect(DATABASE_URL) as conn:
        conn.execute("""
            INSERT INTO visits (visit_number)
            VALUES (%s)
        """, (visits,))

    return {
        "message": "Hello from Docker Compose!",
        "visits": visits,
    }


@app.get("/history")
def history():
    with psycopg.connect(DATABASE_URL) as conn:
        rows = conn.execute("""
            SELECT id, visit_number
            FROM visits
            ORDER BY id DESC
            LIMIT 10
        """).fetchall()

    return {
        "history": [
            {"id": row[0], "visits": row[1]}
            for row in rows
        ]
    }
    

@app.post("/number")
def create_number():
    import random
    from pathlib import Path
    
    folder = Path("/app/data")
    files = len([1 for f in folder.iterdir() if f.is_file()]) + 1
    
    num = random.randint(1, 10000000000)
    filename = f"{files}.txt"
    
    with open(folder/filename, "w") as file:
        file.write(str(num))
        
    return {
        "number": num,
        filename: folder / filename
    }
        
        
    