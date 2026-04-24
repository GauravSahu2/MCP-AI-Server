import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.rbac import Tenant, Role, User, Permission
from auth.jwt import create_access_token
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./aegis.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def bootstrap():
    db = SessionLocal()
    
    # 1. Create Super Admin Tenant
    tenant_id = str(uuid.uuid4())
    super_admin_tenant = Tenant(
        id=tenant_id,
        name="Super Admin",
        slug="super-admin"
    )
    db.add(super_admin_tenant)
    
    # 2. Create Admin Role
    admin_role = Role(
        id=str(uuid.uuid4()),
        name="admin"
    )
    db.add(admin_role)
    
    # 3. Create initial Permissions
    perms = ["model:read", "model:write", "model:promote", "tenant:admin"]
    for p_name in perms:
        p = Permission(name=p_name)
        db.add(p)
        admin_role.permissions.append(p)
        
    db.commit()
    
    # 4. Generate Super Admin Token
    token = create_access_token(
        user_id="admin@aegis.ai",
        tenant_id=tenant_id,
        role="admin",
        permissions=perms
    )
    
    print("======================================================")
    print("AEGIS BOOTSTRAP SUCCESSFUL")
    print(f"Tenant ID: {tenant_id}")
    print(f"Super Admin JWT: {token}")
    print("======================================================")
    
    # Save token to a file for easy retrieval by other phases
    with open("bootstrap_token.txt", "w") as f:
        f.write(token)
    
    db.close()

if __name__ == "__main__":
    bootstrap()
