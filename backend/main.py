from fastapi import FastAPI
from elasticsearch import Elasticsearch

app = FastAPI()

# es = Elasticsearch()

@app.get('/')
def read_root():
    return {"testK":"testV"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id":item_id, "q":q}




# this is fron la

# this is fron la

# this is from PC