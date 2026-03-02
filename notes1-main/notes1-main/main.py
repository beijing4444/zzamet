import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
import os
notes = [
    {
        "id": 1,
        "title": "Азбука",
        "content": "Развивающий",
    },
    {
        "id": 2,
        "title": "AAA",
        "content": "123",
    }
]

# FILE_NAME = "new.json"
#
# def load_notes():
#     if not os.path.exists(FILE_NAME):
#         return [    {
#         "id": 1,
#         "title": "Азбука",
#         "content": "Развивающий",
#     }]
#     with open(FILE_NAME,"r", encoding="utf-8") as f:
#         return json.load(f)
#
# def save_notes(notes):
#     with open(FILE_NAME,"w", encoding="utf-8") as f:
#         json.dump(notes,f, ensure_ascii=False, indent=4)
#
# notes = load_notes()


app = FastAPI()



@app.get("/")
async def main():
    return FileResponse("new.html")

@app.get("/search_notes.html")
async def main():
    return FileResponse("search_notes.html")

@app.get("/add_notes.html")
async def main():
    return FileResponse("add_notes.html")

@app.get("/delete_notes")
async def main():
    return FileResponse("delete_notes.html")


@app.get("/notes", tags=["Заметки"])
def read_all_notes():
    return notes

@app.get("/notes/{id}", tags=["Выбор заметок"])
def read_note(id: int):
    for note in notes:
        if note["id"] == id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")

class NewNote(BaseModel):
    title: str
    content: str

@app.post("/notes", tags=["Добавить в заметки"])
def create_note(note: NewNote):
    notes.append(
        {
            "id": len(notes) + 1,
            "title": note.title,
            "content": note.content,
        }
    )
    return {"success": True}


@app.delete("/notes/{note_id}")
async def delete_note(note_id: int):
    if note_id not in notes:
        return {"error": "Item not found"}
    del notes[note_id]
    return {"message": "Note deleted successfully"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)