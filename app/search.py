from app.db import get_db
from app.embedding import embed_text

async def keyword_search(conn, query: str, categories, limit):
    args = [query, limit]
    #SQL to compare query keywords to keywords search vector
    scoring = """ts_rank(
                        c.keyword_search_vector,
                        plainto_tsquery('english', $1)
                    )"""

    return await perform_search(conn, args, scoring, categories)

async def vector_search(conn, query: str, categories, limit):

    #generate embedding for query
    embedding = embed_text(query)
    args = [f"{embedding}", limit]
    #SQL to compare embedding to vector_representaion
    scoring = "1 - (c.vector_representation <=> $1::vector)"

    await conn.execute("SET ivfflat.probes = 10;")

    return await perform_search(conn, args, scoring, categories)

async def perform_search(conn, args, scoring, categories):

    #setup sql category filter if any given 
    if categories:
        category_filter = "WHERE m.category = ANY($3)"
        args.append(categories)
    else:
        category_filter=""

    #build sql query
    sql = f"""
            WITH ranked AS (
                SELECT c.id, c.article_title, m.title as magazine_title, m.author, m.category, m.publication_date,
                    CONCAT(SUBSTRING(c.content, 1, 100),'...') AS content, {scoring} AS score
                FROM magazines m
                JOIN magazine_contents c ON m.id = c.magazine_id
                {category_filter})
            SELECT * FROM ranked
            WHERE score > 0.00001
            ORDER BY score DESC
            LIMIT $2
        """

    #perform_search
    rows = await conn.fetch(sql, *args)
    return [dict(r) for r in rows]


async def combined_search(query:str, keyword, vector, limit, categories, sorting):

    conn = await get_db()
    #perform keyword & vector searches
    results = []
    if keyword:
        results.extend(await keyword_search(conn, query, categories, limit))
    if vector:
        results.extend(await vector_search(conn, query, categories, limit))
    await conn.close()

    #combine results and remove duplicates
    seen = {}
    for result in results:
        item_id = result.pop("id")
        if item_id not in seen or result["score"] > seen[item_id]["score"]:
            seen[item_id] = result
    deduped = list(seen.values())

    #sort results
    if sorting == "newest":
        deduped.sort(key=lambda x: x.get("publication_date"), reverse=True)
    elif sorting == "oldest":
        deduped.sort(key=lambda x: x.get("publication_date"))
    else:
        deduped.sort(key=lambda x: x.get("score"), reverse=True)

    #return requested number of results
    return deduped[0:limit]
