from sqlalchemy.orm import Session
from database.models.profile import LinkedInProfile
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

class LinkedInProfileService:
    def __init__(self, db: Session):
        self.db = db

    def save_profile(self, profile_data: dict) -> LinkedInProfile:
        try:
            profile = LinkedInProfile(**profile_data)
            self.db.add(profile)
            self.db.commit()
            self.db.refresh(profile)
            return profile
        except SQLAlchemyError as e:
            logger.error("Error saving profile", exc_info=e)
            self.db.rollback()
            return None
    
    def profile_to_dict(self,profile: LinkedInProfile):
        return {
            "id": str(profile.id),
            "username": profile.username,
            "name": profile.name,
            "headline": profile.headline,
            "follower_count": profile.follower_count,
            "connection_count": profile.connection_count,
            "industry": profile.industry,
        }
    
    def get_profiles_by_name(self, username: str) -> list[LinkedInProfile]:
        try:
            
            profile = (
                self.db.query(LinkedInProfile)
                .filter(LinkedInProfile.username.ilike(f"%{username}%"))
                .all()
            )
            if len(profile) > 0:
                profile_dict = self.profile_to_dict(profile[0])
                print(profile_dict)
                return profile_dict
            else:
                return {}
        except SQLAlchemyError as e:
            logger.error("Error retrieving profiles", exc_info=e)
            return []
