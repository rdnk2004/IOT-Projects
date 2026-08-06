from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, Integer, Float, DateTime, String, Index
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
import config

Base = declarative_base()

class WeatherReading(Base):
    __tablename__ = "weather_readings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    temperature = Column(Float, nullable=False)               # °C
    apparent_temperature = Column(Float, nullable=True)       # °C
    humidity = Column(Float, nullable=True)                   # %
    wind_speed = Column(Float, nullable=True)                 # km/h
    weather_code = Column(Integer, nullable=True)             # WMO Code
    location = Column(String(50), default="Kochi, Kerala")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "formatted_time": self.timestamp.strftime("%Y-%m-%d %H:%M:%S") if self.timestamp else "",
            "temperature": round(self.temperature, 2) if self.temperature is not None else None,
            "apparent_temperature": round(self.apparent_temperature, 2) if self.apparent_temperature is not None else None,
            "humidity": round(self.humidity, 1) if self.humidity is not None else None,
            "wind_speed": round(self.wind_speed, 1) if self.wind_speed is not None else None,
            "weather_code": self.weather_code,
            "location": self.location
        }

engine = create_engine(config.DATABASE_URL, echo=False, pool_pre_ping=True)
SessionFactory = sessionmaker(bind=engine)
db_session = scoped_session(SessionFactory)

def init_db():
    """Initialize database schema tables."""
    Base.metadata.create_all(bind=engine)

def get_session():
    """Return a scoped database session."""
    return db_session()

def save_reading(timestamp, temperature, apparent_temperature=None, humidity=None, wind_speed=None, weather_code=None):
    """Save a weather reading into the database."""
    session = get_session()
    try:
        reading = WeatherReading(
            timestamp=timestamp,
            temperature=temperature,
            apparent_temperature=apparent_temperature,
            humidity=humidity,
            wind_speed=wind_speed,
            weather_code=weather_code
        )
        session.add(reading)
        session.commit()
        return reading.to_dict()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_latest_reading():
    """Get the most recent weather reading."""
    session = get_session()
    try:
        reading = session.query(WeatherReading).order_by(WeatherReading.timestamp.desc()).first()
        return reading.to_dict() if reading else None
    finally:
        session.close()

def get_readings_range(start_time=None, end_time=None, limit=1000):
    """Get weather readings between start_time and end_time."""
    session = get_session()
    try:
        query = session.query(WeatherReading)
        if start_time:
            query = query.filter(WeatherReading.timestamp >= start_time)
        if end_time:
            query = query.filter(WeatherReading.timestamp <= end_time)
        readings = query.order_by(WeatherReading.timestamp.asc()).limit(limit).all()
        return [r.to_dict() for r in readings]
    finally:
        session.close()
