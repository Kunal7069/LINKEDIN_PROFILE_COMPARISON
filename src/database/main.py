from database.config.config import SessionLocal, engine
from database.models.base import Base  # Correct: central Base class
import database.models  # This is needed to register all models

from database.services.post_service import LinkedInPostService
from database.services.profile_service import LinkedInProfileService
from database.models import post 
# ✅ Create all tables if they do not exist
Base.metadata.create_all(bind=engine)

# ✅ Start DB session
db = SessionLocal()

# ✅ Initialize services
post_service = LinkedInPostService(db)
profile_service = LinkedInProfileService(db)

# ✅ Expose services for use in other parts
services = {
    "post_service": post_service,
    "profile_service":profile_service
}

# ✅ Clean shutdown
def close_db():
    db.close()
