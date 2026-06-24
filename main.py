"""main.py - CLI demo for PawPal+."""
from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

def main():
      owner = Owner(name="Alex")
      buddy = Pet(name="Buddy", species="Dog")
      whiskers = Pet(name="Whiskers", species="Cat")
      buddy.add_task(Task("Evening Walk", time="18:00", frequency="daily", due_date=date.today()))
      buddy.add_task(Task("Morning Walk", time="07:30", frequency="daily", due_date=date.today()))
      buddy.add_task(Task("Flea Medicine", time="09:00", frequency="weekly", due_date=date.today()))
      whiskers.add_task(Task("Breakfast", time="07:30", frequency="daily", due_date=date.today()))
      whiskers.add_task(Task("Vet Checkup", time="14:00", frequency="once", due_date=date.today()))
      whiskers.add_task(Task("Playtime", time="17:00", frequency="daily", due_date=date.today()))
      owner.add_pet(buddy)
      owner.add_pet(whiskers)
      scheduler = Scheduler(owner)
      print("=" * 50)
      print(f"TODAY'S SCHEDULE for {owner.name}")
      print("=" * 50)
      for pet_name, task in scheduler.sort_by_time():
                print(f"  {pet_name:12} | {task}")
            print("\nCONFLICT CHECK")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
              for (n1, t1), (n2, t2) in conflicts:
                            print(f"  CONFLICT at {t1.time}: {n1} vs {n2}")
    else:
        print("  No conflicts found.")
          scheduler.mark_task_complete(buddy, buddy.tasks[1])
    print("\nAfter completing Morning Walk:")
    for task in buddy.tasks:
              print(f"  {task}")

if __name__ == "__main__":
      main()
