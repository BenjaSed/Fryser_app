import os
import json
import asyncio
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator
import aiofiles

app = FastAPI()

# /data is the official persistent storage directory for Home Assistant Add-ons
DB_FILE = "/data/freezer_db.json"

# Fallback for local testing outside of Home Assistant
if not os.path.exists("/data"):
    DB_FILE = "freezer_db.json"

# Async lock to prevent race conditions during file read/write operations
file_lock = asyncio.Lock()


# Strict schema for items to validate incoming data
class FreezerItem(BaseModel):
    id: str = Field(..., max_length=100)
    name: str = Field(..., min_length=1, max_length=200)
    size: str = Field(default="", max_length=100)
    shelf: str = Field(default="Hylde 1", max_length=100)
    qty: int = Field(default=1, ge=0, le=10000)
    date: str = Field(default="", max_length=10)

    @field_validator("name", "size", "shelf", mode="before")
    @classmethod
    def sanitize_strings(cls, v):
        if isinstance(v, str):
            # Strip whitespace to clean up input
            return v.strip()
        return v


async def load_db_async() -> list:
    if not os.path.exists(DB_FILE):
        return []
    try:
        async with aiofiles.open(DB_FILE, mode="r", encoding="utf-8") as f:
            content = await f.read()
            if not content.strip():
                return []
            return json.loads(content)
    except Exception as e:
        print(f"Error reading database: {e}")
        return []


async def save_db_async(data: list):
    # Write to a temporary file first, then replace to prevent partial writes
    temp_file = f"{DB_FILE}.tmp"
    async with aiofiles.open(temp_file, mode="w", encoding="utf-8") as f:
        await f.write(json.dumps(data, ensure_ascii=False, indent=2))
    os.replace(temp_file, DB_FILE)


@app.get("/")
def read_root():
    return FileResponse("app/index.html")


@app.get("/api/items")
async def get_items():
    async with file_lock:
        return await load_db_async()


@app.post("/api/items")
async def save_items(items: List[FreezerItem]):
    """
    FastAPI automatically validates that 'items' is a list of valid FreezerItem objects.
    If any item contains malicious payloads or wrong data types, FastAPI returns 422 Unprocessable Entity.
    """
    async with file_lock:
        try:
            # Convert validated Pydantic models back to dictionaries for JSON serialization
            serialized_data = [item.model_dump() for item in items]
            await save_db_async(serialized_data)
            return {"status": "success"}
        except Exception as e:
            print(f"Error saving database: {e}")
            raise HTTPException(status_code=500, detail="Failed to save data to disk")