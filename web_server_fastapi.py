from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from resources import EntryManager, Entry
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # разрешает все источники (для разработки)
    allow_credentials=True,
    allow_methods=["*"],  # разрешает все методы (GET, POST и т.д.)
    allow_headers=["*"],  # разрешает все заголовки
)

ENTRIES_FOLDER = os.path.join(os.path.dirname(__file__), 'entries_bank')
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/entries/")
async def get_entries():
    entry_manager = EntryManager(ENTRIES_FOLDER)
    entry_manager.load()
    entries_list = [entry.json() for entry in entry_manager.entries]
    return entries_list



@app.post("/api/save_entries/")
async def save_entries(request: Request):
    entry_manager = EntryManager(ENTRIES_FOLDER)
    data = await request.json()
    for entry_data in data:
        entry = Entry.from_json(entry_data)
        entry_manager.entries.append(entry)
    entry_manager.save()
    return {'status': 'done'}