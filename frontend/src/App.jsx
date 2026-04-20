import { useEffect, useMemo, useState } from "react";
import axios from "axios";
import "./App.css";

const API_BASE =
  import.meta.env.DEV ? "http://127.0.0.1:8000/api" : "/api";

const SPORT_TO_LESSON_TYPES = {
  baseball: [
    "pitching",
    "hitting",
    "catching",
    "infield",
    "outfield",
    "strength_and_conditioning",
  ],
  softball: [
    "pitching",
    "hitting",
    "catching",
    "fielding",
    "speed_and_agility",
  ],
};

const LESSON_TYPE_TO_IMPROVEMENT_AREAS = {
  pitching: [
    "pitching_control",
    "pitching_velocity",
    "throwing_accuracy",
    "confidence_under_pressure",
  ],
  hitting: [
    "swing_consistency",
    "contact_hitting",
    "confidence_under_pressure",
  ],
  catching: [
    "catching_mechanics",
    "throwing_accuracy",
    "confidence_under_pressure",
  ],
  infield: [
    "fielding_footwork",
    "reaction_speed",
    "throwing_accuracy",
  ],
  outfield: [
    "fielding_footwork",
    "reaction_speed",
    "throwing_accuracy",
  ],
  fielding: [
    "fielding_footwork",
    "reaction_speed",
    "throwing_accuracy",
  ],
  strength_and_conditioning: [
    "reaction_speed",
    "throwing_accuracy",
  ],
  speed_and_agility: [
    "reaction_speed",
    "fielding_footwork",
  ],
};

const LESSON_TYPE_TO_MAIN_GOALS = {
  pitching: [
    "build_fundamentals",
    "improve_technique",
    "prepare_for_tryouts",
    "build_confidence",
    "improve_game_performance",
  ],
  hitting: [
    "build_fundamentals",
    "improve_technique",
    "prepare_for_tryouts",
    "build_confidence",
    "improve_game_performance",
  ],
  catching: [
    "build_fundamentals",
    "improve_technique",
    "build_confidence",
    "improve_game_performance",
  ],
  infield: [
    "build_fundamentals",
    "improve_technique",
    "prepare_for_tryouts",
    "improve_game_performance",
  ],
  outfield: [
    "build_fundamentals",
    "improve_technique",
    "prepare_for_tryouts",
    "improve_game_performance",
  ],
  fielding: [
    "build_fundamentals",
    "improve_technique",
    "prepare_for_tryouts",
    "improve_game_performance",
  ],
  strength_and_conditioning: [
    "strength_speed_development",
    "improve_game_performance",
  ],
  speed_and_agility: [
    "strength_speed_development",
    "improve_game_performance",
  ],
};

const SKILL_LEVEL_TO_MAIN_GOALS = {
  beginner: [
    "build_fundamentals",
    "build_confidence",
    "improve_technique",
  ],
  intermediate: [
    "improve_technique",
    "improve_game_performance",
    "prepare_for_tryouts",
    "build_confidence",
  ],
  advanced: [
    "improve_technique",
    "prepare_for_tryouts",
    "improve_game_performance",
  ],
};

const SKILL_LEVEL_OPTIONS = ["beginner", "intermediate", "advanced"];
const PRIOR_COACHING_OPTIONS = ["never", "a_few_times", "regularly"];
const COACHING_STYLE_OPTIONS = [
  "patient_step_by_step",
  "direct_technical_feedback",
  "high_energy_motivation",
  "drill_heavy_practice",
  "game_situation_coaching",
];
const LESSON_FREQUENCY_OPTIONS = [
  "one_time_trial",
  "occasional",
  "weekly_long_term",
];

