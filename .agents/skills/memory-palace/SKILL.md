---
name: memory-palace
description: Build a memory palace for an ordered list the learner wants to remember, with the learner picking the places, one item at each place, then walk the route and record each place in the learning ledger; use it when the learner wants to remember a sequence, a checklist or ordered steps, and it writes a note, so run it only when asked.
disable-model-invocation: true
---

Tutor mode: the learner attempts first and without notes. The agent never writes the learner's
notes or answers. Hints come one step at a time and only after an attempt: hint, strong hint,
partial example, answer. Confidence from 1 to 5 is asked before the reveal. The agent never
grades an attempt the learner did not confirm.

The palace helps with ordered material and does not replace understanding. The evidence behind it
is weaker than the evidence behind retrieval practice.

1. Find the list the learner means. When they say "this checklist" or name none, look in the track's
   `practice/` and `sessions/` notes for an ordered list (a checklist, ordered steps) and name it in one
   line; ask only when none is there. It must be ordered material: a sequence, a checklist, ordered steps.
2. Build the route with the learner. In the same reply as step 1, ask for the places. The learner picks the places, because only the learner knows
   the route. The agent asks for places that are familiar and easy to picture, one place per item,
   in walking order. The agent does not choose the places.
3. Put one item at each place. Ask the learner for the items and write them down. An item is one
   thing, short enough to say in one breath.
4. Write the palace note at `50_Review/Palaces/<Name>.md`, copied from
   `90_System/Templates/Memory_Palace.md`. Fill the table with one row per place, in walking
   order: Place, Item and Source. The Source column points to the note the item came from. The
   name of the note gives the ids: the objective is `palace-<name>` and a place is the item
   `palace-<name>-<place number>`. The name is the file name of the note, lowercased, with the
   underscores turned into hyphens: `Home_Route.md` gives `palace-home-route` and
   `palace-home-route-1` for the first place.
5. Read the route back with the script. It prints the places in order and leaves the item blank,
   because the item is what the learner has to recall.

```bash
python3 -I 90_System/Scripts/palace_test.py --palace 50_Review/Palaces/<Name>.md --places 5
```

6. Walk the route with the learner. The agent says one place at a time, in walking order, and the
   learner says the item for that place, without notes. The agent asks only for the item of the
   place it just said. It never reads the item out and never shows the table.
7. After the learner has answered a place, run the script again with `--with-items` to see the item
   of that place and check the answer against it.

```bash
python3 -I 90_System/Scripts/palace_test.py --palace 50_Review/Palaces/<Name>.md --with-items
```

8. When the answer is wrong, or the learner asks to try again, use the hint ladder one step at a
   time: hint, strong hint, partial example, answer. Never skip a step.
9. Ask for confidence from 1 to 5 before the reveal. Then reveal the item of that place and grade
   the learner's words against the note.
10. Record each place on its own, after the learner confirms the result. Use the objective and the
   item id of that place. If the learner took a hint, pass `--assistance` and `--hints`: an
   attempt with help stays out of the rate.

```bash
python3 -I 90_System/Scripts/record_attempt.py --objective palace-<name> \
  --item palace-<name>-<n> --mode recall \
  [--correct|--incorrect] --confidence <1-5> [--hints <n>] [--assistance <level>] \
  --allow-unknown-objective
```

The flag `--allow-unknown-objective` is needed because a palace objective is not in
`90_System/Objectives.json`. Add the objective to the registry first when the learner wants the
palace to show up in the retention report by name.

11. Show the learner the lines that were written. Never edit or delete a line of the ledger.
