from sqlalchemy.orm import Mapped, mapped_column
from app.models import Base

class Blog(Base):
    __tablename__ = "blogs"
    
    title: Mapped[str]
    description: Mapped[str]