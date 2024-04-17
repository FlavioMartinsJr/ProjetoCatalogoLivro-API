from Configs import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine(settings.DB_URL)

Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine
)


