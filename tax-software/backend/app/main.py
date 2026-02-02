from fastapi import FastAPI

app = FastAPI(title="Tax Preparation API")


@app.get("/health")
def health_check():
    return {"status": "ok"}