function App() {
  const [step, setStep] = useState(1);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const [basicForm, setBasicForm] = useState({
    athlete_name: "Alex Lee",
    city: "Houston",
    sport: "baseball",
    athlete_age: 13,
    budget_max: 80,
    radius_miles: 50,
  });

  const [personalForm, setPersonalForm] = useState({
    lesson_type: "hitting",
    skill_level: "intermediate",
    main_goal: "improve_technique",
    improvement_area: "swing_consistency",
    prior_private_coaching: "a_few_times",
    coaching_style_preference: "direct_technical_feedback",
    lesson_frequency_intent: "weekly_long_term",
  });

  const [eligibilityData, setEligibilityData] = useState(null);
  const [matchResult, setMatchResult] = useState(null);
  const [pricingByCoach, setPricingByCoach] = useState({});

  // useMemo is used to compute allowed dropdown options from the current form state, instead of recalculating them blindly every render.
  const lessonTypeOptions = useMemo(() => {
    return SPORT_TO_LESSON_TYPES[basicForm.sport] || [];
  }, [basicForm.sport]);

  const improvementAreaOptions = useMemo(() => {
    return LESSON_TYPE_TO_IMPROVEMENT_AREAS[personalForm.lesson_type] || [];
  }, [personalForm.lesson_type]);

  const mainGoalOptions = useMemo(() => {
    const lessonGoals = LESSON_TYPE_TO_MAIN_GOALS[personalForm.lesson_type] || [];
    const skillGoals = SKILL_LEVEL_TO_MAIN_GOALS[personalForm.skill_level] || [];
    return lessonGoals.filter((goal) => skillGoals.includes(goal));
  }, [personalForm.lesson_type, personalForm.skill_level]);


  //If current lesson_type becomes invalid after sport change:
  //reset lesson type
  //reset main goal
  //reset improvement area
  // useEffect is used here like a watcher. 
  // When one form choice changes and makes another choice invalid, it automatically fixes the state.
  useEffect(() => {
    if (!lessonTypeOptions.includes(personalForm.lesson_type)) {
      const nextLessonType = lessonTypeOptions[0] || "";
      setPersonalForm((prev) => ({
        ...prev,
        lesson_type: nextLessonType,
        main_goal: (LESSON_TYPE_TO_MAIN_GOALS[nextLessonType] || [])[0] || "",
        improvement_area:
          (LESSON_TYPE_TO_IMPROVEMENT_AREAS[nextLessonType] || [])[0] || "",
      }));
    }
  }, [lessonTypeOptions, personalForm.lesson_type]);

  useEffect(() => {
    const validImprovementAreas =
      LESSON_TYPE_TO_IMPROVEMENT_AREAS[personalForm.lesson_type] || [];
    const lessonGoals =
      LESSON_TYPE_TO_MAIN_GOALS[personalForm.lesson_type] || [];
    const skillGoals =
      SKILL_LEVEL_TO_MAIN_GOALS[personalForm.skill_level] || [];
    const validMainGoals = lessonGoals.filter((goal) =>
      skillGoals.includes(goal)
    );

    setPersonalForm((prev) => ({
      ...prev,
      improvement_area: validImprovementAreas.includes(prev.improvement_area)
        ? prev.improvement_area
        : validImprovementAreas[0] || "",
      main_goal: validMainGoals.includes(prev.main_goal)
        ? prev.main_goal
        : validMainGoals[0] || "",
    }));
  }, [personalForm.lesson_type, personalForm.skill_level]);

  // Updates basicForm when user changes Step 1 input.
  const handleBasicChange = (e) => {
    const { name, value } = e.target;
    const numericFields = ["athlete_age", "budget_max", "radius_miles"];

    setBasicForm((prev) => ({
      ...prev,
      [name]: numericFields.includes(name) ? Number(value) : value,
    }));
  };

  // Updates personalForm when user changes Step 3 input.
  const handlePersonalChange = (e) => {
    const { name, value } = e.target;
    setPersonalForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // Backend sends some reason strings joined by " | ".
  // This function converts them into arrays for rendering bullet lists.
  const splitReasons = (value) => {
    if (!value) return [];
    return String(value)
      .split("|")
      .map((item) => item.trim())
      .filter(Boolean);
  };

  const formatText = (value) => {
    if (!value) return "";
    return String(value).replaceAll("_", " ");
  };

/*For each recommended coach, frontend calls: /api/coaches/{id}/pricing
Then stores those pricing responses in a map by coach id.
Why -
Pricing is treated as a separate backend calculation. */
  const fetchPricingForMatches = async (matches) => {
    const pricingResults = await Promise.all(
      matches.map(async (coach) => {
        const response = await axios.get(
          `${API_BASE}/coaches/${coach.coach_id}/pricing`
        );
        return { coachId: coach.coach_id, pricing: response.data };
      })
    );

    const pricingMap = {};
    pricingResults.forEach((item) => {
      pricingMap[item.coachId] = item.pricing;
    });

    setPricingByCoach(pricingMap);
  };

  /*  
  What it does
    sets loading
    clears old results
    sends basicForm to /api/eligible
    stores response in eligibilityData
    moves to step 2 
  */
  const handleEligibilityNext = async () => {
    try {
      setLoading(true);
      setError("");
      setEligibilityData(null);
      setMatchResult(null);
      setPricingByCoach({});

      const response = await axios.post(`${API_BASE}/eligible`, basicForm);
      setEligibilityData(response.data);
      setStep(2);
    } catch (err) {
      console.error("Eligibility error:", err?.response?.data || err.message);
      setError("Failed to evaluate eligible coaches.");
    } finally {
      setLoading(false);
    }
  };

  /*
      What it does
        sets loading
        clears old recommendation state
        merges basicForm and personalForm
        sends full payload to /api/match
        stores ranked matches in matchResult
        fetches pricing for each returned coach
        moves to step 4 
  */
  const handleRecommendationSubmit = async () => {
    try {
      setLoading(true);
      setError("");
      setMatchResult(null);
      setPricingByCoach({});

      const payload = {
        ...basicForm,
        ...personalForm,
      };

      const response = await axios.post(`${API_BASE}/match`, payload);
      setMatchResult(response.data);

      if (response.data.matches?.length > 0) {
        await fetchPricingForMatches(response.data.matches);
      }

      setStep(4);
    } catch (err) {
      console.error("Recommendation error:", err?.response?.data || err.message);
      setError("Failed to generate personalized recommendation.");
    } finally {
      setLoading(false);
    }
  };

  // Renders the 4-step progress indicator.
  const renderStepper = () => {
    const steps = [
      "Basic Filters",
      "Eligible Coaches",
      "Personalization",
      "Recommendation",
    ];

    return (
      <div className="stepper">
        {steps.map((label, index) => {
          const stepNumber = index + 1;
          const state =
            step === stepNumber ? "active" : step > stepNumber ? "done" : "upcoming";

          return (
            <div key={label} className={`step-item ${state}`}>
              <div className="step-circle">{stepNumber}</div>
              <div className="step-label">{label}</div>
            </div>
          );
        })}
      </div>
    );
  };

  // Renders Step 1 form.
  const renderBasicFilters = () => (
    <section className="panel">
      <h2>Step 1: Basic Filters</h2>
      <p className="section-subtext">
        First build a broad coach pool using only city, sport, budget, and radius.
      </p>

      <div className="form-grid">
        <div>
          <label>Athlete Name</label>
          <input
            name="athlete_name"
            value={basicForm.athlete_name}
            onChange={handleBasicChange}
          />
        </div>

        <div>
          <label>City</label>
          <select name="city" value={basicForm.city} onChange={handleBasicChange}>
            <option value="Dallas">Dallas</option>
            <option value="Austin">Austin</option>
            <option value="Houston">Houston</option>
            <option value="Oklahoma City">Oklahoma City</option>
            <option value="Norman">Norman</option>
            <option value="Tulsa">Tulsa</option>
          </select>
        </div>

        <div>
          <label>Sport</label>
          <select name="sport" value={basicForm.sport} onChange={handleBasicChange}>
            <option value="baseball">baseball</option>
            <option value="softball">softball</option>
          </select>
        </div>

        <div>
          <label>Athlete Age</label>
          <input
            type="number"
            name="athlete_age"
            value={basicForm.athlete_age}
            onChange={handleBasicChange}
          />
        </div>

        <div>
          <label>Budget Max</label>
          <input
            type="number"
            name="budget_max"
            value={basicForm.budget_max}
            onChange={handleBasicChange}
          />
        </div>

        <div>
          <label>Radius (miles)</label>
          <input
            type="number"
            name="radius_miles"
            value={basicForm.radius_miles}
            onChange={handleBasicChange}
          />
        </div>
      </div>

      <div className="button-row">
        <button className="primary-button" onClick={handleEligibilityNext} disabled={loading}>
          {loading ? "Checking eligible coaches..." : "Next: See Eligible Coaches"}
        </button>
      </div>
    </section>
  );

  // Renders Step 2 eligible coach pool.
  const renderEligibleSummary = () => (
    <section className="panel">
      <h2>Step 2: Eligible Coach Pool</h2>
      <p className="section-subtext">
        These coaches passed the broad eligibility filters. Next, we personalize the ranking.
      </p>

      <div className="summary-hero">
        <div className="summary-metric">
          <span className="summary-number">{eligibilityData?.eligible_count ?? 0}</span>
          <span className="summary-text">eligible coaches found</span>
        </div>
      </div>

      <div className="request-summary">
        <p><strong>Athlete:</strong> {basicForm.athlete_name}</p>
        <p><strong>City:</strong> {basicForm.city}</p>
        <p><strong>Sport:</strong> {basicForm.sport}</p>
        <p><strong>Age:</strong> {basicForm.athlete_age}</p>
        <p><strong>Budget Max:</strong> ${basicForm.budget_max}</p>
        <p><strong>Radius:</strong> {basicForm.radius_miles} miles</p>
      </div>

      {eligibilityData?.eligible_coaches?.length > 0 ? (
        <div className="eligible-list">
          {eligibilityData.eligible_coaches.map((coach) => (
            <div key={coach.coach_id} className="preview-card">
              <h4>{coach.coach_name}</h4>
              <p><strong>Specialty:</strong> {formatText(coach.specialty)}</p>
              <p><strong>City:</strong> {coach.city}</p>
              <p><strong>Price:</strong> ${coach.hourly_price}</p>
              <p><strong>Distance:</strong> {coach.distance_miles} miles</p>
              <p><strong>Rating:</strong> {coach.avg_rating}</p>
              <p><strong>Experience:</strong> {coach.years_experience} years</p>
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <p>{eligibilityData?.message}</p>
        </div>
      )}

      <div className="button-row">
        <button className="secondary-button" onClick={() => setStep(1)}>
          Back
        </button>
        <button
          className="primary-button"
          onClick={() => setStep(3)}
          disabled={!eligibilityData || eligibilityData.eligible_count === 0}
        >
          Next: Personalize Recommendation
        </button>
      </div>
    </section>
  );

  // Renders Step 3 dynamic recommendation form.
  const renderPersonalization = () => (
    <section className="panel">
      <h2>Step 3: Personalization</h2>
      <p className="section-subtext">
        These options are constrained by sport, lesson type, and skill level so the form stays relevant.
      </p>

      <div className="form-grid">
        <div>
          <label>Lesson Type</label>
          <select
            name="lesson_type"
            value={personalForm.lesson_type}
            onChange={handlePersonalChange}
          >
            {lessonTypeOptions.map((option) => (
              <option key={option} value={option}>
                {formatText(option)}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label>Skill Level</label>
          <select
            name="skill_level"
            value={personalForm.skill_level}
            onChange={handlePersonalChange}
          >
            {SKILL_LEVEL_OPTIONS.map((option) => (
              <option key={option} value={option}>
                {formatText(option)}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label>Main Goal</label>
          <select
            name="main_goal"
            value={personalForm.main_goal}
            onChange={handlePersonalChange}
          >
            {mainGoalOptions.map((option) => (
              <option key={option} value={option}>
                {formatText(option)}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label>Improvement Area</label>
          <select
            name="improvement_area"
            value={personalForm.improvement_area}
            onChange={handlePersonalChange}
          >
            {improvementAreaOptions.map((option) => (
              <option key={option} value={option}>
                {formatText(option)}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label>Prior Private Coaching</label>
          <select
            name="prior_private_coaching"
            value={personalForm.prior_private_coaching}
            onChange={handlePersonalChange}
          >
            {PRIOR_COACHING_OPTIONS.map((option) => (
              <option key={option} value={option}>
                {formatText(option)}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label>Coaching Style Preference</label>
          <select
            name="coaching_style_preference"
            value={personalForm.coaching_style_preference}
            onChange={handlePersonalChange}
          >
            {COACHING_STYLE_OPTIONS.map((option) => (
              <option key={option} value={option}>
                {formatText(option)}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label>Lesson Frequency Intent</label>
          <select
            name="lesson_frequency_intent"
            value={personalForm.lesson_frequency_intent}
            onChange={handlePersonalChange}
          >
            {LESSON_FREQUENCY_OPTIONS.map((option) => (
              <option key={option} value={option}>
                {formatText(option)}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="button-row">
        <button className="secondary-button" onClick={() => setStep(2)}>
          Back
        </button>
        <button className="primary-button" onClick={handleRecommendationSubmit} disabled={loading}>
          {loading ? "Generating recommendation..." : "Get Highest Recommended Coach"}
        </button>
      </div>
    </section>
  );

  // Renders Step 4 recommendation output
  const renderResults = () => {
    if (!matchResult?.matches?.length) {
      return (
        <section className="panel">
          <h2>Step 4: Recommendation</h2>
          <div className="empty-state">
            <p>{matchResult?.message || "No recommendation available."}</p>
          </div>
          <div className="button-row">
            <button className="secondary-button" onClick={() => setStep(3)}>
              Back
            </button>
            <button className="primary-button" onClick={() => setStep(1)}>
              Start New Search
            </button>
          </div>
        </section>
      );
    }

    const topCoach = matchResult.matches[0];
    const alternatives = matchResult.matches.slice(1);
    const topPricing = pricingByCoach[topCoach.coach_id];

    return (
      <section className="panel">
        <h2>Step 4: Best-Fit Recommendation</h2>
        <p className="section-subtext">
          From the broad eligible pool, this coach ranked highest after applying
          lesson type, goal, improvement area, style, and reliability.
        </p>

        <div className="hero-result-card">
          <div className="hero-top-row">
            <div>
              <div className="hero-tag">Best First-Fit Coach</div>
              <h3>{topCoach.coach_name}</h3>
              <p className="coach-subtitle">
                {topCoach.sport} • {formatText(topCoach.specialty)} • {topCoach.city}
              </p>
            </div>
            <div className="score-badge">
              <span className="score-label">Recommendation Score</span>
              <span className="score-value">{topCoach.recommendation_score}</span>
            </div>
          </div>

          <div className="meta-row">
            <span><strong>Current Price:</strong> ${topCoach.hourly_price}</span>
            <span><strong>Distance:</strong> {topCoach.distance_miles} miles</span>
            <span><strong>Confidence:</strong> {formatText(topCoach.confidence_label)}</span>
          </div>

          <div className="reason-box">
            <h4>Why this coach was shortlisted</h4>
            <ul>
              {splitReasons(topCoach.shortlist_reasons).map((reason, idx) => (
                <li key={idx}>{reason}</li>
              ))}
            </ul>
          </div>

          <div className="reason-box recommendation-box">
            <h4>Why this coach is recommended for this athlete</h4>
            <ul>
              {splitReasons(topCoach.recommendation_rationale).map((reason, idx) => (
                <li key={idx}>{reason}</li>
              ))}
            </ul>
          </div>

          <div className="tradeoff-box">
            <h4>Tradeoff</h4>
            <p>{topCoach.tradeoff_note}</p>
          </div>

          {topPricing && (
            <div className="pricing-box">
              <p>
                <strong>Recommended Coach Price:</strong> ${topPricing.recommended_low} - ${topPricing.recommended_high}
              </p>
              {topPricing.reasons?.length > 0 && (
                <>
                  <h4>Pricing rationale</h4>
                  <ul>
                    {topPricing.reasons.map((reason, idx) => (
                      <li key={idx}>{reason}</li>
                    ))}
                  </ul>
                </>
              )}
            </div>
          )}
        </div>

        {alternatives.length > 0 && (
          <>
            <h3 className="subsection-title">Alternative Options</h3>
            <div className="card-list">
              {alternatives.map((coach) => {
                const pricing = pricingByCoach[coach.coach_id];

                return (
                  <div className="coach-card" key={coach.coach_id}>
                    <div className="coach-card-header">
                      <div>
                        <h4>#{coach.rank} {coach.coach_name}</h4>
                        <p className="coach-subtitle">
                          {coach.sport} • {formatText(coach.specialty)} • {coach.city}
                        </p>
                      </div>
                      <div className="small-score-badge">{coach.recommendation_score}</div>
                    </div>

                    <p><strong>Why recommended:</strong> {coach.top_reasons}</p>
                    <p><strong>Tradeoff:</strong> {coach.tradeoff_note}</p>
                    <p><strong>Confidence:</strong> {formatText(coach.confidence_label)}</p>

                    {pricing && (
                      <p>
                        <strong>Recommended Coach Price:</strong> ${pricing.recommended_low} - ${pricing.recommended_high}
                      </p>
                    )}
                  </div>
                );
              })}
            </div>
          </>
        )}

        <div className="button-row">
          <button className="secondary-button" onClick={() => setStep(3)}>
            Back
          </button>
          <button className="primary-button" onClick={() => setStep(1)}>
            Start New Search
          </button>
        </div>
      </section>
    );
  };

  return (
    <div className="app-shell">
      <div className="hero-banner">
        <div className="hero-content">
          <h1>Smart Coach Recommendation</h1>
          <p>
            First build a broad eligible pool. Then personalize the ranking to
            find the best first-fit coach.
          </p>
        </div>
      </div>

      <div className="app-container">
        {renderStepper()}

        {error && <div className="error-banner">{error}</div>}

        {step === 1 && renderBasicFilters()}
        {step === 2 && renderEligibleSummary()}
        {step === 3 && renderPersonalization()}
        {step === 4 && renderResults()}
      </div>
    </div>
  );
}

export default App;