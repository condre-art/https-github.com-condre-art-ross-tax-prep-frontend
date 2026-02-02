from fastapi import FastAPI, Header, HTTPException, Response

app = FastAPI(title="Tax Preparation API")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get(
    "/api/certificates/{certificateId}/download",
    response_class=Response,
    responses={
        200: {"content": {"application/pdf": {}}},
        401: {"description": "Unauthorized"},
        404: {"description": "Not found"},
    },
)
def download_certificate(certificateId: str, authorization: str | None = Header(default=None)):
    if authorization is None or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    if certificateId == "missing":
        raise HTTPException(status_code=404, detail="Not found")

    pdf_bytes = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\ntrailer\n<<>>\n%%EOF"
    return Response(content=pdf_bytes, media_type="application/pdf")
