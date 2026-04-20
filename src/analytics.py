import pandas as pd
from load_data import load_coaches, load_availability, load_search_requests
from matching_engine import rank_coaches_for_request


def run_marketplace_analytics():
    coaches_df = load_coaches()
    availability_df = load_availability()
    search_requests_df = load_search_requests()

    summary_rows = []

    for _, request_row in search_requests_df.iterrows():
        ranked_results = rank_coaches_for_request(request_row, coaches_df, availability_df)
        match_count = len(ranked_results)

        summary_rows.append(
            {
                "request_id": int(request_row["id"]),
                "sport": request_row["sport"],
                "lesson_type": request_row["lesson_type"],
                "city": (
                    "Dallas" if float(request_row["search_latitude"]) == 32.7767 else
                    "Austin" if float(request_row["search_latitude"]) == 30.2672 else
                    "Houston" if float(request_row["search_latitude"]) == 29.7604 else
                    "Oklahoma City" if float(request_row["search_latitude"]) == 35.4676 else
                    "Norman" if float(request_row["search_latitude"]) == 35.2226 else
                    "Tulsa"
                ),
                "skill_level": request_row["skill_level"],
                "budget_max": float(request_row["budget_max"]),
                "radius_miles": float(request_row["radius_miles"]),
                "match_count": match_count,
                "has_match": match_count > 0,
                "top_match_score": float(ranked_results.iloc[0]["match_score"]) if match_count > 0 else None,
            }
        )

    summary_df = pd.DataFrame(summary_rows)

    total_requests = len(summary_df)
    matched_requests = int(summary_df["has_match"].sum())
    unmatched_requests = total_requests - matched_requests
    match_rate = matched_requests / total_requests if total_requests > 0 else 0.0
    avg_match_count = summary_df["match_count"].mean() if total_requests > 0 else 0.0

    print("=" * 80)
    print("MARKETPLACE ANALYTICS SUMMARY")
    print("=" * 80)
    print(f"Total search requests              : {total_requests}")
    print(f"Requests with at least one match   : {matched_requests}")
    print(f"Requests with zero matches         : {unmatched_requests}")
    print(f"Request-level match rate           : {match_rate:.2%}")
    print(f"Average candidates per request     : {avg_match_count:.2f}")
    print("=" * 80)

    print("\nRequests with zero matches")
    zero_match_df = summary_df[summary_df["has_match"] == False]
    if zero_match_df.empty:
        print("  None")
    else:
        print(zero_match_df[["request_id", "sport", "lesson_type", "city", "skill_level", "radius_miles"]].to_string(index=False))

    print("\nMatch rate by sport")
    sport_summary = (
        summary_df.groupby("sport")
        .agg(
            total_requests=("request_id", "count"),
            matched_requests=("has_match", "sum"),
            avg_match_count=("match_count", "mean"),
        )
        .reset_index()
    )
    sport_summary["match_rate"] = sport_summary["matched_requests"] / sport_summary["total_requests"]
    print(sport_summary.to_string(index=False))

    print("\nMatch rate by lesson type")
    lesson_summary = (
        summary_df.groupby(["sport", "lesson_type"])
        .agg(
            total_requests=("request_id", "count"),
            matched_requests=("has_match", "sum"),
            avg_match_count=("match_count", "mean"),
        )
        .reset_index()
    )
    lesson_summary["match_rate"] = lesson_summary["matched_requests"] / lesson_summary["total_requests"]
    print(lesson_summary.to_string(index=False))

    print("\nLowest-supply request segments")
    low_supply = summary_df.sort_values(by=["match_count", "top_match_score"], ascending=[True, True])
    print(low_supply[["request_id", "sport", "lesson_type", "city", "skill_level", "match_count", "top_match_score"]].head(10).to_string(index=False))


if __name__ == "__main__":
    run_marketplace_analytics()