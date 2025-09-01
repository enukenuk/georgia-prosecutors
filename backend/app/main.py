# backend/app/main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

from .database import get_db, wait_for_db
from .services.person_service import PersonService
from .config import settings

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up application...")
    try:
        wait_for_db()
        logger.info("Database is ready!")
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise
    yield
    logger.info("Shutting down application...")

app = FastAPI(
    title="Georgia Prosecutors API",
    description="API for managing prosecutors and their counties",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Test database connection
        result = db.execute(text("SELECT COUNT(*) FROM people"))
        count = result.scalar()
        return {
            "status": "healthy",
            "database": "connected",
            "people_count": count
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")

@app.get("/people/{person_id}")
def get_person(person_id: int, db: Session = Depends(get_db)):
    try:
        person_service = PersonService(db)
        person = person_service.get_person_by_id(person_id)
        if not person:
            raise HTTPException(status_code=404, detail="Person not found")
        return person
    except Exception as e:
        logger.error(f"Error getting person {person_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/counties/{county_id}/people")
def get_people_by_county(county_id: str, db: Session = Depends(get_db)):
    try:
        person_service = PersonService(db)
        return person_service.get_people_by_county(county_id)
    except Exception as e:
        logger.error(f"Error getting people for county {county_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/people/search")
def search_people(name: str, db: Session = Depends(get_db)):
    try:
        person_service = PersonService(db)
        return person_service.search_people_by_name(name)
    except Exception as e:
        logger.error(f"Error searching people with name '{name}': {e}")
        raise HTTPException(status_code=500, detail=str(e))