from fastapi import FastAPI, Depends
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal, engine, Base
from models import Contact
import logging
import asyncio

# Logging setup
logging.basicConfig(filename="app.log", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize FastAPI
app = FastAPI(title="Jasraj Singh Portfolio API")

# CORS
origins = ["http://localhost", "http://127.0.0.1"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model
class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str

# Dependency to get DB session
async def get_db():
    async with SessionLocal() as session:
        yield session

# Create tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_db())

@app.get("/")
async def read_root():
    return {"status": "API is running"}

@app.post("/contact")
async def handle_contact_form(form_data: ContactForm, db: AsyncSession = Depends(get_db)):
    contact = Contact(name=form_data.name, email=form_data.email, message=form_data.message)
    db.add(contact)
    await db.commit()
    logging.info(f"New contact submitted: {form_data}")
    return {"message": "Thank you! Your message has been received."}
