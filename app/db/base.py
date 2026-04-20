from sqlalchemy.orm import declarative_base

Base = declarative_base()

# import models here so Alembic (later) can detect them
from app.models.contact import Contact
from app.models.consultation import Consultation
from app.models.product import Product
from app.models.service import Service
from app.models.tip import Tip
from app.models.faq import FAQ
from app.models.success_story import SuccessStory
from app.models.profile import Profile