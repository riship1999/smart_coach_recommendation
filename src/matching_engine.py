import math
import pandas as pd
from src.load_data import load_coaches


""" 
These constants allow the engine to score:

    exact fit
    near fit
    instead of only yes/no matching.

This is what makes the recommendation more flexible. 
"""
CITY_COORDINATES = {
    "Dallas": {"latitude": 32.7767, "longitude": -96.7970},
    "Austin": {"latitude": 30.2672, "longitude": -97.7431},
    "Houston": {"latitude": 29.7604, "longitude": -95.3698},
    "Oklahoma City": {"latitude": 35.4676, "longitude": -97.5164},
    "Norman": {"latitude": 35.2226, "longitude": -97.4395},
    "Tulsa": {"latitude": 36.1540, "longitude": -95.9928},
}

GOAL_RELATED = {
    "build_fundamentals": ["build_confidence", "improve_technique"],
    "improve_technique": ["prepare_for_tryouts", "improve_game_performance", "build_fundamentals"],
    "prepare_for_tryouts": ["improve_game_performance", "improve_technique"],
    "build_confidence": ["build_fundamentals", "improve_game_performance"],
    "improve_game_performance": ["improve_technique", "prepare_for_tryouts", "build_confidence"],
    "strength_speed_development": ["improve_game_performance"],
}

IMPROVEMENT_RELATED = {
    "pitching_control": ["pitching_velocity", "throwing_accuracy", "confidence_under_pressure"],
    "pitching_velocity": ["pitching_control", "throwing_accuracy"],
    "swing_consistency": ["contact_hitting", "confidence_under_pressure"],
    "contact_hitting": ["swing_consistency", "confidence_under_pressure"],
    "fielding_footwork": ["reaction_speed", "throwing_accuracy"],
    "catching_mechanics": ["throwing_accuracy", "confidence_under_pressure"],
    "throwing_accuracy": ["pitching_control", "fielding_footwork", "catching_mechanics"],
    "reaction_speed": ["fielding_footwork", "throwing_accuracy"],
    "confidence_under_pressure": ["pitching_control", "swing_consistency", "catching_mechanics"],
}

STYLE_RELATED = {
    "patient_step_by_step": ["high_energy_motivation"],
    "direct_technical_feedback": ["game_situation_coaching"],
    "high_energy_motivation": ["patient_step_by_step", "drill_heavy_practice"],
    "drill_heavy_practice": ["high_energy_motivation", "game_situation_coaching"],
    "game_situation_coaching": ["direct_technical_feedback", "drill_heavy_practice"],
}

FREQUENCY_RELATED = {
    "one_time_trial": ["occasional"],
    "occasional": ["one_time_trial", "weekly_long_term"],
    "weekly_long_term": ["occasional"],
}

RELATED_SPECIALTIES = {
    "pitching": ["pitching"],
    "hitting": ["hitting"],
    "catching": ["catching"],
    "infield": ["infield", "fielding"],
    "outfield": ["outfield", "fielding"],
    "fielding": ["fielding", "infield", "outfield"],
    "strength_and_conditioning": ["strength_and_conditioning", "speed_and_agility"],
    "speed_and_agility": ["speed_and_agility", "strength_and_conditioning"],
}


def parse_pipe_list(value) -> list:
    if value is None:
        return []
    text = str(value).strip()
    if not text:
        return []
    return [item.strip() for item in text.split("|") if item.strip()]


def to_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def humanize(text: str) -> str:
    return str(text).replace("_", " ")


def haversine_miles(lat1, lon1, lat2, lon2):
    # Computes geographic distance between two coordinates.
    r = 3958.8

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return r * c


def get_city_coordinates(city: str):
    if city not in CITY_COORDINATES:
        raise ValueError(f"Unsupported city: {city}")
    return CITY_COORDINATES[city]


def filter_candidates(request_row: dict, coaches_df: pd.DataFrame) -> pd.DataFrame:
    sport = request_row["sport"]
    city = request_row["city"]
    budget_max = float(request_row["budget_max"])
    radius_miles = float(request_row["radius_miles"])

    coords = get_city_coordinates(city)
    request_lat = coords["latitude"]
    request_lng = coords["longitude"]

    filtered = coaches_df[coaches_df["sport"] == sport].copy()

    filtered["distance_miles"] = filtered.apply(
        lambda row: haversine_miles(
            request_lat,
            request_lng,
            float(row["latitude"]),
            float(row["longitude"]),
        ),
        axis=1,
    )

    filtered = filtered[filtered["distance_miles"] <= radius_miles].copy()
    filtered = filtered[filtered["hourly_price"] <= budget_max * 1.30].copy()

    return filtered.reset_index(drop=True)


