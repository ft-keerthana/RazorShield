from fastapi import FastAPI

app = FastAPI(
    title="RazorShield API",
    description="AI-powered risk intelligence platform for modern payments",
    version="0.1.0",
)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}