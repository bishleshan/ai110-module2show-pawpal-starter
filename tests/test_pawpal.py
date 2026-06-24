"""tests/test_pawpal.py - Automated test suite for PawPal+."""
import pytest
from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


@pytest.fixture
def sample_owner():
      owner = Owner(name="Test Owner")
      dog = Pet(name="Rex", species="Dog")
      cat = Pet(name="Luna", species="Cat")
      owner.add_pet(dog)
      owner.add_pet(cat)
      return owner, dog, cat


def test_mark_complete_changes_status():
      task = Task("Morning Walk", time="07:00", frequency="once")
      assert task.completed is False
      task.mark_complete()
      assert task.completed is True


def test_adding_task_increases_pet_task_count():
      pet = Pet(name="Buddy", species="Dog")
      assert len(pet.tasks) == 0
      pet.add_task(Task("Walk", time="08:00", frequency="daily"))
      assert len(pet.tasks) == 1


def test_daily_task_recurrence():
      today = date.today()
      task = Task("Feeding", time="08:00", frequency="daily", due_date=today)
      new_task = task.mark_complete()
      assert new_task is not None
      assert new_task.due_date == today + timedelta(days=1)
      assert new_task.completed is False


def test_weekly_task_recurrence():
      today = date.today()
      task = Task("Bath", time="10:00", frequency="weekly", due_date=today)
      new_task = task.mark_complete()
      assert new_task is not None
      assert new_task.due_date == today + timedelta(weeks=1)


def test_once_task_no_recurrence():
      task = Task("Vet Visit", time="14:00", frequency="once")
      new_task = task.mark_complete()
      assert new_task is None


def test_sort_by_time(sample_owner):
      owner, dog, cat = sample_owner
      dog.add_task(Task("Evening Walk", time="18:00", frequency="daily"))
      dog.add_task(Task("Morning Walk", time="07:00", frequency="daily"))
      cat.add_task(Task("Breakfast", time="07:30", frequency="daily"))
      scheduler = Scheduler(owner)
      sorted_tasks = scheduler.sort_by_time()
      times = [task.time for _, task in sorted_tasks]
      assert times == sorted(times)


def test_filter_by_pet(sample_owner):
      owner, dog, cat = sample_owner
      dog.add_task(Task("Walk", time="07:00", frequency="daily"))
      cat.add_task(Task("Playtime", time="15:00", frequency="daily"))
      scheduler = Scheduler(owner)
      rex_tasks = scheduler.filter_tasks(pet_name="Rex")
      assert all(name == "Rex" for name, _ in rex_tasks)
      assert len(rex_tasks) == 1


def test_filter_by_status(sample_owner):
      owner, dog, _ = sample_owner
      t1 = Task("Walk", time="07:00", frequency="once")
      t2 = Task("Bath", time="10:00", frequency="once")
      t1.completed = True
      dog.add_task(t1)
      dog.add_task(t2)
      scheduler = Scheduler(owner)
      pending = scheduler.filter_tasks(completed=False)
      assert all(not t.completed for _, t in pending)


def test_conflict_detection(sample_owner):
      owner, dog, cat = sample_owner
      today = date.today()
      dog.add_task(Task("Walk", time="08:00", frequency="once", due_date=today))
      cat.add_task(Task("Breakfast", time="08:00", frequency="once", due_date=today))
      scheduler = Scheduler(owner)
      conflicts = scheduler.detect_conflicts()
      assert len(conflicts) == 1


def test_no_false_conflicts(sample_owner):
      owner, dog, cat = sample_owner
      today = date.today()
      dog.add_task(Task("Walk", time="07:00", frequency="once", due_date=today))
      cat.add_task(Task("Breakfast", time="08:00", frequency="once", due_date=today))
      scheduler = Scheduler(owner)
      conflicts = scheduler.detect_conflicts()
      assert len(conflicts) == 0


def test_pet_with_no_tasks(sample_owner):
      _, dog, _ = sample_owner
      assert dog.get_pending_tasks() == []
  