def compute_lesson_type_fit(request_row: dict, coach_row: pd.Series) -> float:
    lesson_type = request_row["lesson_type"]
    coach_specialty = coach_row["specialty"]

    if lesson_type == coach_specialty:
        return 1.0

    related = RELATED_SPECIALTIES.get(lesson_type, [lesson_type])
    if coach_specialty in related:
        return 0.6

    return 0.0


def compute_goal_fit(request_row: dict, coach_row: pd.Series) -> float:
    main_goal = request_row["main_goal"]
    supported_goals = parse_pipe_list(coach_row["goals_supported"])

    if main_goal in supported_goals:
        return 1.0

    related_goals = GOAL_RELATED.get(main_goal, [])
    if any(goal in supported_goals for goal in related_goals):
        return 0.5

    return 0.0


def compute_pain_point_fit(request_row: dict, coach_row: pd.Series) -> float:
    improvement_area = request_row["improvement_area"]
    supported_areas = parse_pipe_list(coach_row["improvement_areas_supported"])

    if improvement_area in supported_areas:
        return 1.0

    related_areas = IMPROVEMENT_RELATED.get(improvement_area, [])
    if any(area in supported_areas for area in related_areas):
        return 0.5

    return 0.0


def compute_skill_fit(request_row: dict, coach_row: pd.Series) -> float:
    skill_level = request_row["skill_level"]
    preferred_levels = parse_pipe_list(coach_row["preferred_athlete_levels"])
    beginner_friendly = to_bool(coach_row["beginner_friendly"])

    if skill_level in preferred_levels:
        base = 1.0
    elif skill_level == "beginner":
        base = 0.75 if beginner_friendly else 0.20
    elif skill_level == "intermediate":
        base = 0.60 if ("beginner" in preferred_levels or "advanced" in preferred_levels) else 0.20
    elif skill_level == "advanced":
        base = 0.45 if "intermediate" in preferred_levels else 0.10
    else:
        base = 0.20

    return round(base, 3)


def compute_coaching_style_fit(request_row: dict, coach_row: pd.Series) -> float:
    preferred_style = request_row["coaching_style_preference"]
    coach_style = str(coach_row["coaching_style"]).strip()

    if preferred_style == coach_style:
        return 1.0

    related_styles = STYLE_RELATED.get(preferred_style, [])
    if coach_style in related_styles:
        return 0.45

    return 0.0


def compute_reliability_fit(coach_row: pd.Series) -> float:
    completion_rate = float(coach_row["completion_rate"])
    response_rate = float(coach_row["response_rate"])
    repeat_booking_rate = float(coach_row["repeat_booking_rate"])
    cancellation_rate = float(coach_row["cancellation_rate"])

    score = (
        0.45 * completion_rate
        + 0.25 * response_rate
        + 0.20 * repeat_booking_rate
        + 0.10 * (1 - cancellation_rate)
    )
    return round(score, 3)


def compute_commitment_fit(request_row: dict, coach_row: pd.Series) -> float:
    frequency_intent = request_row["lesson_frequency_intent"]
    coach_fit = parse_pipe_list(coach_row["lesson_frequency_fit"])

    if frequency_intent in coach_fit:
        return 1.0

    related = FREQUENCY_RELATED.get(frequency_intent, [])
    if any(item in coach_fit for item in related):
        return 0.5

    return 0.0


def compute_price_comfort(request_row: dict, coach_row: pd.Series) -> float:
    budget_max = float(request_row["budget_max"])
    hourly_price = float(coach_row["hourly_price"])

    if hourly_price <= budget_max * 0.85:
        return 1.0
    if hourly_price <= budget_max:
        return 0.7
    if hourly_price <= budget_max * 1.10:
        return 0.3
    return 0.0


