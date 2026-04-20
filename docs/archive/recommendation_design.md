# Personalized Coach Recommendation Design

## 1. Product Goal
Help a youth athlete choose the best first-fit coach after basic filtering by applying a personalized recommendation layer.

## 2. Two-Stage System

### Stage 1: Eligibility Filtering
A coach must pass these conditions:
- same sport
- relevant lesson type
- within search radius
- within budget tolerance
- schedule overlap

### Stage 2: Personalized Recommendation
Among eligible coaches, rank them using deeper athlete-context signals:
- athlete goal
- improvement area
- prior coaching experience
- skill level
- coaching style preference
- lesson frequency intent
- coach reliability
- price comfort
- distance convenience

---

## 3. Youth Athlete Inputs

### Basic Filtering Inputs
- athlete_name
- sport
- lesson_type
- city
- age
- budget_max
- preferred_days
- preferred_time
- radius_miles

### Personalized Recommendation Inputs
- skill_level
- main_goal
- improvement_area
- prior_private_coaching
- coaching_style_preference
- lesson_frequency_intent

---

## 4. Personalized Input Options

### skill_level
- beginner
- intermediate
- advanced

### main_goal
- build_fundamentals
- improve_technique
- prepare_for_tryouts
- build_confidence
- improve_game_performance
- strength_speed_development

### improvement_area
Baseball / Softball examples:
- pitching_control
- pitching_velocity
- swing_consistency
- contact_hitting
- fielding_footwork
- catching_mechanics
- throwing_accuracy
- reaction_speed
- confidence_under_pressure

### prior_private_coaching
- never
- a_few_times
- regularly

### coaching_style_preference
- patient_step_by_step
- direct_technical_feedback
- high_energy_motivation
- drill_heavy_practice
- game_situation_coaching

### lesson_frequency_intent
- one_time_trial
- occasional
- weekly_long_term

---

## 5. Coach Attributes Needed

### Existing
- sport
- specialty
- city
- latitude
- longitude
- hourly_price
- avg_rating
- review_count
- completion_rate
- response_rate
- availability

### New Fields to Add
- goals_supported
- improvement_areas_supported
- preferred_athlete_levels
- coaching_style
- beginner_friendly
- repeat_booking_rate
- cancellation_rate
- lesson_frequency_fit

---

## 6. Recommendation Score Formula

Final score is applied only after eligibility filtering.

RecommendationScore =
0.25 * GoalFit +
0.20 * PainPointFit +
0.15 * SkillFit +
0.15 * CoachingStyleFit +
0.10 * ReliabilityFit +
0.08 * CommitmentFit +
0.04 * PriceComfort +
0.03 * DistanceConvenience

Total weight = 1.00

---

## 7. Component Definitions

### GoalFit
How well the coach supports the athlete's main goal.
- exact support = 1.0
- partial support = 0.5
- weak support = 0.0

### PainPointFit
How well the coach matches the athlete's specific improvement area.
- exact support = 1.0
- related support = 0.5
- weak support = 0.0

### SkillFit
How well the coach fits the athlete's current level.
Use:
- preferred_athlete_levels
- beginner_friendly
- division level as supporting signal

### CoachingStyleFit
How closely the coach's teaching style matches athlete preference.
- exact style match = 1.0
- related style = 0.5
- mismatch = 0.0

### ReliabilityFit
ReliabilityFit =
0.5 * completion_rate +
0.3 * response_rate +
0.2 * repeat_booking_rate

All values normalized to [0,1]

### CommitmentFit
How well the coach matches the athlete's lesson frequency intent.
- exact fit = 1.0
- acceptable fit = 0.5
- weak fit = 0.0

### PriceComfort
- comfortably under budget = 1.0
- near budget ceiling = 0.7
- slightly above budget = 0.3
- too expensive = 0.0

### DistanceConvenience
- under 5 miles = 1.0
- 5 to 10 miles = 0.8
- 10 to 15 miles = 0.6
- near radius edge = 0.4

---

## 8. Recommendation Output

For each top coach, return:
- rank
- coach_name
- recommendation_score
- current_price
- distance_miles
- shortlist_reasons
- recommendation_rationale
- tradeoff_note
- confidence_label

### shortlist_reasons
These explain why the coach passed the initial filtering stage.
Examples:
- within your budget
- matches your lesson type
- good schedule overlap
- within your search radius

### recommendation_rationale
These explain why the coach ranked highly after personalization.
Examples:
- strong fit for pitching control
- good match for beginner development
- matches your coaching style preference
- supports weekly long-term development
- high lesson reliability

### tradeoff_note
This explains any important compromise in the recommendation.
Examples:
- slightly farther away, but strongest technical fit
- best value option, but moderate experience level
- strongest beginner-friendly coach, though limited weekend slots

### confidence_label
- high_confidence_match
- moderate_confidence_match
- best_available_option

---

## 9. Product Principle
Filtering answers:
"Who is eligible?"

Recommendation answers:
"Who is the best first-fit coach for this athlete?"