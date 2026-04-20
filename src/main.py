import sys
from src.load_data import load_coaches, load_availability, load_search_requests
from src.matching_engine import rank_coaches_for_request
from src.pricing_engine import recommend_price_for_coach

def get_request_by_id(search_requests_df, request_id: int):
    matched = search_requests_df[search_requests_df["id"] == request_id]
    if matched.empty:
        return None
    return matched.iloc[0]


def get_coach_by_id(coaches_df, coach_id: int):
    matched = coaches_df[coaches_df["id"] == coach_id]
    if matched.empty:
        return None
    return matched.iloc[0]


def main():
    coaches_df = load_coaches()
    availability_df = load_availability()
    search_requests_df = load_search_requests()

    if len(sys.argv) > 1:
        try:
            request_id = int(sys.argv[1])
        except ValueError:
            print("Please provide a valid integer request ID.")
            return
    else:
        request_id = 1

    request_row = get_request_by_id(search_requests_df, request_id)

    if request_row is None:
        print(f"No search request found for ID {request_id}")
        return

    ranked_results = rank_coaches_for_request(request_row, coaches_df, availability_df)

    print("=" * 80)
    print("SMART COACH MATCHING RESULTS")
    print("=" * 80)
    print(f"Request ID      : {int(request_row['id'])}")
    print(f"Sport           : {request_row['sport']}")
    print(f"Lesson Type     : {request_row['lesson_type']}")
    print(f"Athlete Age     : {int(request_row['athlete_age'])}")
    print(f"Skill Level     : {request_row['skill_level']}")
    print(f"Budget Max      : ${float(request_row['budget_max']):.2f}")
    print(f"Preferred Days  : {request_row['preferred_days']}")
    print(f"Preferred Time  : {request_row['preferred_time']}")
    print(f"Search Radius   : {float(request_row['radius_miles']):.0f} miles")
    print("=" * 80)

    if ranked_results.empty:
        print("No matching coaches found for the current search criteria.")
        print()
        print("Suggested next actions:")
        print("  1. Increase the search radius")
        print("  2. Broaden the lesson specialty")
        print("  3. Expand preferred day/time availability")
        print("  4. Notify the marketplace team about low local supply")
        print()
        print("=" * 80)
        print("Displayed 0 recommendation(s)")
        print("=" * 80)
        return

    top_3 = ranked_results.head(3)

    for _, row in top_3.iterrows():
        rank = int(row["rank"])
        coach_id = int(row["coach_id"])
        coach_name = str(row["coach_name"])
        sport = str(row["sport"])
        specialty = str(row["specialty"])
        city = str(row["city"])
        hourly_price = float(row["hourly_price"])
        distance_miles = float(row["distance_miles"])
        match_score = float(row["match_score"])
        top_reasons = str(row["top_reasons"])

        coach_row = get_coach_by_id(coaches_df, coach_id)
        pricing_result = recommend_price_for_coach(coach_row)

        print()
        print(f"Rank #{rank}: {coach_name}")
        print(f"  Coach ID       : {coach_id}")
        print(f"  Sport          : {sport}")
        print(f"  Specialty      : {specialty}")
        print(f"  City           : {city}")
        print(f"  Current Price  : ${hourly_price:.2f}")
        print(f"  Distance       : {distance_miles:.2f} miles")
        print(f"  Match Score    : {match_score:.3f}")
        print(f"  Why Recommended: {top_reasons}")
        print(f"  Suggested Price: ${pricing_result['recommended_low']:.2f} - ${pricing_result['recommended_high']:.2f}")

        if pricing_result["reasons"]:
            print("  Pricing Reasons:")
            for reason in pricing_result["reasons"]:
                print(f"    - {reason}")

    print()
    print("=" * 80)
    print(f"Displayed top {min(3, len(ranked_results))} recommendation(s)")
    print("=" * 80)


if __name__ == "__main__":
    main()