def compute_distance_convenience(request_row: dict, coach_row: pd.Series) -> float:
    city = request_row["city"]
    radius_miles = float(request_row["radius_miles"])
    coords = get_city_coordinates(city)

    distance = haversine_miles(
        coords["latitude"],
        coords["longitude"],
        float(coach_row["latitude"]),
        float(coach_row["longitude"]),
    )

    if distance <= min(5, radius_miles):
        return 1.0
    if distance <= min(10, radius_miles):
        return 0.8
    if distance <= min(15, radius_miles):
        return 0.6
    if distance <= radius_miles:
        return 0.4
    return 0.0

""" 
- Below function archetypes
What it does
Applies extra boosts/penalties depending on athlete profile.

Beginner protection
    If athlete is beginner:
        boost beginner-friendly coaches
        boost patient style
        boost fundamentals/confidence coaches
            penalize intense competitive coaches

Intermediate technique emphasis
    If athlete is intermediate + improve technique:
        boost direct technical coaches
        boost intermediate-fit coaches

Advanced performance emphasis
    If athlete is advanced:
        boost advanced coaches
        boost game-situation coaching
        boost competitive/performance goals
        penalize beginner-only style coaches 
Why ?
Without this, many toggles would only change scores slightly.
This function is what makes personas rank differently.
"""
def compute_archetype_adjustment(request_row: dict, coach_row: pd.Series) -> float:
    skill_level = request_row["skill_level"]
    main_goal = request_row["main_goal"]
    prior_private_coaching = request_row["prior_private_coaching"]
    preferred_style = request_row["coaching_style_preference"]
    lesson_frequency_intent = request_row["lesson_frequency_intent"]

    coach_style = str(coach_row["coaching_style"]).strip()
    beginner_friendly = to_bool(coach_row["beginner_friendly"])
    preferred_levels = parse_pipe_list(coach_row["preferred_athlete_levels"])
    supported_goals = parse_pipe_list(coach_row["goals_supported"])
    lesson_frequency_fit = parse_pipe_list(coach_row["lesson_frequency_fit"])

    adj = 0.0

    # Beginner protection
    if skill_level == "beginner":
        if beginner_friendly:
            adj += 0.12
        if coach_style == "patient_step_by_step":
            adj += 0.10
        if main_goal in ["build_fundamentals", "build_confidence"]:
            if main_goal in supported_goals:
                adj += 0.08
        if prior_private_coaching == "never":
            if coach_style == "patient_step_by_step":
                adj += 0.06
            if coach_style == "game_situation_coaching":
                adj -= 0.12
            if preferred_levels == ["advanced"] or ("advanced" in preferred_levels and "beginner" not in preferred_levels):
                adj -= 0.15

    # Intermediate technique emphasis
    if skill_level == "intermediate" and main_goal == "improve_technique":
        if coach_style == "direct_technical_feedback":
            adj += 0.10
        if "intermediate" in preferred_levels:
            adj += 0.06
        if beginner_friendly and coach_style == "patient_step_by_step":
            adj -= 0.03

    # Advanced performance emphasis
    if skill_level == "advanced":
        if "advanced" in preferred_levels:
            adj += 0.10
        if coach_style == "game_situation_coaching":
            adj += 0.10
        if main_goal in ["prepare_for_tryouts", "improve_game_performance"] and main_goal in supported_goals:
            adj += 0.08
        if prior_private_coaching == "regularly":
            if coach_style == "direct_technical_feedback":
                adj += 0.04
            if coach_style == "patient_step_by_step" and beginner_friendly:
                adj -= 0.10
            if "beginner" in preferred_levels and "advanced" not in preferred_levels:
                adj -= 0.14

    # Style mismatch penalty
    if preferred_style == "patient_step_by_step" and coach_style == "game_situation_coaching":
        adj -= 0.10
    if preferred_style == "game_situation_coaching" and coach_style == "patient_step_by_step":
        adj -= 0.08
    if preferred_style == "direct_technical_feedback" and coach_style == "high_energy_motivation":
        adj -= 0.08
    if preferred_style == "high_energy_motivation" and coach_style == "direct_technical_feedback":
        adj -= 0.05

    # Lesson frequency intent
    if lesson_frequency_intent == "one_time_trial":
        if beginner_friendly:
            adj += 0.05
        if "one_time_trial" in lesson_frequency_fit:
            adj += 0.05

    if lesson_frequency_intent == "weekly_long_term":
        if "weekly_long_term" in lesson_frequency_fit:
            adj += 0.06
        if float(coach_row["repeat_booking_rate"]) >= 0.75:
            adj += 0.04

    return round(adj, 3)


