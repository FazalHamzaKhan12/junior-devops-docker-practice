import os
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Boolean, DateTime, Integer, String, create_engine, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker


DB_HOST = os.getenv("DB_HOST", "mysql")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "taskuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "task123")
DB_NAME = os.getenv("DB_NAME", "taskdb")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    completed: bool
    created_at: datetime


def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Company Task API",
    description="DEVOPS-106 FastAPI and MySQL Docker Compose practice project.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/", tags=["Service"])
def root():
    return {
        "service": "Company Task API",
        "status": "running",
        "documentation": "/docs",
    }


@app.get("/health", tags=["Service"])
def health(database: Session = Depends(get_db)):
    try:
        database.execute(text("SELECT 1"))
        return {
            "api": "healthy",
            "database": "connected",
            "project": "DEVOPS-106",
        }
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable",
        ) from error


@app.post(
    "/tasks",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Tasks"],
)
def create_task(payload: TaskCreate, database: Session = Depends(get_db)):
    title = payload.title.strip()
    if not title:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Task title cannot be blank",
        )

    task = Task(title=title)
    database.add(task)
    database.commit()
    database.refresh(task)
    return task


@app.get("/tasks", response_model=list[TaskRead], tags=["Tasks"])
def list_tasks(database: Session = Depends(get_db)):
    return database.query(Task).order_by(Task.id.desc()).all()


@app.patch(
    "/tasks/{task_id}/complete",
    response_model=TaskRead,
    tags=["Tasks"],
)
def complete_task(task_id: int, database: Session = Depends(get_db)):
    task = database.get(Task, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    task.completed = True
    database.commit()
    database.refresh(task)
    return task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Tasks"],
)
def delete_task(task_id: int, database: Session = Depends(get_db)):
    task = database.get(Task, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    database.delete(task)
    database.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
