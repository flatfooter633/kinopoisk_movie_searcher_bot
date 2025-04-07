from sqlalchemy import BigInteger, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

# Create the database engine
engine = create_async_engine(url="sqlite+aiosqlite:///database//db.sqlite3")

# Create the async session
async_session = async_sessionmaker(engine)


# Define the base class for the database model
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )


# Define the User model
class User(Base):
    __tablename__ = "users"

    tg_id = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str] = mapped_column(String(25), nullable=False)
    last_name: Mapped[str] = mapped_column(String(25))


# Define the Request model
class Request(Base):
    __tablename__ = "requests"

    search_date = mapped_column(DateTime)
    movie_id: Mapped[int] = mapped_column(nullable=False)
    movie_name: Mapped[str] = mapped_column(String(120), nullable=False)
    movie_description: Mapped[str] = mapped_column()
    rating: Mapped[int] = mapped_column()
    year: Mapped[int] = mapped_column()
    genre: Mapped[str] = mapped_column(String(25))
    age_rating: Mapped[int] = mapped_column(nullable=True)
    poster_url: Mapped[str] = mapped_column()
    movie_viewed = mapped_column(Boolean, nullable=True)
    movie_favorite = mapped_column(Boolean, nullable=True)
    tg_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"))


# Create tables in the database
async def async_main():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
