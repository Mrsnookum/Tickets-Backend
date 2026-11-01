from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import events

app = FastAPI(title="Multi-Marketplace API")

# Allow frontend HTML files to make requests to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(events.router, prefix="/api/events", tags=["Events"])

@app.get("/")
def read_root():
    return {"status": "online", "system": "Ticket Management Engine"}