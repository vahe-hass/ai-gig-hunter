from fastapi import FastAPI
from agents.marketing_agent import MarketingAgent
from agents.sales_agent import SalesAgent

app = FastAPI()

@app.get("/run-marketing")
def run_marketing():
    MarketingAgent().run()
    return {"status": "marketing done"}

@app.get("/run-sales")
def run_sales():
    SalesAgent().run()
    return {"status": "sales done"}