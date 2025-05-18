from fastapi import FastAPI, Request, HTTPException
import hashlib
import hmac
from fastapi import APIRouter, Depends, HTTPException, status, Request
import logging
from open_webui.models.users import User
from open_webui.internal.db import get_db
from datetime import datetime, timedelta
import json

router = APIRouter()

SIGNING_SECRET = 'c845e8a6f2bb3f0d7d22e8b4728f7ce5b3f7e0'
CREDIT_PLANS = {
    'creator': 30000,
    'creator+': 80000,
    'on_trial': 5000,
}


@router.post("/webhook")
async def webhook(request: Request):
    signature = request.headers.get('x-signature')
    if not signature:
        raise HTTPException(status_code=400, detail="Missing signature")

    body = await request.body()
    digest = hmac.new(SIGNING_SECRET.encode(), body, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(digest, signature):
        raise HTTPException(status_code=403, detail="Invalid signature")

    logging.error("Webhook received and Verified")
    event = await request.json()
    data = event.get('data', {})
    attributes = data.get("attributes", {})

    email = attributes.get("user_email")
    variant = attributes.get("variant_name", "").lower()
    status = attributes.get("status")
    trial_ends_at = attributes.get("trial_ends_at", '')

    logging.error(f"Received email: {email}")
    logging.error(f"Received variant: {variant}")
    logging.error(f"Received status: {status}")
    logging.error(f"Received trial_ends_at: {trial_ends_at}")

    if not email:
        raise HTTPException(status_code=422, detail="Missing user_email in payload")
    with get_db() as db:
        user = db.query(User).filter_by(email=email).first()
        if not user:
            logging.error(f"User not found: {email}")
            raise HTTPException(status_code=404, detail="User not found")
                    
        # Determine credit amount
        credit_amount = CREDIT_PLANS.get(variant)
        if credit_amount is None:
            logging.error(f"Unknown variant_name: {variant}")
            raise HTTPException(status_code=400, detail=f"Unknown variant_name: {variant}")

        # Update user fields
        logging.error(f"Updating user credit_resets_at: {user.credit_resets_at}")
        logging.error(f"Updating user stats is in on_trial: {status in ['on_trial']}")
        if status in ["on_trial"] and not user.credit_resets_at:
            logging.error(f"User is on trial: {email}")
            credit_amount = CREDIT_PLANS.get("on_trial")
            user.credit_limit = (user.credit_limit or 0) + credit_amount
            user.credits = (user.credits or 0) + credit_amount
            print(json.dumps(event, indent=2))
            user.credit_resets_at = datetime.fromisoformat(trial_ends_at.replace("Z", "+00:00"))
        elif status in ["active"]:
            logging.error(f"User is active: {email}")
            if user.subscription != variant:
                user.credit_limit = (user.credit_limit or 0) + credit_amount
                user.credits = (user.credits or 0) + credit_amount
                if status == "active":
                    user.subscription_status = "active"
                    user.credit_resets_at = datetime.now() + timedelta(days=30)
        user.subscription = variant
        user.subscription_status = status
        if user.role == 'pending':
            logging.error(f"User is pending and now active: {email}")
            user.role = 'user'
        if status in ["expired", "unpaid"]:
            logging.error(f"User is expired or unpaid: {email}")
            user.subscription = None
            user.subscription_status = None
            user.credit_limit = 0
            user.credits = 0
            user.credit_resets_at = None
            user.role = 'pending'
        db.commit()

    # Process your payload
    return {"status": "success"}
