# apps/model-control-plane/models/audit.py
from sqlalchemy import Column, String, DateTime, event
from sqlalchemy.orm import Session
from .base import Base
from datetime import datetime
import uuid

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id          = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id   = Column(String, nullable=False, index=True)
    user_id     = Column(String, nullable=False)
    action      = Column(String, nullable=False)   # e.g. "model:promote"
    resource_id = Column(String)
    metadata_json = Column(String)                   # JSON string
    created_at  = Column(DateTime, default=datetime.utcnow, nullable=False)

@event.listens_for(AuditLog, "before_update")
def prevent_update(mapper, connection, target):
    raise RuntimeError("AuditLog records are immutable — do not update them")

def audit_log(db: Session, user_id: str, tenant_id: str, action: str, resource_id: str = None):
    entry = AuditLog(
        user_id=user_id, tenant_id=tenant_id,
        action=action, resource_id=resource_id
    )
    db.add(entry)
    db.commit()
