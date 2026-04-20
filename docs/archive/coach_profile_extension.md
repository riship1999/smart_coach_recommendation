# Coach Profile Extension for Personalized Recommendation

## 1. Purpose
These fields exist only to support the personalized recommendation layer.

Basic filtering already uses:
- sport
- specialty
- radius
- budget
- availability

The new fields are used to decide:
**Which eligible coach is the best first-fit coach for this athlete?**

---

## 2. New Columns to Add to coaches.csv

Add these columns after `bio`:

- goals_supported
- improvement_areas_supported
- preferred_athlete_levels
- coaching_style
- beginner_friendly
- repeat_booking_rate
- cancellation_rate
- lesson_frequency_fit

Full header becomes:

id,name,sport,specialty,division_level,years_experience,city,state,latitude,longitude,hourly_price,avg_rating,review_count,completion_rate,response_rate,bio,goals_supported,improvement_areas_supported,preferred_athlete_levels,coaching_style,beginner_friendly,repeat_booking_rate,cancellation_rate,lesson_frequency_fit

---

## 3. Exact Meaning of Each Field

### goals_supported
What type of athlete goal this coach is best for.

**Type:**
- pipe-separated string

**Allowed values:**
- build_fundamentals
- improve_technique
- prepare_for_tryouts
- build_confidence
- improve_game_performance
- strength_speed_development

**Used in scoring:**
- GoalFit

**Example:**
- build_fundamentals|build_confidence|improve_technique

---

### improvement_areas_supported
Specific problem areas the coach is good at improving.

**Type:**
- pipe-separated string

**Allowed values:**
- pitching_control
- pitching_velocity
- swing_consistency
- contact_hitting
- fielding_footwork
- catching_mechanics
- throwing_accuracy
- reaction_speed
- confidence_under_pressure

**Used in scoring:**
- PainPointFit

**Example:**
- pitching_control|throwing_accuracy|confidence_under_pressure

---

### preferred_athlete_levels
Which athlete levels the coach works best with.

**Type:**
- pipe-separated string

**Allowed values:**
- beginner
- intermediate
- advanced

**Used in scoring:**
- SkillFit

**Example:**
- beginner|intermediate

---

### coaching_style
The coach’s primary teaching style.

**Type:**
- string

**Allowed values:**
- patient_step_by_step
- direct_technical_feedback
- high_energy_motivation
- drill_heavy_practice
- game_situation_coaching

**Used in scoring:**
- CoachingStyleFit

**Example:**
- patient_step_by_step

---

### beginner_friendly
Whether the coach is especially good for first-time, lower-confidence, or early-stage athletes.

**Type:**
- boolean

**Allowed values:**
- true
- false

**Used in scoring:**
- SkillFit
- confidence_label
- recommendation_rationale

**Example:**
- true

---

### repeat_booking_rate
How often athletes return for additional lessons after a completed first lesson.

**Type:**
- float

**Range:**
- 0.30 to 0.95

**Used in scoring:**
- ReliabilityFit

**Example:**
- 0.74

---

### cancellation_rate
How often booked lessons are canceled or rescheduled.

**Type:**
- float

**Range:**
- 0.00 to 0.25

**Used in scoring:**
- tradeoff_note
- future reliability penalty if needed

**Example:**
- 0.06

---

### lesson_frequency_fit
What lesson cadence this coach is best suited for.

**Type:**
- pipe-separated string

**Allowed values:**
- one_time_trial
- occasional
- weekly_long_term

**Used in scoring:**
- CommitmentFit

**Example:**
- one_time_trial|occasional

---

## 4. Mapping to Recommendation Formula

### GoalFit
**Uses:**
- goals_supported

**Rule:**
- exact match -> 1.0
- adjacent/partial support -> 0.5
- no support -> 0.0

---

### PainPointFit
**Uses:**
- improvement_areas_supported

**Rule:**
- exact match -> 1.0
- related support -> 0.5
- no support -> 0.0

---

### SkillFit
**Uses:**
- preferred_athlete_levels
- beginner_friendly
- division_level

**Rule:**
- athlete level included in preferred_athlete_levels -> strong fit
- beginner + beginner_friendly=true -> bonus
- advanced athlete with only beginner support -> low fit

---

### CoachingStyleFit
**Uses:**
- coaching_style

**Rule:**
- exact match -> 1.0
- somewhat compatible -> 0.5
- mismatch -> 0.0

---

### ReliabilityFit
**Uses:**
- completion_rate
- response_rate
- repeat_booking_rate

**Formula:**
ReliabilityFit =
0.5 * completion_rate +
0.3 * response_rate +
0.2 * repeat_booking_rate

---

### CommitmentFit
**Uses:**
- lesson_frequency_fit

**Rule:**
- exact fit -> 1.0
- acceptable fit -> 0.5
- weak fit -> 0.0

---

## 5. Coach Archetypes to Use for Mock Data

To avoid random fake values, assign each coach one of these archetypes.

### Archetype A: Beginner Development Coach
**Best for:**
- beginners
- first-time private coaching
- confidence building
- fundamentals

**Typical values:**
- goals_supported = build_fundamentals|build_confidence|improve_technique
- preferred_athlete_levels = beginner|intermediate
- coaching_style = patient_step_by_step
- beginner_friendly = true
- repeat_booking_rate = 0.60 to 0.78
- cancellation_rate = 0.03 to 0.08
- lesson_frequency_fit = one_time_trial|occasional

