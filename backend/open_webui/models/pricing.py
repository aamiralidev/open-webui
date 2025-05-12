from sqlalchemy import Column, String, Integer, Numeric
from open_webui.internal.db import Base
from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from typing import Optional, List
from open_webui.internal.db import get_db

class ModelPricing(Base):
    __tablename__ = "model_pricing"

    model_id = Column(String, primary_key=True)
    max_output_tokens = Column(Integer)
    input_price_per_million_token = Column(Numeric(precision=10, scale=6))
    output_price_per_million_token = Column(Numeric(precision=10, scale=6))

class ModelPricingModel(BaseModel):
    model_id: str
    max_output_tokens: int
    input_price_per_million_token: Decimal
    output_price_per_million_token: Decimal

    model_config = ConfigDict(from_attributes=True)

class ModelPricingTable:

    def get_all_pricing(self) -> List[ModelPricingModel]:
        with get_db() as db:
            records = db.query(ModelPricing).all()
            return [ModelPricingModel.model_validate(r) for r in records]

    def get_pricing_by_model_id(self, model_id: str) -> Optional[ModelPricingModel]:
        with get_db() as db:
            record = db.query(ModelPricing).filter_by(model_id=model_id).first()
            return ModelPricingModel.model_validate(record) if record else None

    def upsert_pricing(self, pricing: ModelPricingModel) -> bool:
        with get_db() as db:
            existing = db.query(ModelPricing).filter_by(model_id=pricing.model_id).first()
            if existing:
                for field, value in pricing.model_dump().items():
                    setattr(existing, field, value)
            else:
                db.add(ModelPricing(**pricing.model_dump()))
            db.commit()
            return True

    def delete_all_pricing(self) -> None:
        with get_db() as db:
            db.query(ModelPricing).delete()
            db.commit()

    def replace_all_pricing(self, pricing_list: List[ModelPricingModel]) -> bool:
      try:
          with get_db() as db:
              # Start a transaction
              db.query(ModelPricing).delete()  # Delete all existing records

              # Insert new pricing entries
              new_records = [ModelPricing(**pricing.model_dump()) for pricing in pricing_list]
              db.add_all(new_records)

              db.commit()
              return True
      except Exception as e:
          db.rollback()
          print("Error replacing pricing:", e)
          return False

# Singleton instance
ModelPricings = ModelPricingTable()

