# Database Schema

## 1. coaches
Stores coach profile and performance information.

| column_name        | type         | description |
|-------------------|--------------|-------------|
| id                | integer      | unique coach id |
| name              | string       | coach full name |
| sport             | string       | primary sport, e.g. baseball |
| specialty         | string       | lesson specialty, e.g. pitching |
| division_level    | string       | playing level, e.g. D1, D2, D3 |
| years_experience  | integer      | years of coaching experience |
| city              | string       | city name |
| state             | string       | state abbreviation |
| latitude          | float        | latitude for distance calculations |
| longitude         | float        | longitude for distance calculations |
| hourly_price      | float        | current lesson price |
| avg_rating        | float        | average rating from reviews |
| review_count      | integer      | number of reviews |
| completion_rate   | float        | percent of booked lessons completed |
| response_rate     | float        | percent of parent inquiries responded to |
| bio               | string       | short profile summary |

---

## 2. availability
Stores coach weekly availability windows.

| column_name | type    | description |
|------------|---------|-------------|
| id         | integer | unique row id |
| coach_id   | integer | foreign key to coaches.id |
| day_of_week| string  | Monday, Tuesday, etc. |
| start_time | string  | start time, e.g. 17:00 |
| end_time   | string  | end time, e.g. 20:00 |

---

## 3. parents
Stores parent/user information for search simulation.

| column_name | type    | description |
|------------|---------|-------------|
| id         | integer | unique parent id |
| name       | string  | parent name |
| city       | string  | city name |
| state      | string  | state abbreviation |

---

## 4. search_requests
Stores each search input submitted by a parent.

| column_name         | type    | description |
|--------------------|---------|-------------|
| id                 | integer | unique search request id |
| parent_id          | integer | foreign key to parents.id |
| sport              | string  | requested sport |
| lesson_type        | string  | requested lesson type / specialty |
| athlete_age        | integer | athlete age |
| skill_level        | string  | beginner, intermediate, advanced |
| budget_max         | float   | max budget parent is willing to pay |
| preferred_days     | string  | comma-separated days or JSON later |
| preferred_time     | string  | morning / afternoon / evening |
| search_latitude    | float   | parent search location latitude |
| search_longitude   | float   | parent search location longitude |
| radius_miles       | float   | acceptable search radius |

---

## 5. bookings
Stores historical search-to-book outcomes.

| column_name      | type    | description |
|-----------------|---------|-------------|
| id              | integer | unique booking record id |
| parent_id       | integer | foreign key to parents.id |
| coach_id        | integer | foreign key to coaches.id |
| request_id      | integer | foreign key to search_requests.id |
| shown_rank      | integer | rank position shown to parent |
| clicked         | boolean | whether parent clicked coach profile |
| booked          | boolean | whether a booking was made |
| completed       | boolean | whether the booked lesson was completed |
| review_submitted| boolean | whether the lesson was reviewed |

---

## 6. pricing_recommendations
Stores system-generated price recommendations for coaches.

| column_name       | type    | description |
|------------------|---------|-------------|
| id               | integer | unique row id |
| coach_id         | integer | foreign key to coaches.id |
| recommended_low  | float   | lower bound of recommended price |
| recommended_high | float   | upper bound of recommended price |
| explanation      | string  | text explanation of pricing logic |

---

## Relationships
- coaches.id -> availability.coach_id
- parents.id -> search_requests.parent_id
- parents.id -> bookings.parent_id
- coaches.id -> bookings.coach_id
- search_requests.id -> bookings.request_id
- coaches.id -> pricing_recommendations.coach_id