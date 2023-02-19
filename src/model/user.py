import bcrypt
import jwt
from uuid import uuid4
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..config import Config
from ..database.pg import Base, PG
from ..utils.time import current_timestamp

class User(Base):
    __tablename__ = "users"

    email = Column(String, unique=True, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    created_at = Column(Integer)
    # items = relationship("Item", back_populates="owner")

    def find(email: str):
        return PG.query(User).filter_by(email=email).first()
    
    def create(email: str, first_name: str, last_name: str, raw_password: str):
        exs = User.find(email)
        if exs:
            return None

        # Encrypt password using bcrypt
        hashed = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
        pwd = hashed.decode('utf-8')

        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=pwd,
            created_at=current_timestamp()
        )
        PG.add(user)
        PG.commit()
        PG.refresh(user)
        return user
    
    def verify_password(self, raw_password: str):
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))
    
    def from_jwt(self, token: str):
        try:
            claims = jwt.decode(token, Config.JWT_SECRET, algorithms=['HS256'])
            if claims['exp'] < current_timestamp():
                return None
            return User.find(claims['sub'])
        except:
            return None
    
    def issue_jwt(self, duration: int = 86400):
        ts = current_timestamp()
        claims: dict = {
            'iss': 'github.com/krissukoco/python-fastapi-simple',
            'sub': self.email,
            'aud': 'github.com/krissukoco/python-fastapi-simple',
            'iat': ts,
            'exp': ts + duration,
            'nbf': ts,
            'jti': uuid4().hex,
        }
        enc: str = jwt.encode(claims, Config.JWT_SECRET, algorithm='HS256')
        return enc

# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     # owner_id = Column(Integer, ForeignKey("users.email"))
#     # owner = relationship("User", back_populates="items")