# 2–3 Minute Presentation Demo Script (Person B: AI Recommendation Engine)

This demo showcases the AI/ML personalized study planner, adaptive learning engine, and LLM fallback system for our team presentation.

---

## Demo Overview
* **Presenter:** Person B (AI Engine & Recommendation Lead)
* **Duration:** ~2.5 Minutes
* **Key Message:** *"Our rule-based engine generates customized study plans within daily time budgets, dynamically adapts when a student passes a quiz, and protects the system with deterministic fallbacks if the LLM is offline."*

---

## Live Demo Walkthrough

### Part 1: Initial Weak Learner Plan (0:00 – 0:45)
**What to say:**
> *"Here we have a student profile with a 60-minute daily study budget. The student is strong in variables and conditions, but scored only 25% on loops. Let's run our study planner."*

**Terminal Command:**
```bash
python -c "import json; from ai_engine.recommendation.study_planner import build_plan; data = json.load(open('tests/test_learners/learner_one_weak.json')); print(json.dumps(build_plan(data), indent=2))"
```

**Key Points to Highlight:**
* Point out that `loops` is scheduled first with activity `"relearn"` for 30 minutes.
* Show that `total_minutes` (55 min) is within `daily_minutes` (60 min).
* Read the generated reason: *"Your study plan prioritizes loops (25% mastery) with 30 minutes of focused relearning."*

---

### Part 2: Adaptive Learning After a Quiz (0:45 – 1:30)
**What to say:**
> *"Now, the learner studies loops and takes a topic quiz. Person A's analysis module scores the attempt at 90%. Watch how our adaptive engine immediately recalculates the plan."*

**Terminal Command:**
```bash
python -c "import json; from tests.test_adaptive_learning import simulate_quiz_result; from ai_engine.recommendation.adaptive_learning import adapt_plan; before = json.load(open('tests/test_learners/learner_one_weak.json')); after = simulate_quiz_result(before, 'loops', 90); res = adapt_plan(before, after); print('CHANGES:'); [print('-', c) for c in res['changes']]; print('\nNEW PLAN TOPICS:'); [print(f\"  {t['topic']}: {t['activity']} ({t['minutes']}m)\") for t in res['plan']['recommended_topics']]"
```

**Key Points to Highlight:**
* Show the `changes` list: `"Topic 'loops' activity changed from 'relearn' to 'advance'."`
* Show how the learner automatically progresses to the next topics (`conditions`, `lists`, `variables`).

---

### Part 3: Offline LLM Explainer & Bulletproof Fallback (1:30 – 2:15)
**What to say:**
> *"When a learner gets a question wrong, our system provides a clear explanation. We designed our LLM caller to be completely resilient: if there is no internet, no API key, or the LLM times out, it never crashes; it returns a clean template explanation."*

**Terminal Command:**
```bash
python -c "from ai_engine.llm.ai_explainer import explain_wrong_answer; print(explain_wrong_answer('What keyword defines a function in Python?', 'func', 'def', 'Python functions use the def keyword.'))"
```

**Key Points to Highlight:**
* Output: *"You selected 'func', but the correct answer is 'def'. Explanation: Python functions use the def keyword."*
* Explain that the core logic is 100% deterministic and safe.

---

### Part 4: Conclusion & Test Suite Verification (2:15 – 2:30)
**What to say:**
> *"Every component has strict automated unit tests covering all 8 learner profiles, prerequisite gating, and budget invariants. All 27 tests pass in under 0.2 seconds."*

**Terminal Command:**
```bash
python -m unittest discover -s tests -t . -v
```
