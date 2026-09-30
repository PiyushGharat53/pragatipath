"""Synthetic data generator for the प्रगतीPath prototype.
All people are fictional. Run `python seed.py` to write ../frontend/data.json
(used by the static GitHub Pages demo)."""
import json
import random
from pathlib import Path

CP = [3, 6, 12, 18, 24]
POS = ("employed", "self_employed", "apprentice")
DISTRICTS = {"Pune": 1.15, "Mumbai": 1.25, "Thane": 1.1, "Nagpur": 1.0, "Nashik": .95,
             "Chh. Sambhajinagar": .95, "Kolhapur": .9, "Solapur": .85}
# course: (base monthly wage, P(placed), P(stay per checkpoint), P(self-employed | placed), P(job related))
COURSES = {"Electrician": (16000, .72, .9, .12, .85), "Tailoring": (9000, .55, .8, .45, .9),
           "Retail Sales": (12000, .8, .68, .03, .5), "Data Entry Operator": (13000, .65, .75, .05, .55),
           "Welding Technician": (17000, .7, .88, .1, .85), "Hospitality Assistant": (11000, .78, .7, .05, .6),
           "Solar PV Installer": (15000, .6, .85, .15, .8)}
PROVIDERS = {"Sahyadri Skills": 1.05, "Deccan Vocational": .95, "Konkan Institute": 1.0,
             "Vidarbha Tech Academy": .9, "Godavari Training Hub": 1.02, "Maharashtra Skill Works": .85}
LEAVE = {"Low salary": 4, "Skill mismatch": 3, "Working conditions": 3, "Location / relocation": 3,
         "Family / personal": 2, "Discrimination": 1}
FIRST = ["Rahul", "Sneha", "Amit", "Pooja", "Vikas", "Anjali", "Suresh", "Kavita", "Nitin", "Priya", "Sagar", "Megha"]
LAST = ["Patil", "Jadhav", "Shinde", "Pawar", "More", "Kale", "Deshmukh", "Gaikwad", "Kulkarni", "Chavan"]
PROGS = [("PMKVY", "A"), ("Mahaswayam", "B"), ("DDU-GKY", "D"), ("ITI", "")]


def make(i):
    d = random.choice(list(DISTRICTS)); c = random.choice(list(COURSES)); p = random.choice(list(PROVIDERS))
    base, pp, stay, sp, rel = COURSES[c]; dm = DISTRICTS[d]; pq = PROVIDERS[p]
    months = random.choice([3, 6, 6, 12, 12, 18, 24])
    related = random.random() < rel * min(pq, 1.05)
    ver = random.choices(["reported", "employer_verified", "registry_matched"], [5, 3, 2])[0]
    prev, wage, cps = None, 0, []
    for m in CP:
        if m > months:
            break
        if random.random() < .08:
            cps.append({"m": m, "status": "no_response", "wage": 0, "reason": None})
            continue
        reason = None
        if prev in POS:
            if random.random() < min(.96, stay * pq + .05):
                st = prev
            else:
                st = "unemployed"
                reason = random.choices(list(LEAVE), list(LEAVE.values()))[0]
        else:
            if random.random() < min(.95, pp * dm * pq):
                st = "self_employed" if random.random() < sp else ("apprentice" if random.random() < .1 else "employed")
            else:
                st = "unemployed"
                reason = "No suitable openings" if random.random() < .5 else random.choices(list(LEAVE), list(LEAVE.values()))[0]
        if st in POS:
            if st == prev and wage:
                wage = int(round(wage * (1 + random.uniform(-.02, .1)), -2))
            else:
                f = {"employed": random.uniform(.85, 1.15), "self_employed": random.uniform(.7, 1.3), "apprentice": .5}[st]
                wage = int(round(base * dm * f, -2))
        else:
            wage = 0
        cps.append({"m": m, "status": st, "wage": wage, "reason": reason})
        prev = st

    last = next((x for x in reversed(cps) if x["status"] != "no_response"), None)
    risk, why = .1, []
    if last and last["status"] == "unemployed":
        risk, why = .8, ["Currently unemployed"]
    elif last:
        if last["status"] == "employed" and last["wage"] < base * dm * .9:
            risk += .25; why.append("Wage below course/district norm")
        if not related:
            risk += .25; why.append("Training-job mismatch")
        if ver == "reported":
            risk += .1; why.append("Employment not verified")
        if months <= 6:
            risk += .1; why.append("Early-tenure window")
    if any(x["status"] == "no_response" for x in cps):
        risk += .1; why.append("Missed follow-up")

    f, l = random.choice(FIRST), random.choice(LAST)
    variants = [f"{f} {l}", f"{l} {f} {random.choice('ASKMP')}.", f"{f.upper()} {l.upper()}"]
    dob = f"{random.randint(1996, 2005)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
    records = []
    for (prog, pre), nm in zip(random.sample(PROGS, random.choice([1, 2, 2, 3])), variants):
        records.append({"programme": prog, "id": f"{pre}{random.randint(100, 999)}" if pre else str(random.randint(1000, 9999)), "name": nm})
    return {"id": f"KS-{i:04d}", "name": f"{f} {l}", "dob": dob, "district": d, "course": c, "provider": p,
            "months_since_cert": months, "consent": True, "related": related, "verification": ver,
            "skill_feedback": None, "records": records, "checkpoints": cps,
            "risk": round(min(risk, .95), 2), "risk_factors": why}


def generate(n=260, seed=42):
    random.seed(seed)
    return [make(i + 1) for i in range(n)]


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "frontend" / "data.json"
    out.write_text(json.dumps({"synthetic": True, "trainees": generate()}))
    print("wrote", out)