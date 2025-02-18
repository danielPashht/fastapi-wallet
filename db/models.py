from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)


class Wallet(Base):
    __tablename__ = 'wallet'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    strategies = Column(String, default='{}')
    user = relationship('User')
    assets = relationship('Asset', back_populates='wallet')


class Asset(Base):
    __tablename__ = 'asset'
    symbol = Column(Integer, primary_key=True, index=True, unique=True)
    balance = Column(Float)
    usd_price = Column(Float)
    average_buy_price_usd = Column(Float, default=0.0)

    wallet_id = Column(Integer, ForeignKey('wallet.user_id'))
    wallet = relationship('Wallet', back_populates='assets')
