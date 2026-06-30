"""
app.py
PawPal+ Streamlit UI - connected to pawpal_system.py backend.
"""

import streamlit as st
from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

# ── Session state init ──────────────────────────────────────────────────────
if "owner" not in st.session_state:
        st.session_state.owner = Owner(name="Alex")
    if "scheduler" not in st.session_state:
            st.session_state.scheduler = Scheduler(st.session_state.owner)

# ── Sidebar: Owner & Pet setup ──────────────────────────────────────────────
with st.sidebar:
        st.header("🐾 PawPal+")
        st.subheader("Owner Info")
        owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
        if owner_name != st.session_state.owner.name:
                    st.session_state.owner.name = owner_name

        st.subheader("Add a Pet")
        new_pet_name = st.text_input("Pet name", key="new_pet_name")
        new_pet_species = st.selectbox("Species", ["Dog", "Cat", "Rabbit", "Bird", "Other"], key="new_pet_species")
        if st.button("➕ Add Pet"):
                    if new_pet_name.strip():
                                    existing = [p.name.lower() for p in st.session_state.owner.pets]
                                    if new_pet_name.strip().lower() not in existing:
                                                        st.session_state.owner.add_pet(Pet(name=new_pet_name.strip(), species=new_pet_species))
                                                        st.success(f"Added {new_pet_name}!")
                    else:
                                        st.warning("A pet with that name already exists.")
        else:
                        st.warning("Please enter a pet name.")

        if st.session_state.owner.pets:
                    st.subheader("Your Pets")
                    for pet in st.session_state.owner.pets:
                                    st.write(f"🐾 **{pet.name}** ({pet.species}) — {len(pet.tasks)} task(s)")

            # ── Main area ───────────────────────────────────────────────────────────────
            st.title(f"🐾 PawPal+ — {st.session_state.owner.name}'s Dashboard")

if not st.session_state.owner.pets:
        st.info("👈 Use the sidebar to add your owner name and at least one pet to get started.")
    st.stop()

tabs = st.tabs(["📋 Tasks", "🗓️ Today's Schedule", "⚠️ Conflicts", "✅ Complete a Task", "🔍 Filter Tasks"])

# ── Tab 1: Add Tasks ────────────────────────────────────────────────────────
with tabs[0]:
        st.header("Add a Task")
    pet_names = [p.name for p in st.session_state.owner.pets]
    selected_pet_name = st.selectbox("Assign to pet", pet_names, key="task_pet")
    task_desc = st.text_input("Task description", value="Morning walk", key="task_desc")
    task_time = st.time_input("Scheduled time", key="task_time")
    task_freq = st.selectbox("Frequency", ["once", "daily", "weekly"], key="task_freq")
    task_due = st.date_input("Due date", value=date.today(), key="task_due")

    if st.button("➕ Add Task"):
                if task_desc.strip():
                                pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet_name)
                                new_task = Task(
                                    description=task_desc.strip(),
                                    time=task_time.strftime("%H:%M"),
                                    frequency=task_freq,
                due_date=task_due,
                                )
                                pet.add_task(new_task)
                                st.success(f"Task '{task_desc}' added for {selected_pet_name}!")
    else:
            st.warning("Please enter a task description.")

    st.divider()
    st.subheader("All Current Tasks")
    all_tasks = st.session_state.scheduler.get_all_tasks()
    if all_tasks:
                rows = []
                for pet_name, task in all_tasks:
                                rows.append({
                                                    "Pet": pet_name,
                                                    "Task": task.description,
                                                    "Time": task.time,
                                                    "Frequency": task.frequency,
                                                    "Due Date": str(task.due_date),
                                                    "Status": "✅ Done" if task.completed else "⏳ Pending",
                                })
                            st.table(rows)
else:
        st.info("No tasks yet. Add one above!")

