import uuid

from sqlalchemy import Boolean, Column, String, ForeignKey, Table, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.database import Base

user_roles = Table('user_roles', Base.metadata,
                   Column('user_id', UUID(as_uuid=True), ForeignKey('users.id', ondelete="CASCADE")),
                   Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id', ondelete="CASCADE"))
                   )

user_oauth = Table('user_oauth', Base.metadata,
                   Column('user_id', UUID(as_uuid=True), ForeignKey('users.id', ondelete="CASCADE")),
                   Column('oauth_id', UUID(as_uuid=True), ForeignKey('oauth.id', ondelete="CASCADE"))
                   )


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    login_history = relationship("LoginHistory", back_populates="user", cascade="all, delete-orphan")
    oauth = relationship("Oauth", secondary=user_oauth, back_populates="user")


class LoginHistory(Base):
    __tablename__ = "loginhistory"
    __table_args__ = {
        'postgresql_partition_by': 'RANGE (login_at)',
    }

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete="CASCADE"))
    user = relationship('User', back_populates='login_history')
    ip_address = Column(String)
    user_agent = Column(String)
    login_at = Column(DateTime, primary_key=True, default=func.now())


class Oauth(Base):
    # todo один ко многим - не успел
    __tablename__ = "oauth"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    user = relationship('User', secondary="user_oauth", back_populates='oauth')
    provider = Column(String, nullable=True)
    provider_user_id = Column(String, nullable=True, unique=True)
