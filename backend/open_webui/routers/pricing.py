from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Request
from open_webui.models.pricing import ModelPricingModel, ModelPricings
from open_webui.utils.auth import get_admin_user
from open_webui.constants import ERROR_MESSAGES
import logging

router = APIRouter()

############################
# Get All Model Pricing
############################

@router.get("/", response_model=List[ModelPricingModel])
async def get_all_model_pricing(user=Depends(get_admin_user)):
    try:
        return ModelPricings.get_all_pricing()
    except Exception as e:
        logging.error(f"Error fetching model pricing: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch model pricing: {str(e)}",
        )


############################
# Replace All Model Pricing
############################

@router.post("/update", response_model=bool)
async def replace_all_model_pricing(
    pricing_data: List[ModelPricingModel], user=Depends(get_admin_user)
):
    success = ModelPricings.replace_all_pricing(pricing_data)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to replace model pricing.",
        )
    return True