def build_shortlist_reasons(
    request_row: dict,
    coach_row: pd.Series,
    distance_miles: float,
    price_comfort: float,
) -> list:
    reasons = []

    if distance_miles <= 5:
        reasons.append("Very close to your location")
    elif distance_miles <= request_row["radius_miles"]:
        reasons.append("Within your search radius")

    if price_comfort >= 0.7:
        reasons.append("Within your budget")
    elif price_comfort == 0.3:
        reasons.append("Slightly above your budget")

    reasons.append(f"Matches your {coach_row['sport']} search")

    return reasons[:3]


def build_recommendation_rationale(
    request_row: dict,
    coach_row: pd.Series,
    lesson_type_fit: float,
    goal_fit: float,
    pain_point_fit: float,
    skill_fit: float,
    style_fit: float,
    reliability_fit: float,
) -> list:
    reasons = []

    if lesson_type_fit >= 1.0:
        reasons.append(f"Strong fit for {humanize(request_row['lesson_type'])}")
    elif lesson_type_fit >= 0.6:
        reasons.append(f"Related support for {humanize(request_row['lesson_type'])}")

    if goal_fit >= 0.8:
        reasons.append(f"Strong fit for {humanize(request_row['main_goal'])}")
    elif goal_fit >= 0.5:
        reasons.append(f"Supports your goal of {humanize(request_row['main_goal'])}")

    if pain_point_fit >= 0.8:
        reasons.append(f"Good support for {humanize(request_row['improvement_area'])}")
    elif pain_point_fit >= 0.5:
        reasons.append(f"Some support for {humanize(request_row['improvement_area'])}")

    if skill_fit >= 0.8:
        reasons.append(f"Good fit for {humanize(request_row['skill_level'])} athletes")

    if style_fit >= 0.8:
        reasons.append("Matches your preferred coaching style")
    elif style_fit >= 0.45:
        reasons.append("Partially aligned with your coaching style")

    if reliability_fit >= 0.8:
        reasons.append("High lesson reliability")
    elif reliability_fit >= 0.65:
        reasons.append("Solid reliability signals")

    return reasons[:4]


def build_tradeoff_note(
    lesson_type_fit: float,
    price_comfort: float,
    distance_miles: float,
    radius_miles: float,
) -> str:
    if price_comfort == 0.3:
        return "Slightly above budget, but strong overall fit."
    if lesson_type_fit < 1.0:
        return "Not the most specialized option, but still a strong personalized fit."
    if distance_miles > max(5, radius_miles * 0.7):
        return "Farther than the closest option, but stronger overall fit."
    return "Balanced option across fit, value, and reliability."


def build_confidence_label(recommendation_score: float, reliability_fit: float) -> str:
    if recommendation_score >= 0.88 and reliability_fit >= 0.75:
        return "high_confidence_match"
    if recommendation_score >= 0.70:
        return "moderate_confidence_match"
    return "best_available_option"


