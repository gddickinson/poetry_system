"""Start the Poetry System web interface on http://127.0.0.1:8139 (local only).

Install: pip install -r requirements-web.txt   (add spacy, textblob and en_core_web_sm for imagery and sentiment)
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("web.app:app", host="127.0.0.1", port=8139)
