from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime as dt

class Base(DeclarativeBase):
    pass

class TronAddressQuery(Base):
    __tablename__ = "tron_addresses"

    id = Column(Integer, primary_key=True, index=True)
    
    address = Column(String(34), nullable=False, unique=True, index=True) # Адрес кошелька Tron - это уникальная последовательность цифр и букв, используемая для получения токенов TRX
    bandwidth = Column(Float, nullable=False) # "Пропускная способность" определяет, сколько данных (в байтах) можно передать в сети за транзакцию
    energy = Column(Float, nullable=False) # "Энергия" - это вычислительный ресурс для выполнения смарт-контрактов
    balance_trx = Column(Float, nullable=False) # "TRX" - основная криптовалюта блокчейна TRX
    
    created_at = Column(DateTime, nullable=False, default=dt.utcnow)


    