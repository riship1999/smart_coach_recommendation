# Option Matrix

## 1. Purpose
The personalization form should not allow loose or irrelevant combinations.

Every visible input must either:
- constrain downstream options
- materially affect ranking
- improve recommendation explanation

---

## 2. Sport -> Lesson Types

### baseball
- pitching
- hitting
- catching
- infield
- outfield
- strength_and_conditioning

### softball
- pitching
- hitting
- catching
- fielding
- speed_and_agility

---

## 3. Lesson Type -> Improvement Areas

### pitching
- pitching_control
- pitching_velocity
- throwing_accuracy
- confidence_under_pressure

### hitting
- swing_consistency
- contact_hitting
- confidence_under_pressure

### catching
- catching_mechanics
- throwing_accuracy
- confidence_under_pressure

### infield
- fielding_footwork
- reaction_speed
- throwing_accuracy

### outfield
- fielding_footwork
- reaction_speed
- throwing_accuracy

### fielding
- fielding_footwork
- reaction_speed
- throwing_accuracy

### strength_and_conditioning
- reaction_speed
- throwing_accuracy

### speed_and_agility
- reaction_speed
- fielding_footwork

---

## 4. Lesson Type -> Main Goals

### pitching
- build_fundamentals
- improve_technique
- prepare_for_tryouts
- build_confidence
- improve_game_performance

### hitting
- build_fundamentals
- improve_technique
- prepare_for_tryouts
- build_confidence
- improve_game_performance

### catching
- build_fundamentals
- improve_technique
- build_confidence
- improve_game_performance

### infield
- build_fundamentals
- improve_technique
- prepare_for_tryouts
- improve_game_performance

### outfield
- build_fundamentals
- improve_technique
- prepare_for_tryouts
- improve_game_performance

### fielding
- build_fundamentals
- improve_technique
- prepare_for_tryouts
- improve_game_performance

### strength_and_conditioning
- strength_speed_development
- improve_game_performance

### speed_and_agility
- strength_speed_development
- improve_game_performance

---

## 5. Skill Level -> Main Goals

### beginner
- build_fundamentals
- build_confidence
- improve_technique

### intermediate
- improve_technique
- improve_game_performance
- prepare_for_tryouts
- build_confidence

### advanced
- improve_technique
- prepare_for_tryouts
- improve_game_performance

---

## 6. Shared Global Inputs
These remain available across sports:
- skill_level
- prior_private_coaching
- coaching_style_preference
- lesson_frequency_intent

They are not dynamically filtered by sport, but they must meaningfully affect ranking.

---

## 7. UX Rules

### Rule 1
When sport changes:
- lesson type must reset if invalid
- improvement area must reset if invalid
- main goal must reset if invalid

### Rule 2
When lesson type changes:
- rebuild improvement area options
- rebuild main goal options

### Rule 3
When skill level changes:
- rebuild allowed main goals

### Rule 4
No stale invalid values should remain in form state.