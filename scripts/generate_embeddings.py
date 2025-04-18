import asyncio
from sentence_transformers import SentenceTransformer
import asyncpg
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
model = SentenceTransformer('all-MiniLM-L6-v2')

async def generate_embeddings():
    # Connect to the DB
    conn = await asyncpg.connect(DATABASE_URL)
    # Fetch all contents
    rows = await conn.fetch("SELECT id, content FROM magazine_contents")
    print(f"Generating embeddings for {len(rows)} entries...")

    for row in rows:
        content_id = row["id"]
        text = row["content"]
        # Generate embeddings
        vector = model.encode(text).tolist()
        # Save into DB
        await conn.execute(
            "UPDATE magazine_contents SET vector_representation = $1 WHERE id = $2",
            f"{vector}",
            content_id
        )
    await conn.execute(
        """
        CREATE INDEX ON magazine_contents USING ivfflat (vector_representation vector_cosine_ops);
        ANALYZE magazine_contents;""",
    )
    await conn.close()
    print("All embeddings saved.")

if __name__ == "__main__":
    asyncio.run(generate_embeddings())