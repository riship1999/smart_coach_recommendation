# Synthetic Data Dictionary

## 1. Sports
Supported sports for MVP:
- baseball
- softball

## 2. Lesson Types / Specialties

### Baseball
- pitching
- hitting
- catching
- infield
- outfield
- strength_and_conditioning

### Softball
- pitching
- hitting
- fielding
- catching
- speed_and_agility

## 3. Skill Levels
- beginner
- intermediate
- advanced

## 4. Division Levels
- D1
- D2
- D3
- NAIA
- JUCO

## 5. Cities
Use a small set of realistic cities for the MVP:
- Dallas, TX
- Austin, TX
- Houston, TX
- Oklahoma City, OK
- Norman, OK
- Tulsa, OK

## 6. Availability Day Values
- Monday
- Tuesday
- Wednesday
- Thursday
- Friday
- Saturday
- Sunday

## 7. Preferred Time Values
- morning
- afternoon
- evening

## 8. Coach Profile Ranges

### years_experience
- integer from 1 to 8

### hourly_price
Suggested ranges:
- baseball: 35 to 90
- softball: 30 to 85

### avg_rating
- float from 3.5 to 5.0

### review_count
- integer from 0 to 80

### completion_rate
- float from 0.70 to 1.00

### response_rate
- float from 0.60 to 1.00

## 9. Athlete Age Range
- integer from 8 to 18

## 10. Parent Budget Range
- float from 30 to 100

## 11. Search Radius
- 5
- 10
- 15
- 25

## 12. Booking Outcome Logic
Historical bookings should look realistic:
- higher-rated coaches should be slightly more likely to be clicked
- coaches within budget should be more likely to be booked
- availability overlap should improve booking probability
- very high prices should reduce booking probability
- completed lessons should usually follow booked lessons
- review_submitted should usually follow completed lessons

## 13. Pricing Recommendation Logic Inputs
Use these variables to drive recommended price:
- sport
- specialty
- division_level
- years_experience
- avg_rating
- review_count
- completion_rate
- city

## 14. Matching Recommendation Logic Inputs
Use these variables to drive coach ranking:
- sport match
- specialty match
- skill level fit
- budget fit
- distance fit
- availability overlap
- rating score
- completion rate