"""
-computes all component scores
-computes distance
-builds weighted base score
-adds archetype adjustment
-clamps to safe score range
-builds explanation strings
-returns a dictionary for that coach

Important detail

This function is where the final recommendation_score is created.

Interview explanation

“score_coach() is where one athlete request is compared against one coach across all recommendation dimensions.”
   
"""
def score_coach(request_row: dict, coach_row: pd.Series) -> dict:
    lesson_type_fit = compute_lesson_type_fit(request_row, coach_row)
    goal_fit = compute_goal_fit(request_row, coach_row)
    pain_point_fit = compute_pain_point_fit(request_row, coach_row)
    skill_fit = compute_skill_fit(request_row, coach_row)
    style_fit = compute_coaching_style_fit(request_row, coach_row)
    reliability_fit = compute_reliability_fit(coach_row)
    commitment_fit = compute_commitment_fit(request_row, coach_row)
    price_comfort = compute_price_comfort(request_row, coach_row)
    distance_convenience = compute_distance_convenience(request_row, coach_row)
    archetype_adjustment = compute_archetype_adjustment(request_row, coach_row)

    coords = get_city_coordinates(request_row["city"])
    distance_miles = haversine_miles(
        coords["latitude"],
        coords["longitude"],
        float(coach_row["latitude"]),
        float(coach_row["longitude"]),
    )

    # Keep the weighted base score below 1.0 so we preserve headroom.
    base_score = (
        0.16 * lesson_type_fit
        + 0.16 * goal_fit
        + 0.15 * pain_point_fit
        + 0.12 * skill_fit
        + 0.10 * style_fit
        + 0.09 * reliability_fit
        + 0.05 * commitment_fit
        + 0.04 * price_comfort
        + 0.03 * distance_convenience
    )

    # Archetype adjustment still matters, but should not saturate the score.
    raw_score = base_score + (0.25 * archetype_adjustment)

    # Reserve headroom so strong matches do not all collapse to 1.0
    recommendation_score = max(0.0, min(0.98, raw_score))

    shortlist_reasons = build_shortlist_reasons(
        request_row, coach_row, distance_miles, price_comfort
    )
    recommendation_rationale = build_recommendation_rationale(
        request_row,
        coach_row,
        lesson_type_fit,
        goal_fit,
        pain_point_fit,
        skill_fit,
        style_fit,
        reliability_fit,
    )

    tradeoff_note = build_tradeoff_note(
        lesson_type_fit,
        price_comfort,
        distance_miles,
        request_row["radius_miles"],
    )

    confidence_label = build_confidence_label(recommendation_score, reliability_fit)

    return {
        "coach_id": int(coach_row["id"]),
        "coach_name": coach_row["name"],
        "sport": coach_row["sport"],
        "specialty": coach_row["specialty"],
        "city": coach_row["city"],
        "hourly_price": float(coach_row["hourly_price"]),
        "distance_miles": round(distance_miles, 2),
        "recommendation_score": round(recommendation_score, 3),
        "match_score": round(recommendation_score, 3),
        "shortlist_reasons": " | ".join(shortlist_reasons),
        "recommendation_rationale": " | ".join(recommendation_rationale),
        "tradeoff_note": tradeoff_note,
        "confidence_label": confidence_label,
        "top_reasons": " | ".join((shortlist_reasons[:2] + recommendation_rationale[:2])[:4]),
    }
"""
This is the main engine entry point.

- What it does
- calls filter_candidates()
- loops over each eligible coach
- calls score_coach() on each one
- makes DataFrame of results
- sorts by recommendation_score
- assigns rank numbers
- returns final ranked table

Why
This is the function that converts:

- eligible coach pool
into
- ranked recommendation list

This is the most important backend function.
"""

def rank_coaches_for_request(request_row: dict, coaches_df: pd.DataFrame) -> pd.DataFrame:
    candidates = filter_candidates(request_row, coaches_df)

    if candidates.empty:
        return pd.DataFrame()

    scored_results = []
    for _, coach_row in candidates.iterrows():
        scored_results.append(score_coach(request_row, coach_row))

    results_df = pd.DataFrame(scored_results)
    results_df = results_df.sort_values(
        by="recommendation_score",
        ascending=False,
    ).reset_index(drop=True)

    results_df["rank"] = results_df.index + 1

    return results_df[
        [
            "rank",
            "coach_id",
            "coach_name",
            "sport",
            "specialty",
            "city",
            "hourly_price",
            "distance_miles",
            "recommendation_score",
            "match_score",
            "shortlist_reasons",
            "recommendation_rationale",
            "tradeoff_note",
            "confidence_label",
            "top_reasons",
        ]
    ]


if __name__ == "__main__":
    coaches_df = load_coaches()
    sample_request = {
        "athlete_name": "Alex Lee",
        "city": "Houston",
        "sport": "baseball",
        "athlete_age": 13,
        "budget_max": 80,
        "radius_miles": 50,
        "lesson_type": "hitting",
        "skill_level": "intermediate",
        "main_goal": "improve_technique",
        "improvement_area": "swing_consistency",
        "prior_private_coaching": "a_few_times",
        "coaching_style_preference": "direct_technical_feedback",
        "lesson_frequency_intent": "weekly_long_term",
    }
    print(rank_coaches_for_request(sample_request, coaches_df).head(5).to_string(index=False))