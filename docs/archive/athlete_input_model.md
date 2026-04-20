# Athlete Input Model for Personalized Coach Recommendation

## 1. Goal
Define the exact athlete inputs used by the two-stage recommendation system.

Stage 1 uses basic filtering inputs to determine eligibility.

Stage 2 uses personalized inputs to rank the best first-fit coach among eligible coaches.

---

## 2. Athlete Input Groups

### A. Basic Filtering Inputs
These determine which coaches are eligible.

- athlete_name
- city
- sport
- lesson_type
- athlete_age
- budget_max
- preferred_days
- preferred_time
- radius_miles

### B. Personalized Recommendation Inputs
These determine which eligible coach is the best fit.

- skill_level
- main_goal
- improvement_area
- prior_private_coaching
- coaching_style_preference
- lesson_frequency_intent

---

## 3. Exact Fields and Allowed Values

### athlete_name
Type:
- string

Purpose:
- UI only
- does not affect recommendation score directly

Example:
- Alex Carter

---

### city
Type:
- string

Allowed values:
- Dallas
- Austin
- Houston
- Oklahoma City
- Norman
- Tulsa

Purpose:
- maps to search_latitude and search_longitude
- used in filtering and distance scoring

---

### sport
Type:
- string

Allowed values:
- baseball
- softball

Purpose:
- hard filter

---

### lesson_type
Type:
- string

Allowed values:
- pitching
- hitting
- catching
- infield
- outfield
- fielding
- strength_and_conditioning
- speed_and_agility

Purpose:
- hard filter
- also used for shortlist reasons

---

### athlete_age
Type:
- integer

Suggested range:
- 8 to 18

Purpose:
- can be shown in UI
- optional future fit signal
- not part of current recommendation formula

---

### budget_max
Type:
- float or integer

Suggested range:
- 30 to 100

Purpose:
- hard budget filter
- PriceComfort scoring

---

### preferred_days
Type:
- comma-separated string

Example:
- Monday,Wednesday,Saturday

Purpose:
- availability filtering
- shortlist reasons

---

### preferred_time
Type:
- string

Allowed values:
- morning
- afternoon
- evening

Purpose:
- availability filtering
- shortlist reasons

---

### radius_miles
Type:
- integer or float

Suggested values:
- 5
- 10
- 15
- 25

Purpose:
- distance filtering
- DistanceConvenience scoring

---

### skill_level
Type:
- string

Allowed values:
- beginner
- intermediate
- advanced

Purpose:
- SkillFit scoring

---

### main_goal
Type:
- string

Allowed values:
- build_fundamentals
- improve_technique
- prepare_for_tryouts
- build_confidence
- improve_game_performance
- strength_speed_development

Purpose:
- GoalFit scoring

---

### improvement_area
Type:
- string

Allowed values:
- pitching_control
- pitching_velocity
- swing_consistency
- contact_hitting
- fielding_footwork
- catching_mechanics
- throwing_accuracy
- reaction_speed
- confidence_under_pressure

Purpose:
- PainPointFit scoring

---

### prior_private_coaching
Type:
- string

Allowed values:
- never
- a_few_times
- regularly

Purpose:
- modifies confidence label
- supports SkillFit interpretation
- supports recommendation rationale

Example logic:
- beginner + never + beginner_friendly coach = stronger recommendation confidence

---

### coaching_style_preference
Type:
- string

Allowed values:
- patient_step_by_step
- direct_technical_feedback
- high_energy_motivation
- drill_heavy_practice
- game_situation_coaching

Purpose:
- CoachingStyleFit scoring

---

### lesson_frequency_intent
Type:
- string

Allowed values:
- one_time_trial
- occasional
- weekly_long_term

Purpose:
- CommitmentFit scoring

---

## 4. Example Athlete Profiles

### Example 1: First-Time Beginner
- athlete_name: Mia Johnson
- city: Dallas
- sport: softball
- lesson_type: hitting
- athlete_age: 11
- budget_max: 50
- preferred_days: Monday,Wednesday
- preferred_time: evening
- radius_miles: 10
- skill_level: beginner
- main_goal: build_fundamentals
- improvement_area: swing_consistency
- prior_private_coaching: never
- coaching_style_preference: patient_step_by_step
- lesson_frequency_intent: one_time_trial

Expected recommendation style:
- beginner-friendly coach
- patient coaching style
- fundamentals-oriented
- strong confidence-building support

---

### Example 2: Competitive Intermediate Athlete
- athlete_name: Ryan Patel
- city: Austin
- sport: baseball
- lesson_type: pitching
- athlete_age: 14
- budget_max: 75
- preferred_days: Tuesday,Thursday,Saturday
- preferred_time: evening
- radius_miles: 15
- skill_level: intermediate
- main_goal: improve_technique
- improvement_area: pitching_control
- prior_private_coaching: a_few_times
- coaching_style_preference: direct_technical_feedback
- lesson_frequency_intent: weekly_long_term

Expected recommendation style:
- technical specialist
- strong pitching-control support
- reliable recurring lesson candidate

---

### Example 3: Advanced Tryout Prep Athlete
- athlete_name: Jordan Lee
- city: Houston
- sport: softball
- lesson_type: pitching
- athlete_age: 16
- budget_max: 85
- preferred_days: Monday,Friday,Saturday
- preferred_time: evening
- radius_miles: 25
- skill_level: advanced
- main_goal: prepare_for_tryouts
- improvement_area: confidence_under_pressure
- prior_private_coaching: regularly
- coaching_style_preference: game_situation_coaching
- lesson_frequency_intent: occasional

Expected recommendation style:
- competitive or tryout-prep coach
- advanced-level fit
- performance-under-pressure support

---

## 5. API Payload Shape

The backend live match endpoint should eventually accept:

{
  "athlete_name": "Alex Carter",
  "city": "Dallas",
  "sport": "baseball",
  "lesson_type": "pitching",
  "athlete_age": 13,
  "budget_max": 65,
  "preferred_days": "Monday,Wednesday,Saturday",
  "preferred_time": "evening",
  "radius_miles": 15,
  "skill_level": "intermediate",
  "main_goal": "improve_technique",
  "improvement_area": "pitching_control",
  "prior_private_coaching": "a_few_times",
  "coaching_style_preference": "direct_technical_feedback",
  "lesson_frequency_intent": "weekly_long_term"
}

The backend can convert city to coordinates internally.

---

## 6. Product Principle
The athlete should not feel like they are filling out random filters.

The inputs should clearly answer:
- what kind of coach do I need?
- what am I trying to improve?
- how do I learn best?
- what kind of lesson relationship am I looking for?

That is what makes the system feel like recommendation instead of search.