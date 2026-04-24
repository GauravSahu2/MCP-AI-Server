from sqlalchemy import Column, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from .base import Base
import uuid

# Role → Permission many-to-many
role_permissions = Table(
    "role_permissions", Base.metadata,
    Column("role_id", String, ForeignKey("roles.id")),
    Column("permission_id", String, ForeignKey("permissions.id"))
)

class Permission(Base):
    __tablename__ = "permissions"
    id   = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)

class Role(Base):
    __tablename__ = "roles"
    id          = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name        = Column(String, unique=True, nullable=False)
    permissions = relationship("Permission", secondary=role_permissions)

class Tenant(Base):
    __tablename__ = "tenants"
    id     = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name   = Column(String, unique=True, nullable=False)
    slug   = Column(String, unique=True, nullable=False)
    active = Column(Boolean, default=True)

class User(Base):
    __tablename__ = "users"
    id        = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email     = Column(String, unique=True, nullable=False)
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False)
    role_id   = Column(String, ForeignKey("roles.id"), nullable=False)
    role      = relationship("Role")
    tenant    = relationship("Tenant")
