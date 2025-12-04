from fastapi import FastAPI, HTTPException

app = FastAPI(title="API Getway", description="API Getway for AI Powered E-commerce")

USER_SERVICE_URL = "http://localhost:8001"
PRODUCT_SERVICE_URL = "http://localhost:8002"


@app.get("/api-health")
def api_health():
    return {"status": "ok", "message": "API getway is running"}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)