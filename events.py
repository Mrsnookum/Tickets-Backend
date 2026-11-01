from fastapi import APIRouter, HTTPException
from database import supabase
from schemas import EventCreate

router = APIRouter()

@router.post("/")
async def create_event(payload: EventCreate):
    # 1. Look up the marketplace UUID using the slug
    market_res = supabase.table("marketplaces").select("id").eq("slug", payload.marketplace_id).execute()
    if not market_res.data:
        raise HTTPException(status_code=404, detail="Marketplace not found")
    market_uuid = market_res.data[0]["id"]

    # 2. Insert the Event
    event_data = {
        "marketplace_id": market_uuid,
        "title": payload.title,
        "venue": payload.venue,
        "event_date": payload.event_date.isoformat(),
        "event_time": payload.event_time.isoformat(),
        "poster_url": payload.poster_url,
        "status": payload.status
    }
    event_res = supabase.table("events").insert(event_data).execute()
    new_event_id = event_res.data[0]["id"]

    # 3. Insert the Tickets
    tickets_data = []
    for t in payload.tickets:
        tickets_data.append({
            "event_id": new_event_id,
            "marketplace_id": market_uuid,
            "category": t.category,
            "price": t.price,
            "quantity": t.quantity,
            "status": t.status
        })
    supabase.table("tickets").insert(tickets_data).execute()

    return {"status": "success", "event_id": new_event_id}

@router.get("/marketplace/{slug}")
async def get_marketplace_events(slug: str):
    # Look up marketplace UUID
    market_res = supabase.table("marketplaces").select("id").eq("slug", slug).execute()
    if not market_res.data:
        raise HTTPException(status_code=404, detail="Marketplace not found")
    market_uuid = market_res.data[0]["id"]

    # Fetch published events and their linked tickets
    events_res = supabase.table("events").select(
        "*, tickets(*)"
    ).eq("marketplace_id", market_uuid).eq("status", "published").execute()
    
    return events_res.data

@router.get("/")
async def get_all_events():
    # Fetch all events across all marketplaces for the admin dashboard
    events_res = supabase.table("events").select("*, tickets(*)").execute()
    return events_res.data

@router.delete("/{event_id}")
async def delete_event(event_id: str):
    # Deleting the event automatically deletes associated tickets due to CASCADE
    res = supabase.table("events").delete().eq("id", event_id).execute()
    
    if not res.data:
        raise HTTPException(status_code=404, detail="Event not found or already deleted")
        
    return {"status": "success", "deleted_id": event_id}