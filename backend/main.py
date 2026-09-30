"""प्रगतीPath prototype API. Run: uvicorn main:app --reload  (from /backend)
Serves the dashboard at http://localhost:8000 and the REST API under /api."""
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from seed import CP, generate

app = FastAPI(title="प्रगतीPath API", version="0.1-prototype")
DB = {t["id"]: t for t in generate()}  # in-memory; production = PostgreSQL

RULES = {  # keyword placeholder for the NLP feedback classifier (production: trained model)
    "Low salary": ["salary", "pay", "wage", "paid", "stipend"],
    "Location / relocation": ["far", "distance", "relocat", "transfer", "commute", "city"],
    "Skill mismatch": ["skill", "not related", "different field", "irrelevant", "mismatch"],
    "Working conditions": ["hours", "condition", "unsafe", "boss", "overtime", "toxic"],
    "Family / personal": ["family", "marriage", "pregnan", "personal", "home"],
    "Discrimination": ["caste", "discriminat", "gender", "harass"],
}


class Checkpoint(BaseModel):
    m: int
    status: str
    wage: int = 0
    text: str = ""


class Verify(BaseModel):
    skill_feedback: str | None = None


class Text(BaseModel):
    text: str


def classify(text: str):
    t = text.lower()
    tags = [k for k, words in RULES.items() if any(w in t for w in words)]
    return {"primary": tags[0] if tags else ("Other" if t.strip() else None), "tags": tags}


def get(tid):
    if tid not in DB:
        raise HTTPException(404, "Trainee not found")
    return DB[tid]


@app.get("/api/health")
def health():
    return {"ok": True, "trainees": len(DB)}


@app.get("/api/trainees")
def trainees():
    return {"synthetic": True, "trainees": list(DB.values())}


@app.get("/api/trainees/{tid}")
def trainee(tid: str):
    return get(tid)


@app.post("/api/trainees/{tid}/checkpoint")
def add_checkpoint(tid: str, body: Checkpoint):
    t = get(tid)
    if not t["consent"]:
        raise HTTPException(403, "No consent on record")  # DPDP-style consent gate
    if body.m not in CP:
        raise HTTPException(422, f"m must be one of {CP}")
    c = {"m": body.m, "status": body.status, "wage": body.wage, "reason": classify(body.text)["primary"]}
    t["checkpoints"] = sorted([x for x in t["checkpoints"] if x["m"] != body.m] + [c], key=lambda x: x["m"])
    return t


@app.post("/api/trainees/{tid}/verify")
def verify(tid: str, body: Verify):
    t = get(tid)
    t["verification"] = "employer_verified"
    t["skill_feedback"] = body.skill_feedback
    return t


@app.post("/api/classify")
def classify_ep(body: Text):
    return classify(body.text)


FRONT = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/", StaticFiles(directory=FRONT, html=True), name="frontend")  # keep last
