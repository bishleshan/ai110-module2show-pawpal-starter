"""
pawpal_system.py
Core logic layer for PawPal+ - a smart pet care management system.
"""

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional


@dataclass
class Task:
      """Represents a single pet care activity."""
      description: str
      time: str
      frequency: str
      due_date: date = field(default_factory=date.today)
      completed: bool = False

    def mark_complete(self):
              """Mark this task as complete and reschedule if recurring."""
              self.completed = True
              if self.frequency == "daily":
                            return Task(
                                              description=self.description,
                                              time=self.time,
                                              frequency=self.frequency,
                                              due_date=self.due_date + timedelta(days=1),
                                              completed=False,
                            )
elif self.frequency == "weekly":
            return Task(
                              description=self.description,
                              time=self.time,
                              frequency=self.frequency,
                              due_date=self.due_date + timedelta(weeks=1),
                              completed=False,
            )
        return None

    def __repr__(self):
              """Return a readable string representation of the task."""
              status = "done" if self.completed else "pending"
              return f"[{self.time}] {self.description} ({self.frequency}) - due {self.due_date} [{status}]"


@dataclass
class Pet:
      """Stores pet details and its list of tasks."""
      name: str
      species: str
      tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
              """Add a task to this pet's task list."""
              self.tasks.append(task)

    def remove_task(self, task: Task):
              """Remove a task from this pet's task list."""
              if task in self.tasks:
                            self.tasks.remove(task)

          def get_pending_tasks(self):
                    """Return only incomplete tasks for this pet."""
                    return [t for t in self.tasks if not t.completed]

    def __repr__(self):
              """Return a readable string for this pet."""
              return f"{self.name} ({self.species}) - {len(self.tasks)} task(s)"


@dataclass
class Owner:
      """Manages multiple pets and provides access to all their tasks."""
      name: str
      pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet):
              """Add a pet to the owner's pet list."""
              self.pets.append(pet)

    def remove_pet(self, pet: Pet):
              """Remove a pet from the owner's pet list."""
              if pet in self.pets:
                            self.pets.remove(pet)

          def get_all_tasks(self):
                    """Return all tasks across all pets as (pet_name, task) tuples."""
                    result = []
                    for pet in self.pets:
                                  for task in pet.tasks:
                                                    result.append((pet.name, task))
                                            return result

    def __repr__(self):
              """Return a readable string for this owner."""
              return f"{self.name} - {len(self.pets)} pet(s)"


class Scheduler:
      """The brain of PawPal+: retrieves, organizes, and manages tasks."""

    def __init__(self, owner: Owner):
              """Initialize the scheduler with an owner."""
              self.owner = owner

    def get_all_tasks(self):
              """Return all (pet_name, task) tuples from the owner."""
              return self.owner.get_all_tasks()

    def sort_by_time(self):
              """Return all tasks sorted chronologically by time."""
              return sorted(self.get_all_tasks(), key=lambda pair: pair[1].time)

    def filter_tasks(self, pet_name=None, completed=None):
              """Filter tasks by pet name and/or completion status."""
              results = self.get_all_tasks()
              if pet_name is not None:
                            results = [(n, t) for n, t in results if n.lower() == pet_name.lower()]
                        if completed is not None:
                                      results = [(n, t) for n, t in results if t.completed == completed]
                                  return results

    def detect_conflicts(self):
              """Detect tasks scheduled at the same time on the same due date."""
        seen = {}
        conflicts = []
        for pet_name, task in self.get_all_tasks():
                      key = (task.time, task.due_date)
                      if key in seen:
                                        conflicts.append((seen[key], (pet_name, task)))
else:
                seen[key] = (pet_name, task)
          return conflicts

    def mark_task_complete(self, pet, task):
              """Mark a task complete; auto-reschedule if recurring."""
        new_task = task.mark_complete()
        if new_task:
                      pet.add_task(new_task)
          
