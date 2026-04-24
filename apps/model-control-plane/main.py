from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import uuid
import datetime
from sqlalchemy import create_engine, Column, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from auth.rbac import require_permission
from models.audit import audit_log
import os

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./aegis.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Model(Base):
    __tablename__ = "models"
    id = Column(String, primary_key=True, index=True)
    tenant_id = Column(String, index=True)
    name = Column(String)
    version = Column(String)
    description = Column(String)
    framework = Column(String)
    s3_uri = Column(String)
    status = Column(String)
    registered_at = Column(DateTime, default=datetime.datetime.utcnow)

# Ensure tables are created (in production migrations handle this)
Base.metadata.create_all(bind=engine)

# Pydantic Schemas
class ModelSpec(BaseModel):
    name: str
    version: str
    description: str
    framework: str
    s3_uri: str

class ModelStatusUpdate(BaseModel):
    status: str

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="Aegis MCP Control Plane", description="Centralized Model Registry and Lifecycle Manager")

from auth.jwt import create_access_token

from models.rbac import Tenant, Role

from models.billing import TenantUsage

@app.post("/api/v1/billing/usage")
@require_permission("billing:write")
async def record_usage(req: dict, db: Session = Depends(get_db)):
    usage = TenantUsage(
        tenant_id=req["tenant_id"],
        tokens_used=req["tokens"],
        cost_incurred=req["cost"]
    )
    db.add(usage)
    db.commit()
    return {"status": "success"}

@app.post("/api/v1/admin/tenants")
@require_permission("tenant:admin")
async def create_tenant(name: str, db: Session = Depends(get_db)):
    tenant_id = str(uuid.uuid4())
    slug = name.lower().replace(" ", "-")
    db_tenant = Tenant(id=tenant_id, name=name, slug=slug)
    db.add(db_tenant)
    db.commit()
    
    # Return onboarding token
    token = create_access_token(
        user_id="system",
        tenant_id=tenant_id,
        role="tenant-admin",
        permissions=["model:read", "model:write", "model:promote"]
    )
    return {"tenant_id": tenant_id, "onboarding_token": token}

@app.post("/api/v1/auth/login")
async def login(email: str, tenant_id: str):
    # Mocking user roles for testing Phase 2
    # In production, this would verify password and fetch from User table
    token = create_access_token(
        user_id=email,
        tenant_id=tenant_id,
        role="admin",
        permissions=["model:read", "model:write", "model:promote"]
    )
    return {"access_token": token, "token_type": "bearer"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "model-control-plane"}

@app.post("/api/v1/models")
@require_permission("model:write")
async def register_model(spec: ModelSpec, tenant_id: str = "", user_id: str = "", db: Session = Depends(get_db)):
    model_id = str(uuid.uuid4())
    db_model = Model(
        id=model_id,
        tenant_id=tenant_id,
        name=spec.name,
        version=spec.version,
        description=spec.description,
        framework=spec.framework,
        s3_uri=spec.s3_uri,
        status="REGISTERED"
    )
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    
    audit_log(db, user_id, tenant_id, "model:register", model_id)
    return {"message": "Model registered successfully", "data": db_model}

@app.get("/api/v1/models")
@require_permission("model:read")
async def list_models(tenant_id: str = "", db: Session = Depends(get_db)):
    # CRITICAL: Multi-tenant isolation
    models = db.query(Model).filter(Model.tenant_id == tenant_id).all()
    return {"models": models}

@app.get("/api/v1/models/{model_id}")
@require_permission("model:read")
async def get_model(model_id: str, tenant_id: str = "", db: Session = Depends(get_db)):
    model = db.query(Model).filter(Model.id == model_id, Model.tenant_id == tenant_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model

@app.put("/api/v1/models/{model_id}/status")
@require_permission("model:promote")
async def update_model_status(model_id: str, update: ModelStatusUpdate, tenant_id: str = "", user_id: str = "", db: Session = Depends(get_db)):
    model = db.query(Model).filter(Model.id == model_id, Model.tenant_id == tenant_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    valid_statuses = ["REGISTERED", "STAGING", "PRODUCTION", "ARCHIVED"]
    if update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of {valid_statuses}")
        
    model.status = update.status
    db.commit()
    
    audit_log(db, user_id, tenant_id, f"model:status_update:{update.status}", model_id)
    return {"message": "Status updated", "data": model}
