from sqlmodel import SQLModel, create_engine

engine = create_engine("postgresql://localhost/luna")

async def init_db() -> None:
    SQLModel.metadata.create_all(engine)