# ── Tab 2: Today's Schedule ─────────────────────────────────────────────────
with tabs[1]:
        st.header("🗓️ Today's Schedule")
    st.caption("All tasks sorted chronologically by scheduled time.")
    sorted_tasks = st.session_state.scheduler.sort_by_time()
    today_tasks = [(n, t) for n, t in sorted_tasks if t.due_date == date.today()]

    if today_tasks:
                for pet_name, task in today_tasks:
                                status_icon = "✅" if task.completed else "⏳"
                                st.markdown(
                                    f"**{task.time}** — {status_icon} **{task.description}** "
                                    f"*(for {pet_name}, {task.frequency})*"
                                )
elif sorted_tasks:
        st.info("No tasks scheduled for today. Here are all upcoming tasks:")
        for pet_name, task in sorted_tasks:
                        status_icon = "✅" if task.completed else "⏳"
                        st.markdown(
                            f"**{task.time}** ({task.due_date}) — {status_icon} **{task.description}** "
                            f"*(for {pet_name}, {task.frequency})*"
                        )
else:
        st.info("No tasks scheduled yet. Add tasks in the Tasks tab.")

# ── Tab 3: Conflicts ────────────────────────────────────────────────────────
with tabs[2]:
        st.header("⚠️ Conflict Detection")
    st.caption("Tasks scheduled at the same time on the same date for different pets.")
    conflicts = st.session_state.scheduler.detect_conflicts()
    if conflicts:
                st.error(f"Found {len(conflicts)} conflict(s)!")
        for (n1, t1), (n2, t2) in conflicts:
                        st.warning(
                                            f"🕐 **{t1.time}** on {t1.due_date}: "
                                            f"**{n1}** ({t1.description}) conflicts with **{n2}** ({t2.description})"
                        )
else:
        st.success("✅ No scheduling conflicts found!")

# ── Tab 4: Complete a Task ──────────────────────────────────────────────────
with tabs[3]:
        st.header("✅ Mark a Task Complete")
    pending = st.session_state.scheduler.filter_tasks(completed=False)
    if pending:
                options = {
                    f"{pet_name} — {task.description} @ {task.time} ({task.due_date})": (pet_name, task)
                    for pet_name, task in pending
    }
        selected_label = st.selectbox("Select task to complete", list(options.keys()))
        if st.button("✅ Mark Complete"):
                        pet_name, task = options[selected_label]
                        pet = next(p for p in st.session_state.owner.pets if p.name == pet_name)
                        st.session_state.scheduler.mark_task_complete(pet, task)
                        next_due = task.due_date + timedelta(days=1) if task.frequency == "daily" else (
                            task.due_date + timedelta(weeks=1) if task.frequency == "weekly" else None
                        )
                        if next_due:
                                            st.success(f"✅ '{task.description}' marked complete! Next scheduled: {next_due}")
        else:
                st.success(f"✅ '{task.description}' marked complete!")
else:
        st.success("🎉 All tasks are complete!")

# ── Tab 5: Filter Tasks ─────────────────────────────────────────────────────
with tabs[4]:
        st.header("🔍 Filter Tasks")
    col1, col2 = st.columns(2)
    with col1:
                pet_names_filter = ["All"] + [p.name for p in st.session_state.owner.pets]
        filter_pet = st.selectbox("Filter by pet", pet_names_filter)
    with col2:
                filter_status = st.selectbox("Filter by status", ["All", "Pending", "Completed"])

    pet_arg = None if filter_pet == "All" else filter_pet
    status_arg = None if filter_status == "All" else (filter_status == "Completed")

    filtered = st.session_state.scheduler.filter_tasks(pet_name=pet_arg, completed=status_arg)
    if filtered:
                rows = []
        for pet_name, task in filtered:
                        rows.append({
                                            "Pet": pet_name,
                                            "Task": task.description,
                                            "Time": task.time,
                                            "Frequency": task.frequency,
                                            "Due Date": str(task.due_date),
                                            "Status": "✅ Done" if task.completed else "⏳ Pending",
                        })
                    st.table(rows)
else:
        st.info("No tasks match the selected filters.")
