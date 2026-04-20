import pandas as pd
from src.load_data import load_coaches


SPORT_BASE_PRICES = {
    ("baseball", "pitching"): 50,
    ("baseball", "hitting"): 48,
    ("baseball", "catching"): 45,
    ("baseball", "infield"): 46,
    ("baseball", "outfield"): 44,
    ("baseball", "strength_and_conditioning"): 55,
    ("softball", "pitching"): 52,
    ("softball", "hitting"): 47,
    ("softball", "catching"): 45,
    ("softball", "fielding"): 46,
    ("softball", "speed_and_agility"): 43,
}

DIVISION_PRICE_ADJUSTMENTS = {
    "D1": 8,
    "D2": 5,
    "D3": 3,
    "NAIA": 2,
    "JUCO": 1,
}

CITY_PRICE_ADJUSTMENTS = {
    "Dallas": 4,
    "Austin": 5,
    "Houston": 4,
    "Oklahoma City": 2,
    "Norman": 1,
    "Tulsa": 1,
}


def get_base_price(sport: str, specialty: str) -> float:
    return SPORT_BASE_PRICES.get((sport, specialty), 45)


def compute_experience_adjustment(years_experience: int) -> float:
    if years_experience >= 7:
        return 6
    if years_experience >= 5:
        return 4
    if years_experience >= 3:
        return 2
    return 0


def compute_rating_adjustment(avg_rating: float) -> float:
    if avg_rating >= 4.8:
        return 6
    if avg_rating >= 4.5:
        return 4
    if avg_rating >= 4.2:
        return 2
    return 0


def compute_review_adjustment(review_count: int) -> float:
    if review_count >= 50:
        return 4
    if review_count >= 25:
        return 2
    if review_count >= 10:
        return 1
    return 0


def compute_completion_adjustment(completion_rate: float) -> float:
    if completion_rate >= 0.95:
        return 3
    if completion_rate >= 0.90:
        return 2
    if completion_rate >= 0.85:
        return 1
    return 0

# Matching decides who is the best fit. Pricing is a separate layer that estimates where the coach should be priced.
def recommend_price_for_coach(coach_row: pd.Series) -> dict:
    sport = str(coach_row["sport"])
    specialty = str(coach_row["specialty"])
    division_level = str(coach_row["division_level"])
    years_experience = int(coach_row["years_experience"])
    avg_rating = float(coach_row["avg_rating"])
    review_count = int(coach_row["review_count"])
    completion_rate = float(coach_row["completion_rate"])
    city = str(coach_row["city"])

    base_price = get_base_price(sport, specialty)
    division_adj = DIVISION_PRICE_ADJUSTMENTS.get(division_level, 0)
    experience_adj = compute_experience_adjustment(years_experience)
    rating_adj = compute_rating_adjustment(avg_rating)
    review_adj = compute_review_adjustment(review_count)
    completion_adj = compute_completion_adjustment(completion_rate)
    city_adj = CITY_PRICE_ADJUSTMENTS.get(city, 0)

    recommended_mid = (
        base_price
        + division_adj
        + experience_adj
        + rating_adj
        + review_adj
        + completion_adj
        + city_adj
    )

    recommended_low = max(30, recommended_mid - 4)
    recommended_high = recommended_mid + 4

    reasons = []

    if division_adj >= 5:
        reasons.append(f"{division_level} playing background supports premium pricing")
    elif division_adj > 0:
        reasons.append(f"{division_level} experience adds pricing value")

    if experience_adj >= 4:
        reasons.append("Strong coaching experience supports higher pricing")
    elif experience_adj > 0:
        reasons.append("Coaching experience supports moderate price lift")

    if rating_adj >= 4:
        reasons.append("Strong ratings support premium positioning")
    elif rating_adj > 0:
        reasons.append("Positive ratings support pricing confidence")

    if review_adj >= 2:
        reasons.append("Review volume improves pricing confidence")

    if completion_adj >= 2:
        reasons.append("High completion rate supports trust and price stability")

    if city_adj >= 4:
        reasons.append("Local market demand supports a higher price")
    elif city_adj > 0:
        reasons.append("Local market conditions slightly increase price")

    return {
        "coach_id": int(coach_row["id"]),
        "coach_name": coach_row["name"],
        "sport": sport,
        "specialty": specialty,
        "current_price": float(coach_row["hourly_price"]),
        "recommended_low": float(recommended_low),
        "recommended_high": float(recommended_high),
        "recommended_mid": float(recommended_mid),
        "reasons": reasons[:4],
    }


if __name__ == "__main__":
    coaches_df = load_coaches()
    print(recommend_price_for_coach(coaches_df.iloc[0]))