---

### Archetype B: Technical Skill Specialist
**Best for:**
- intermediate to advanced athletes
- technique correction
- position-specific improvement

**Typical values:**
- goals_supported = improve_technique|improve_game_performance
- preferred_athlete_levels = intermediate|advanced
- coaching_style = direct_technical_feedback
- beginner_friendly = false
- repeat_booking_rate = 0.68 to 0.85
- cancellation_rate = 0.02 to 0.06
- lesson_frequency_fit = occasional|weekly_long_term

---

### Archetype C: Competitive / Tryout Prep Coach
**Best for:**
- advanced athletes
- competitive training
- tryout preparation
- pressure performance

**Typical values:**
- goals_supported = prepare_for_tryouts|improve_game_performance|improve_technique
- preferred_athlete_levels = advanced
- coaching_style = game_situation_coaching
- beginner_friendly = false
- repeat_booking_rate = 0.72 to 0.88
- cancellation_rate = 0.02 to 0.05
- lesson_frequency_fit = occasional|weekly_long_term

---

### Archetype D: Athletic Performance Coach
**Best for:**
- speed
- reaction
- general performance development

**Typical values:**
- goals_supported = strength_speed_development|improve_game_performance
- preferred_athlete_levels = intermediate|advanced
- coaching_style = drill_heavy_practice
- beginner_friendly = false
- repeat_booking_rate = 0.65 to 0.82
- cancellation_rate = 0.01 to 0.05
- lesson_frequency_fit = occasional|weekly_long_term

---

### Archetype E: High-Energy Motivator
**Best for:**
- confidence
- engagement
- younger athletes who respond to energy and encouragement

**Typical values:**
- goals_supported = build_confidence|build_fundamentals|improve_game_performance
- preferred_athlete_levels = beginner|intermediate
- coaching_style = high_energy_motivation
- beginner_friendly = true
- repeat_booking_rate = 0.58 to 0.76
- cancellation_rate = 0.03 to 0.09
- lesson_frequency_fit = one_time_trial|occasional|weekly_long_term

---

## 6. Concrete Sample Rows

### Tyler Brooks
**Archetype:**
- Technical Skill Specialist

**goals_supported:**
- improve_technique|prepare_for_tryouts|improve_game_performance

**improvement_areas_supported:**
- pitching_control|pitching_velocity|throwing_accuracy

**preferred_athlete_levels:**
- intermediate|advanced

**coaching_style:**
- direct_technical_feedback

**beginner_friendly:**
- false

**repeat_booking_rate:**
- 0.78

**cancellation_rate:**
- 0.04

**lesson_frequency_fit:**
- occasional|weekly_long_term

---

### Logan Bennett
**Archetype:**
- Beginner Development Coach

**goals_supported:**
- build_fundamentals|build_confidence|improve_technique

**improvement_areas_supported:**
- pitching_control|throwing_accuracy|confidence_under_pressure

**preferred_athlete_levels:**
- beginner|intermediate

**coaching_style:**
- patient_step_by_step

**beginner_friendly:**
- true

**repeat_booking_rate:**
- 0.62

**cancellation_rate:**
- 0.08

**lesson_frequency_fit:**
- one_time_trial|occasional

---

### Sarah Collins
**Archetype:**
- Competitive / Tryout Prep Coach

**goals_supported:**
- improve_technique|prepare_for_tryouts|improve_game_performance

**improvement_areas_supported:**
- pitching_control|pitching_velocity|confidence_under_pressure

**preferred_athlete_levels:**
- intermediate|advanced

**coaching_style:**
- direct_technical_feedback

**beginner_friendly:**
- false

**repeat_booking_rate:**
- 0.84

**cancellation_rate:**
- 0.03

**lesson_frequency_fit:**
- occasional|weekly_long_term

---

### Olivia Turner
**Archetype:**
- Beginner Development Coach

**goals_supported:**
- build_fundamentals|improve_technique|build_confidence

**improvement_areas_supported:**
- swing_consistency|contact_hitting|confidence_under_pressure

**preferred_athlete_levels:**
- beginner|intermediate

**coaching_style:**
- patient_step_by_step

**beginner_friendly:**
- true

**repeat_booking_rate:**
- 0.73

**cancellation_rate:**
- 0.05

**lesson_frequency_fit:**
- one_time_trial|occasional|weekly_long_term

---

### Caleb Morgan
**Archetype:**
- Athletic Performance Coach

**goals_supported:**
- strength_speed_development|improve_game_performance

**improvement_areas_supported:**
- reaction_speed|throwing_accuracy

**preferred_athlete_levels:**
- intermediate|advanced

**coaching_style:**
- drill_heavy_practice

**beginner_friendly:**
- false

**repeat_booking_rate:**
- 0.76

**cancellation_rate:**
- 0.02

**lesson_frequency_fit:**
- occasional|weekly_long_term

---

## 7. Rule for Assigning Fields to All 20 Coaches

For every coach:
1. Pick one archetype first
2. Assign values consistent with that archetype
3. Make sure specialty and improvement areas make sense together
4. Make sure beginner_friendly and preferred_athlete_levels are consistent
5. Keep repeat_booking_rate and cancellation_rate believable relative to rating, response_rate, and completion_rate

---

## 8. Output Quality Goal
The dataset should be realistic enough that when a youth athlete answers personalization questions, the system can produce recommendation reasons that feel specific and believable rather than generic.