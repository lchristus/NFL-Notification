from fastapi import FastAPI
import scraper.py 

app = FastAPI()

@app.get("/status")
def root():
    return {"status": "working"}

@app.get("")
def root():
    scraper.start()
    return {"status": "starting"}
