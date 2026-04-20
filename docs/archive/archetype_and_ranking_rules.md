# Coach Archetypes and Ranking Impact Rules

## 1. Goal
The recommendation must visibly change when athlete context changes.

A beginner building fundamentals should not usually get the same coach as an advanced athlete preparing for tryouts.

---

## 2. Coach Archetypes

### Archetype A: Beginner Fundamentals Coach
Best for:
- beginners
- first-time private coaching
- fundamentals
- confidence building

Typical traits:
- beginner_friendly = true
- preferred_athlete_levels = beginner|intermediate
- coaching_style = patient_step_by_step
- goals_supported = build_fundamentals|build_confidence|improve_technique
- lesson_frequency_fit = one_time_trial|occasional

Should win when:
- skill_level = beginner
- prior_private_coaching = never
- main_goal = build_fundamentals
- coaching_style_preference = patient_step_by_step

---

### Archetype B: Technical Skill Specialist
Best for:
- intermediate athletes
- technique correction
- lesson-specific improvement

Typical traits:
- beginner_friendly = false or mixed
- preferred_athlete_levels = intermediate|advanced
- coaching_style = direct_technical_feedback
- goals_supported = improve_technique|improve_game_performance
- strong exact improvement-area support
- lesson_frequency_fit = occasional|weekly_long_term

Should win when:
- skill_level = intermediate
- main_goal = improve_technique
- improvement_area is specific
- coaching_style_preference = direct_technical_feedback

---

### Archetype C: Competitive Performance Coach
Best for:
- advanced athletes
- tryout prep
- game performance
- pressure readiness

Typical traits:
- preferred_athlete_levels = advanced
- coaching_style = game_situation_coaching
- goals_supported = prepare_for_tryouts|improve_game_performance|improve_technique
- high reliability
- lesson_frequency_fit = occasional|weekly_long_term

Should win when:
- skill_level = advanced
- main_goal = prepare_for_tryouts or improve_game_performance
- prior_private_coaching = regularly
- coaching_style_preference = game_situation_coaching

---

### Archetype D: Confidence / Engagement Coach
Best for:
- nervous beginners
- younger athletes
- athletes needing comfort and motivation

Typical traits:
- beginner_friendly = true
- preferred_athlete_levels = beginner|intermediate
- coaching_style = high_energy_motivation
- goals_supported = build_confidence|build_fundamentals
- lesson_frequency_fit = one_time_trial|occasional

Should win when:
- skill_level = beginner
- main_goal = build_confidence
- prior_private_coaching = never
- coaching_style_preference = high_energy_motivation

---

### Archetype E: Athletic Development Coach
Best for:
- speed
- explosiveness
- movement work
- athletic performance development

Typical traits:
- preferred_athlete_levels = intermediate|advanced
- coaching_style = drill_heavy_practice
- goals_supported = strength_speed_development|improve_game_performance
- lesson_frequency_fit = occasional|weekly_long_term

Should win when:
- lesson_type = strength_and_conditioning or speed_and_agility
- main_goal = strength_speed_development
- coaching_style_preference = drill_heavy_practice

---

## 3. Archetype Assignment Rules for Dataset

### pitching coaches
Allowed primary archetypes:
- Beginner Fundamentals Coach
- Technical Skill Specialist
- Competitive Performance Coach

### hitting coaches
Allowed primary archetypes:
- Beginner Fundamentals Coach
- Technical Skill Specialist
- Competitive Performance Coach
- Confidence / Engagement Coach

### catching coaches
Allowed primary archetypes:
- Beginner Fundamentals Coach
- Technical Skill Specialist

### infield / outfield / fielding coaches
Allowed primary archetypes:
- Beginner Fundamentals Coach
- Technical Skill Specialist
- Competitive Performance Coach

### strength_and_conditioning / speed_and_agility coaches
Allowed primary archetype:
- Athletic Development Coach

---

## 4. Strict Ranking Rules

### Rule A: Beginner protection
If:
- skill_level = beginner
- prior_private_coaching = never

Then:
- strongly boost beginner_friendly coaches
- strongly boost patient_step_by_step
- strongly boost build_fundamentals and build_confidence
- penalize advanced-only coaches
- penalize game_situation_coaching
- penalize prepare_for_tryouts-heavy coaches

This must visibly change the top recommendation.

---

### Rule B: Intermediate technical preference
If:
- skill_level = intermediate
- main_goal = improve_technique

Then:
- strongly boost exact lesson_type fit
- strongly boost exact improvement_area fit
- strongly boost direct_technical_feedback
- strongly boost intermediate support

This should usually surface Technical Skill Specialists.

---

### Rule C: Advanced competitive preference
If:
- skill_level = advanced
- main_goal = improve_game_performance or prepare_for_tryouts
- prior_private_coaching = regularly

Then:
- strongly boost advanced-only coaches
- strongly boost game_situation_coaching
- strongly boost Competitive Performance Coaches
- penalize beginner-development coaches

This should usually produce a different top coach than beginner scenarios.

---

### Rule D: Coaching style mismatch must matter
Examples:
- athlete wants patient_step_by_step and coach is game_situation_coaching -> real penalty
- athlete wants direct_technical_feedback and coach is only high_energy_motivation -> real penalty

Style mismatch cannot be just cosmetic.

---

### Rule E: Lesson frequency must matter
If:
- lesson_frequency_intent = one_time_trial

Then boost:
- beginner-friendly
- intro-safe
- one_time_trial fit

If:
- lesson_frequency_intent = weekly_long_term

Then boost:
- repeat_booking_rate
- reliability
- weekly_long_term fit

---

## 5. Inputs That Must Materially Affect Ranking

These fields stay only if they visibly shift winners or top-3 ordering:

- lesson_type
- skill_level
- main_goal
- improvement_area
- prior_private_coaching
- coaching_style_preference
- lesson_frequency_intent

If a field only changes decimals and not rank behavior, either:
- increase its weight
- increase coach differentiation
- or remove the field

---

## 6. Interview Demo Personas

### Persona 1: Beginner Fundamentals
- sport = baseball
- lesson_type = hitting
- skill_level = beginner
- main_goal = build_fundamentals
- improvement_area = swing_consistency
- prior_private_coaching = never
- coaching_style_preference = patient_step_by_step
- lesson_frequency_intent = one_time_trial

Expected winner:
- Beginner Fundamentals Coach

---

### Persona 2: Intermediate Technique
- sport = baseball
- lesson_type = hitting
- skill_level = intermediate
- main_goal = improve_technique
- improvement_area = swing_consistency
- prior_private_coaching = a_few_times
- coaching_style_preference = direct_technical_feedback
- lesson_frequency_intent = weekly_long_term

Expected winner:
- Technical Skill Specialist

---

### Persona 3: Advanced Performance
- sport = baseball
- lesson_type = hitting or outfield
- skill_level = advanced
- main_goal = improve_game_performance
- improvement_area = confidence_under_pressure or reaction_speed
- prior_private_coaching = regularly
- coaching_style_preference = game_situation_coaching
- lesson_frequency_intent = weekly_long_term

Expected winner:
- Competitive Performance Coach

These personas should not usually return the same top coach.