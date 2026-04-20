# Matching Logic

## 1. Two-Stage Design

### Stage 1: Broad Eligibility
The app first filters coaches by:
- sport
- distance radius
- broad affordability

This produces the eligible coach pool.

### Stage 2: Personalized Ranking
The app then ranks that pool using athlete-specific recommendation inputs.

This separation is important because filtering and recommendation solve different problems.

---

## 2. Inputs Used in Ranking
The ranking stage uses:
- lesson_type
- skill_level
- main_goal
- improvement_area
- prior_private_coaching
- coaching_style_preference
- lesson_frequency_intent

---

## 3. Main Scoring Components

### lesson type fit
Rewards coaches whose specialty exactly matches or closely relates to the requested lesson type.

### goal fit
Rewards coaches whose supported goals match the athlete’s selected goal.

### improvement area fit
Rewards coaches whose supported improvement areas match the athlete’s selected focus area.

### skill fit
Rewards coaches whose preferred athlete levels align with the athlete’s current level.

### coaching style fit
Rewards alignment between the athlete’s preferred coaching style and the coach’s actual coaching style.

### reliability fit
Uses:
- completion_rate
- response_rate
- repeat_booking_rate
- cancellation_rate

### commitment fit
Rewards alignment between athlete lesson frequency intent and coach lesson frequency fit.

### price comfort
Rewards coaches who fit well within budget.

### distance convenience
Rewards closer coaches within the selected radius.

---

## 4. Archetype-Style Adjustments
In addition to base scoring, the app applies stronger adjustments for important athlete states.

### Beginner protection
If:
- skill_level = beginner
- prior_private_coaching = never

Then boost:
- beginner_friendly coaches
- patient_step_by_step coaches
- fundamentals and confidence-oriented coaches

And penalize:
- advanced-only coaches
- highly intense competitive coaching styles

### Intermediate technique emphasis
If:
- skill_level = intermediate
- main_goal = improve_technique

Then boost:
- exact lesson-type fit
- exact improvement-area fit
- direct_technical_feedback coaches

### Advanced performance emphasis
If:
- skill_level = advanced
- main_goal = improve_game_performance or prepare_for_tryouts
- prior_private_coaching = regularly

Then boost:
- advanced-level coaches
- game_situation_coaching
- performance-oriented coaches

And penalize:
- beginner-development coaches

### Style mismatch penalties
Style mismatch is treated as a real penalty, not a cosmetic one.

### Lesson frequency effects
- one_time_trial boosts intro-safe and trial-friendly coaches
- weekly_long_term boosts reliable long-term development coaches

---

## 5. Explainability Outputs
For every ranked coach, the app returns:
- recommendation_score
- shortlist_reasons
- recommendation_rationale
- tradeoff_note
- confidence_label

This makes the recommendation explainable rather than a black box.

---

## 6. What Good Behavior Looks Like
A strong recommendation system should often produce different top coaches for:

### Persona A
beginner + fundamentals + patient style

### Persona B
intermediate + technique + direct technical feedback

### Persona C
advanced + performance + game-situation coaching

If those personas repeatedly get the same top coach, the dataset or scoring rules are not differentiated enough.