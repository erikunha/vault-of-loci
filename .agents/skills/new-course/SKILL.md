---
name: new-course
description: Create a new course in this vault (course note, lessons folder, project folder, map). Use when the user starts a course, class or discipline. Writes files, so only run when asked.
---

1. Ask for the course name, its order and the block or semester only if missing. Name the folder `10_Courses/<NN>_<Course_Name>/` with underscores instead of spaces.
2. Create `<Course_Name>.md` from `90_System/Templates/Course.md` with `type: course`, `order`, `status: active`, `period`.
3. Create `lessons/` and `project/`. Lessons go in `lessons/lesson-NN-<slug>.md` from `90_System/Templates/Lesson.md`.
4. Add the course to `00_Home.md` under "Courses".
5. Run the `run-checks` skill and report each check as passed, failed or not run.
6. Add one line to `90_System/Agent_Log/YYYY-MM.md`.
