from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List
import strawberry
from strawberry.fastapi import GraphQLRouter
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request

# Import your models & DB
from .models import User, UserCreate
from .database import get_session, engine, create_db_and_tables

app = FastAPI(title="Backend Practice API")

# Rate limiting (security best practice)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS for future frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup (dev only)
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()  # Runs on startup
    yield  # App runs here
    # Optional: cleanup code on shutdown
app = FastAPI(title="Backend Practice API", lifespan=lifespan)

# REST Endpoints
@app.get("/users", response_model=List[User])
def get_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()

@app.post("/users", response_model=User, status_code=201)
@limiter.limit("5/minute")  # Keep this line
def create_user(
    request: Request,               # <-- Add this
    user: UserCreate,
    session: Session = Depends(get_session)
):
    db_user = User(**user.dict())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

# GraphQL Setup
@strawberry.type
class Query:
    @strawberry.field
    def users(self, info: strawberry.types.Info) -> List[User]:
        session = info.context["session"]
        return session.exec(select(User)).all()

schema = strawberry.Schema(query=Query)
graphql_router = GraphQLRouter(
    schema,
    context_getter=lambda: {"session": next(get_session())}
)

app.include_router(graphql_router, prefix="/graphql")