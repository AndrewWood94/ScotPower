from fastapi import FastAPI, Query
from typing import Optional, List, Literal
from app.search import combined_search

app = FastAPI()

@app.get("/search")
async def search(
    query: str = Query(...),
    keyword: bool = True,
    vector: bool = True,
    limit: int = Query(default=10),
    order_by: Literal["newest", "oldest", "relevance"] = "relevance",
    categories: Optional[List[str]] = Query(None)):
    
    results = await combined_search(query, keyword, vector, limit, categories, order_by)
    return results