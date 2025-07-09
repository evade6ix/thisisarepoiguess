from fastapi import FastAPI, Response, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from bigcommerce import BigCommerceAPI
from feed_generator import generate_meta_xml

app = FastAPI()

# CORS Middleware (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment variables
FEED_URL_SECRET = os.getenv("FEED_URL_SECRET", "meta-feed-7f4e9b2c9a1e")

# Initialize BigCommerce API
bc_api = BigCommerceAPI()

@app.get(f"/{FEED_URL_SECRET}/products.xml")
async def get_meta_feed():
    try:
        products = bc_api.get_all_products()
        xml_feed = generate_meta_xml(products)
        return Response(content=xml_feed, media_type="application/xml")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating feed: {e}")

@app.post("/webhook")
async def webhook_listener(request: Request):
    payload = await request.json()
    # Optionally validate webhook signature here
    print("Webhook received:", payload)
    # Refresh cached feed or regenerate feed as needed
    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
