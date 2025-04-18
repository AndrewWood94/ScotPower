# Initial Setup 

### Install the required packages

From the `search_api/` folder location run the following:   

`python3.9 -m venv .venv`\
`source .venv/bin/activate`\
`pip install -r requirements.txt`\
`bash scripts/setup.sh`

### Set up the database with your chosen username and password

`sudo service postgresql start`\
`sudo -u postgres psql -v user=username -v pass=password -f scripts/create_db.sql`

### Populate the database with data in *scripts/populate_db.sql*
`PGPASSWORD=password psql -U username -d magazine_db -f scripts/populate_db.sql`

### Setup *.env* file
Copy *.env.example* to new *.env* file\
`cp .env.example .env`\
Edit the DATABASE_URL in *.env* to include your username and password\
`DATABASE_URL = "postgresql://username:password@localhost/magazine_db"`

### Generate the embeddings for vector search
`python scripts/generate_embeddings.py`

# Run the API
`uvicorn app.main:app --reload --port 5000`

# Testing

The format of your search query should be as follows:  
http://localhost:5000/search?query=[addition+separated+text]

In addition, a number of parameters are available and can be included in the search, separated by '&'  
* keyword=[true/false] (default = true) - whether the system performs keyword search   
* vector=[true/false] (default = true) - whether the system performs vector search  
* order_by=[newest/oldest/relevance] (default = relevance) - how the results should be ordered  
* limit=[number] (default = 10) - the maximum number of results to return  
* categories=[Technology/Travel/Gardening/Fitness/Business/Sports/Art/Science/Fashion/Home+Decor/Music/Cooking] - filters which magazine categories are included in the search 
    * multiple categories can be selected by duplicating the parameter

Queries can be run either in a browser search, or in a terminal with the `curl` command, e.g `curl 'http://localhost:5000/search?query=Sports'`

## Example queries:
* http://localhost:5000/search?query=Sports
    * Runs a combined vector & keyword search on the word Sports, returning up to 10 results sorted by relevance  
* http://localhost:5000/search?query=Sports+Evelin&keyword=False
    * Runs a vector-only search on the words Sports and Evelin, returning up to 10 results sorted by relevance
* http://localhost:5000/search?query=Sports+Evelin&vector=False&limit=5
    * Runs a keyword-only search on the words Sports and Evelin, returning up to 5 results sorted by relevance (4 results in practice)
* http://localhost:5000/search?query=Sports&limit=15&&categories=Business&categories=Fitness
    * Runs a combined vector & keyword search on the word Sports, from Business or Fitness magazines returning up to 15 results sorted by relevance  
* http://localhost:5000/search?query=Sports+Evelin&limit=5&order_by=oldest
    * Runs a combined vector & keyword search on the words Sports and Evelin, returning up to 5 results sorted by publication date (oldest first) 
* http://localhost:5000/search?query=Sports&limit=50&categories=Fitness&order_by=newest
    * Runs a combined vector & keyword search on the word Sports, from Fitness magazines returning up to 50 results sorted by publication date (newest first) 

