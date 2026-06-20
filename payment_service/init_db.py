from payment_service.database import engine
from payment_service.models import Base

Base.metadata.create_all(bind=engine)

print("Database tables created")