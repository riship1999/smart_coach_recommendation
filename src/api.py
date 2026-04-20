from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.load_data import load_coaches
from src.matching_engine import rank_coaches_for_request, filter_candidates
from src.pricing_engine import recommend_price_for_coach

# These point to the built React frontend so FastAPI can serve it.
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIST_DIR = BASE_DIR / "frontend" / "dist"
FRONTEND_ASSETS_DIR = FRONTEND_DIST_DIR / "assets"
FRONTEND_INDEX_FILE = FRONTEND_DIST_DIR / "index.html"


app = FastAPI(title="Smart Coach Matching API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BasicEligibilityRequest(BaseModel):
    athlete_name: str
    city: str
    sport: str
    athlete_age: int
    budget_max: float
    radius_miles: float


class MatchRequest(BaseModel):
    athlete_name: str
    city: str
    sport: str
    athlete_age: int
    budget_max: float
    radius_miles: float
    lesson_type: str
    skill_level: str
    main_goal: str
    improvement_area: str
    prior_private_coaching: str
    coaching_style_preference: str
    lesson_frequency_intent: str


def get_coach_by_id(coaches_df, coach_id: int):
    matched = coaches_df[coaches_df["id"] == coach_id]
    if matched.empty:
        return None
    return matched.iloc[0]


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/eligible")
def get_eligible_coaches(payload: BasicEligibilityRequest):
    coaches_df = load_coaches()

    request_row = {
        "athlete_name": payload.athlete_name,
        "city": payload.city,
        "sport": payload.sport,
        "athlete_age": payload.athlete_age,
        "budget_max": payload.budget_max,
        "radius_miles": payload.radius_miles,
    }

    eligible_df = filter_candidates(request_row, coaches_df)

    eligible_list = []
    if not eligible_df.empty:
        eligible_df = eligible_df.sort_values(
            by="distance_miles", ascending=True
        ).reset_index(drop=True)

        for _, row in eligible_df.iterrows():
            eligible_list.append(
                {
                    "coach_id": int(row["id"]),
                    "coach_name": row["name"],
                    "sport": row["sport"],
                    "specialty": row["specialty"],
                    "city": row["city"],
                    "hourly_price": float(row["hourly_price"]),
                    "distance_miles": round(float(row["distance_miles"]), 2),
                    "avg_rating": float(row["avg_rating"]),
                    "years_experience": int(row["years_experience"]),
                }
            )

    return {
        "request": request_row,
        "eligible_count": int(len(eligible_df)),
        "eligible_coaches": eligible_list,
        "message": (
            "Eligible coaches found."
            if len(eligible_df) > 0
            else "No coaches passed the basic eligibility filters."
        ),
    }


@app.post("/api/match")
def match_live_request(payload: MatchRequest):
    coaches_df = load_coaches()

    request_row = {
        "athlete_name": payload.athlete_name,
        "city": payload.city,
        "sport": payload.sport,
        "athlete_age": payload.athlete_age,
        "budget_max": payload.budget_max,
        "radius_miles": payload.radius_miles,
        "lesson_type": payload.lesson_type,
        "skill_level": payload.skill_level,
        "main_goal": payload.main_goal,
        "improvement_area": payload.improvement_area,
        "prior_private_coaching": payload.prior_private_coaching,
        "coaching_style_preference": payload.coaching_style_preference,
        "lesson_frequency_intent": payload.lesson_frequency_intent,
    }

    ranked_results = rank_coaches_for_request(request_row, coaches_df)

    if ranked_results.empty:
        return {
            "request": request_row,
            "matches": [],
            "message": "No matching coaches found for the current search criteria.",
        }

    return {
        "request": request_row,
        "matches": ranked_results.head(3).to_dict(orient="records"),
    }


@app.get("/api/coaches/{coach_id}/pricing")
def get_pricing_for_coach(coach_id: int):
    coaches_df = load_coaches()
    coach_row = get_coach_by_id(coaches_df, coach_id)

    if coach_row is None:
        raise HTTPException(status_code=404, detail="Coach not found")

    return recommend_price_for_coach(coach_row)


if FRONTEND_ASSETS_DIR.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_ASSETS_DIR), name="assets")


@app.get("/{full_path:path}")
def serve_frontend(full_path: str):
    if FRONTEND_INDEX_FILE.exists():
        return FileResponse(FRONTEND_INDEX_FILE)
    return {
        "message": "Frontend build not found. Run 'npm run build' inside the frontend folder."
    }