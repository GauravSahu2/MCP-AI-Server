from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from .base import Base
from datetime import datetime
import uuid

class TenantUsage(Base):
    __tablename__ = "tenant_usage"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, ForeignKey("tenants.id"), index=True, nullable=False)
    tokens_used = Column(Integer, nullable=False)
    cost_incurred = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
