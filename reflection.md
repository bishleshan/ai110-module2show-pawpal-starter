# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial UML design included four core classes: `Task`, `Pet`, `Owner`, and `Scheduler`. I started by thinking about the real-world entities a pet care app would need to model. `Task` represents a single care activity (like a walk or feeding), with attributes for description, time, frequency, and completion status. `Pet` owns a list of tasks and stores basic info like name and species. `Owner` manages a collection of pets and provides a unified view of all tasks. `Scheduler` acts as the "brain" — it wraps an `Owner` and provides sorting, filtering, conflict detection, and task completion logic. I used Python `dataclasses` for `Task` and `Pet` to keep attribute definitions clean and concise.

**b. Design changes**

Yes, the design evolved during implementation. Originally I considered giving `Scheduler` its own task storage separate from `Pet`, but I quickly realized that was unnecessary complexity — tasks belong to pets, and the scheduler should just read through the owner's pets to gather them. I also added a `mark_task_complete` method to `Scheduler` (instead of calling it directly on `Task`) so that the scheduler could handle the auto-rescheduling side effect (creating a new recurring task and adding it to the pet). This kept the UI and CLI code clean — they just call `scheduler.mark_task_complete(pet, task)` and don't need to know the rescheduling logic.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler currently considers two main constraints: **time** (tasks have a scheduled time string like "08:00") and **recurrence** (tasks can be once, daily, or weekly). The `sort_by_time()` method orders tasks chronologically so the daily schedule is easy to read. The `detect_conflicts()` method checks whether two tasks share the same time and due date — flagging potential scheduling overlaps. I prioritized time ordering because a pet care schedule is inherently time-driven: morning walk at 07:30, feeding at 08:00, vet at 14:00. Getting that order right is the most useful output for an owner.

**b. Tradeoffs**

One key tradeoff is that the current scheduler sorts by time string lexicographically rather than parsing time objects. This works correctly as long as times are in 24-hour "HH:MM" format (which the UI enforces via Streamlit's `time_input`), but it would break with 12-hour AM/PM strings. I accepted this tradeoff because it keeps the implementation simple and the Streamlit UI guarantees the correct format. A future version should parse times into `datetime.time` objects for more robust sorting.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI assistance throughout this project. During the design phase, I asked the AI to help me brainstorm what attributes and methods each class should have — for example, whether `Scheduler` should own its own task list or delegate to `Owner`. During implementation, I used AI to generate the initial class skeletons based on my UML, and then fleshed out the logic myself. For the test suite, I described the behaviors I wanted to verify (recurrence, conflict detection, filtering) and asked the AI to suggest test cases, which I then reviewed and cleaned up. For the Streamlit UI, I described the tabs and features I wanted and used AI to scaffold the layout.

**b. Judgment and verification**

One moment where I didn't accept the AI suggestion as-is was in the conflict detection logic. The AI initially suggested detecting conflicts by comparing only time strings, without considering the `due_date`. I realized this would cause false positives — a daily morning walk on Monday and another walk on Tuesday would both be at "07:30" and incorrectly be flagged as a conflict. I updated the logic to use `(task.time, task.due_date)` as the composite key, which correctly limits conflict detection to tasks on the same day. I verified this by writing the `test_no_false_conflicts` test case.

---

## 4. Testing and Verification

**a. What you tested**

I tested the following behaviors: marking a task complete changes its status; adding a task increases the pet's task count; daily tasks reschedule to the next day; weekly tasks reschedule to the next week; one-time tasks do not reschedule; `sort_by_time` returns tasks in chronological order; `filter_tasks` correctly filters by pet name; `filter_tasks` correctly filters by completion status; `detect_conflicts` catches two tasks at the same time on the same date; `detect_conflicts` does not flag tasks at different times as conflicts; and a pet with no tasks returns an empty pending list. These tests are important because they cover the core scheduling behaviors that the app depends on — if any of these break, the schedule output would be wrong or misleading.

**b. Confidence**

I'm fairly confident the core scheduler logic is correct for the cases covered by the test suite. The main edge cases I'd test next with more time are: tasks that span midnight (e.g., a late-night feeding that pushes into the next day), pets with very large task lists for performance, and the behavior when an owner has no pets at all.

---

## 5. Reflection

**a. What went well**

I'm most satisfied with the separation of concerns in the architecture. The `pawpal_system.py` backend is completely independent of the UI — it can be tested with pytest, run from the CLI via `main.py`, and connected to Streamlit via `app.py` without any changes to the core logic. This made debugging much easier: I could verify the scheduler's output in the terminal before worrying about the UI at all.

**b. What you would improve**

If I had another iteration, I'd add a `priority` field to `Task` (high/medium/low) and use it as a secondary sort key in the scheduler — tasks at the same time would be ordered by priority. I'd also add time duration to tasks so the scheduler can detect not just exact-time conflicts but overlapping time windows (e.g., a 30-minute walk starting at 08:00 conflicts with a task at 08:15).

**c. Key takeaway**

The most important thing I learned is that designing the system on paper (UML) before writing code pays off significantly. Because I had a clear class diagram upfront, the implementation was straightforward — each class had defined responsibilities, and I never ended up with tangled logic where one class was doing too many things. AI collaboration worked best as a sounding board during design and a scaffolding tool during implementation, but the judgment calls — like how to handle conflict detection correctly — still required human reasoning and verification through tests.
