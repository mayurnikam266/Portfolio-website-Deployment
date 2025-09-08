from fastapi import FastAPI, Depends
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, init_models
from models import Contact
import logging

# Logging setup
logging.basicConfig(filename="app.log", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize FastAPI
app = FastAPI(title="Mayur Nikam Portfolio API")

# CORS
origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://100.26.45.235"  # your public IP if frontend accesses via IP
]
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

# Startup: initialize tables
@app.on_event("startup")
async def on_startup():
    await init_models()
    logging.info("Database initialized successfully")

# Health check
@app.get("/")
async def read_root():
    return {"status": "API is running"}

# Contact endpoint (fixed async session)
@app.post("/contact")
async def handle_contact_form(form_data: ContactForm, session: AsyncSession = Depends(get_db)):
    async with session as db:
        contact = Contact(
            name=form_data.name,
            email=form_data.email,
            message=form_data.message
        )
        db.add(contact)
        await db.commit()
        logging.info(f"New contact submitted: {form_data}")
        return {"message": "Thank you! Your message has been received."}

