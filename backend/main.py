from fastapi import FastAPI, Depends
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, engine, init_models
from models import Contact
import logging
import asyncio

# Logging setup
logging.basicConfig(filename="app.log", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize FastAPI
app = FastAPI(title="Mayur Nikam Portfolio API")

# CORS (allow frontend domain served via Nginx)
origins = [
    "http://localhost",
    "http://127.0.0.1"
   
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for contact form
class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str

# Startup event: initialize database tables
@app.on_event("startup")
async def on_startup():
    await init_models()
    logging.info("Database initialized successfully")

# Health check route
@app.get("/")
async def read_root():
    return {"status": "API is running"}

# Contact form endpoint
@app.post("/contact")
async def handle_contact_form(form_data: ContactForm, db: AsyncSession = Depends(get_db)):
    contact = Contact(
        name=form_data.name,
        email=form_data.email,
        message=form_data.message
    )
    db.add(contact)
    await db.commit()
    logging.info(f"New contact submitted: {form_data}")
    return {"message": "Thank you! Your message has been received."}
