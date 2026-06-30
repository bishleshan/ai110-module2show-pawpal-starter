# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

### Run the CLI demo

```bash
python main.py
```

## Sample Output

Sample CLI output from `python main.py`:

```
==================================================
TODAY'S SCHEDULE for Alex
==================================================
 Buddy        | [07:30] Morning Walk (daily) - due 2026-06-30 [pending]
 Whiskers     | [07:30] Breakfast (daily) - due 2026-06-30 [pending]
 Buddy        | [09:00] Flea Medicine (weekly) - due 2026-06-30 [pending]
 Whiskers     | [14:00] Vet Checkup (once) - due 2026-06-30 [pending]
 Whiskers     | [17:00] Playtime (daily) - due 2026-06-30 [pending]
 Buddy        | [18:00] Evening Walk (daily) - due 2026-06-30 [pending]

CONFLICT CHECK
  CONFLICT at 07:30: Buddy vs Whiskers

After completing Morning Walk:
  [07:30] Morning Walk (daily) - due 2026-06-30 [done]
  [18:00] Evening Walk (daily) - due 2026-06-30 [pending]
  [09:00] Flea Medicine (weekly) - due 2026-06-30 [pending]
  [07:30] Morning Walk (daily) - due 2026-07-01 [pending]
```

## Testing PawPal+

```bash
# Run the full test suite:
pytest tests/

# Run with verbose output:
pytest tests/ -v
```

Sample test output:

```
============================= test session starts ==============================
platform linux -- Python 3.11.0, pytest-8.x.x
collected 11 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED          [  9%]
tests/test_pawpal.py::test_adding_task_increases_pet_task_count PASSED  [ 18%]
tests/test_pawpal.py::test_daily_task_recurrence PASSED                 [ 27%]
tests/test_pawpal.py::test_weekly_task_recurrence PASSED                [ 36%]
tests/test_pawpal.py::test_once_task_no_recurrence PASSED               [ 45%]
tests/test_pawpal.py::test_sort_by_time PASSED                          [ 54%]
tests/test_pawpal.py::test_filter_by_pet PASSED                         [ 63%]
tests/test_pawpal.py::test_filter_by_status PASSED                      [ 72%]
tests/test_pawpal.py::test_conflict_detection PASSED                    [ 81%]
tests/test_pawpal.py::test_no_false_conflicts PASSED                    [ 90%]
tests/test_pawpal.py::test_pet_with_no_tasks PASSED                     [100%]

============================== 11 passed in 0.42s ==============================
```

## Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts all tasks chronologically by HH:MM time string |
| Filtering | `Scheduler.filter_tasks(pet_name, completed)` | Filters by pet name and/or completion status; supports combining both filters |
| Conflict handling | `Scheduler.detect_conflicts()` | Detects tasks sharing the same time AND due date across different pets |
| Recurring tasks | `Task.mark_complete()` | Returns a new Task with due_date shifted +1 day (daily) or +7 days (weekly); one-time tasks return None |

## Demo Walkthrough

1. **Launch the app** with `streamlit run app.py` — the sidebar loads with a default owner name "Alex" and prompts you to add a pet.
2. **Add a pet** — enter a pet name (e.g., "Buddy") and species (e.g., "Dog") in the sidebar and click "Add Pet". The pet appears in the sidebar pet list.
3. **Add tasks** — go to the Tasks tab, select your pet, enter a description ("Morning walk"), choose a time (07:30), set frequency to "daily", and click "Add Task". Repeat to add more tasks.
4. **View today's schedule** — switch to the "Today's Schedule" tab to see all tasks for today sorted by time, with status icons showing pending vs. completed tasks.
5. **Check for conflicts** — open the Conflicts tab. If two tasks are scheduled at the same time on the same date, they appear highlighted as conflicts. Otherwise a green success message confirms no conflicts.
6. **Complete a task** — go to the "Complete a Task" tab, select a pending task from the dropdown, and click "Mark Complete". Daily/weekly tasks automatically reschedule with the next due date shown in a success message.
7. **Filter tasks** — use the "Filter Tasks" tab to filter by pet name and/or completion status to view exactly the tasks you care about.
