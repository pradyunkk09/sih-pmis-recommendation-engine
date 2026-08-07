from sqlalchemy.orm import declarative_base


# Base stores SQLAlchemy's shared model metadata. Every future ORM model should
# inherit from this object so SQLAlchemy can discover all table definitions from
# one consistent registry when migrations or metadata operations are added.
Base = declarative_base()
