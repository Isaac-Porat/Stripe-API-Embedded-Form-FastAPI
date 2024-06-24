import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import stripe
import uvicorn
from dotenv import load_dotenv

logger = logging.getLogger("uvicorn")

load_dotenv()

stripe.api_key = os.getenv("STRIPE_API_KEY")

logger.warning(stripe.api_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

YOUR_DOMAIN = 'http://localhost:5173'

class SessionStatus(BaseModel):
    session_id: str

@app.post("/create-checkout-session")
async def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            ui_mode='embedded',
            line_items=[
                {
                    'price': 'price_1PVFxTKrQQFwO9FldVAmc5q0',
                    'quantity': 1,
                },
            ],
            mode='payment',
            return_url=YOUR_DOMAIN + '/return?session_id={CHECKOUT_SESSION_ID}',
        )
        return JSONResponse(content={"clientSecret": session.client_secret})
    except Exception as e:
        logger.warning(str(e))
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/session-status")
async def session_status(session_id: str):
  try:
      session = stripe.checkout.Session.retrieve(session_id)
      return JSONResponse(content={"status": session.status, "customer_email": session.customer_details.email})
  except Exception as e:
      logger.warning(str(e))
      raise HTTPException(status_code=400, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)