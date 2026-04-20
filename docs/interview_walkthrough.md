# Smart Coach Recommendation — Interview Walkthrough

## 1. Problem
Youth athletes often see many coach options after basic filtering by city, sport, and price. That creates choice overload.

The goal of this project is to go beyond filtering and build a recommendation layer that identifies the best first-fit coach for a specific athlete.

Instead of only asking:
- which coaches are available?

the system also asks:
- which coach is the best fit for this athlete’s skill level, learning style, and goals?

---

## 2. Product Flow

### Step 1: Basic Filters
The athlete enters:
- name
- city
- sport
- age
- budget
- radius

This creates a broad eligible coach pool.

### Step 2: Eligible Coach Pool
The app shows all coaches who pass broad eligibility:
- same sport
- within radius
- within broad affordability band

This step is intentionally broad so the recommendation stage has multiple candidates to rank.

### Step 3: Personalization
The athlete then provides:
- lesson type
- skill level
- main goal
- improvement area
- prior private coaching
- coaching style preference
- lesson frequency intent

These inputs drive the personalized ranking.

### Step 4: Recommendation
The app ranks the eligible pool and returns:
- best-fit coach
- recommendation score
- rationale
- tradeoff note
- alternative options

---

## 3. Why This Is Not Just Filtering
A pure filter flow would stop at “20 coaches match your search.”

This project adds a second stage that determines:
- which coach best fits a beginner vs advanced athlete
- which coach is better for fundamentals vs competitive development
- which coach matches the athlete’s coaching style preference
- which coach best supports the selected improvement area

That is the core difference between search and recommendation.

---

## 4. Key Product Design Decisions

### Broad filtering first
I intentionally kept Step 1 broad so the recommendation engine has a real candidate pool to rank.

### Dynamic personalization form
The personalization page does not show every possible option at once.
Instead:
- sport controls lesson types
- lesson type controls improvement areas
- lesson type and skill level constrain main goals

This prevents invalid or noisy combinations.

### Recommendation must visibly react
The ranking logic is designed so changing important athlete context should often change the top recommendation, especially for:
- beginner vs advanced
- fundamentals vs tryout prep
- patient vs technical coaching style

---

## 5. Ranking Logic Overview
The recommendation score combines:
- lesson type fit
- goal fit
- improvement area fit
- athlete level fit
- coaching style fit
- reliability
- lesson frequency fit
- price comfort
- distance convenience

On top of that, the system adds stronger adjustments for athlete archetypes, for example:
- beginner + no prior coaching boosts beginner-friendly, patient coaches
- advanced + performance goals boosts competitive, game-situation coaches

---

## 6. Example Demo Personas

### Persona A: Beginner Fundamentals
- baseball
- lesson type: hitting
- skill level: beginner
- main goal: build fundamentals
- improvement area: swing consistency
- prior coaching: never
- coaching style: patient step by step

Expected result:
- beginner-friendly fundamentals coach

### Persona B: Intermediate Technique
- baseball
- lesson type: hitting
- skill level: intermediate
- main goal: improve technique
- improvement area: swing consistency
- prior coaching: a few times
- coaching style: direct technical feedback

Expected result:
- technical skill specialist

### Persona C: Advanced Performance
- baseball
- lesson type: hitting or outfield
- skill level: advanced
- main goal: improve game performance
- prior coaching: regularly
- coaching style: game situation coaching

Expected result:
- competitive performance coach

---

## 7. Technical Implementation
The current app uses:
- React frontend
- FastAPI backend
- CSV-based mock dataset for coaches
- deterministic recommendation scoring logic

The product was structured this way so I could focus on recommendation behavior, form logic, and explainability before introducing a persistent database.

---

## 8. Why This Is Relevant to SideCoach
This project is relevant because it maps closely to the real marketplace problem:

- athletes need help choosing among multiple coaches
- basic search is not enough when users are unsure who is best for them
- different athletes need different coaching styles and development paths
- explainable recommendations increase trust in the platform

The value is not only ranking a coach higher. It is helping the athlete understand why that coach is the best fit.

---

## 9. What I Would Build Next
If I extended this beyond the demo, I would add:
- persistent athlete profiles
- saved recommendation requests
- click / booking / rebooking event tracking
- learning-to-rank or feedback-driven weight tuning
- schedule availability as a properly modeled supply dimension