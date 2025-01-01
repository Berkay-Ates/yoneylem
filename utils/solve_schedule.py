from ortools.linear_solver import pywraplp


def get_instructor_by_name(instructors, name):
    for instructor in instructors:
        if instructor["name"] == name:
            return instructor
    return None


def solve_schedule(data):
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        return

    instructors = data["instructors"]
    lessons = data["lessons"]
    classrooms = data["classrooms"]

    # Remove instructors with empty lesson lists
    instructors = [instructor for instructor in instructors if instructor["lessons"]]

    # Remove duplicate lessons with same group numbers
    unique_lessons = {}
    for lesson in lessons:
        key = (lesson["name"], lesson["grade"], lesson["group"])
        if key not in unique_lessons:
            unique_lessons[key] = lesson
    lessons = list(unique_lessons.values())

    time_slots = list(range(8, 17))  # 8:00 AM to 5:00 PM
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    grades = [1, 2, 3, 4]
    lunch_start = 12
    lunch_end = 13

    # Print debug information
    print(f"Total number of lessons: {len(lessons)}")
    print(f"Total number of instructors: {len(instructors)}")
    print(f"Total number of classrooms: {len(classrooms)}")
    print(f"Time slots: {time_slots}")
    print(
        "Available time slots per day:",
        len(
            [
                t
                for t in time_slots
                if not (t < lunch_start and t + 3 > lunch_start) and not (t >= lunch_start and t < lunch_end)
            ]
        ),
    )
    print("\nStarting solver...\n")

    # Decision variables
    x = {}
    for lesson in lessons:
        for instructor in lesson["instructors"]:
            instructor_data = get_instructor_by_name(instructors, instructor)
            if not instructor_data:
                print(f"Warning: Instructor {instructor} not found in instructors list")
                continue

            # Only create variables for instructor's preferred days
            instructor_days = instructor_data["preferred_days"]
            for day in instructor_days:
                # Only create variables for valid start times that don't overlap with lunch
                for time in range(8, 17 - lesson["duration"] + 1):
                    # Skip if lesson would overlap with lunch break
                    if time < lunch_start and time + lesson["duration"] > lunch_start:
                        continue
                    if time >= lunch_start and time < lunch_end:
                        continue

                    if lesson["type"] in ["FaceToFace", "Hybrid"]:
                        for classroom in classrooms:
                            x[(lesson["name"], lesson["group"], instructor, classroom, day, time)] = solver.BoolVar(
                                f'x_{lesson["name"]}_{lesson["group"]}_{instructor}_{classroom}_{day}_{time}'
                            )
                    else:  # Online classes
                        x[(lesson["name"], lesson["group"], instructor, None, day, time)] = solver.BoolVar(
                            f'x_{lesson["name"]}_{lesson["group"]}_{instructor}_None_{day}_{time}'
                        )

    print(f"Number of variables created: {len(x)}")

    # Constraint 1: Each lesson-group combination must be scheduled exactly once
    for lesson in lessons:
        constraint_expr = []
        for instructor in lesson["instructors"]:
            instructor_data = get_instructor_by_name(instructors, instructor)
            if not instructor_data:
                continue

            instructor_days = instructor_data["preferred_days"]
            for day in instructor_days:
                for time in range(8, 17 - lesson["duration"] + 1):
                    if time < lunch_start and time + lesson["duration"] > lunch_start:
                        continue
                    if time >= lunch_start and time < lunch_end:
                        continue

                    if lesson["type"] in ["FaceToFace", "Hybrid"]:
                        for classroom in classrooms:
                            if (lesson["name"], lesson["group"], instructor, classroom, day, time) in x:
                                constraint_expr.append(
                                    x[(lesson["name"], lesson["group"], instructor, classroom, day, time)]
                                )
                    else:
                        if (lesson["name"], lesson["group"], instructor, None, day, time) in x:
                            constraint_expr.append(x[(lesson["name"], lesson["group"], instructor, None, day, time)])

        if constraint_expr:
            solver.Add(sum(constraint_expr) == 1)

    # Constraint 2: Instructor cannot teach overlapping classes
    for instructor in instructors:
        for day in days_of_week:
            for time in time_slots:
                constraint_expr = []
                for lesson in lessons:
                    if instructor["name"] in lesson["instructors"]:
                        # Check all possible start times that would overlap with current time slot
                        for start_time in range(
                            max(8, time - lesson["duration"] + 1), min(time + 1, 17 - lesson["duration"] + 1)
                        ):
                            if start_time < lunch_start and start_time + lesson["duration"] > lunch_start:
                                continue
                            if start_time >= lunch_start and start_time < lunch_end:
                                continue

                            if lesson["type"] in ["FaceToFace", "Hybrid"]:
                                for classroom in classrooms:
                                    if (
                                        lesson["name"],
                                        lesson["group"],
                                        instructor["name"],
                                        classroom,
                                        day,
                                        start_time,
                                    ) in x:
                                        constraint_expr.append(
                                            x[
                                                (
                                                    lesson["name"],
                                                    lesson["group"],
                                                    instructor["name"],
                                                    classroom,
                                                    day,
                                                    start_time,
                                                )
                                            ]
                                        )
                            else:
                                if (lesson["name"], lesson["group"], instructor["name"], None, day, start_time) in x:
                                    constraint_expr.append(
                                        x[(lesson["name"], lesson["group"], instructor["name"], None, day, start_time)]
                                    )
                if constraint_expr:
                    solver.Add(sum(constraint_expr) <= 1)

    # Constraint 3: Classroom cannot have overlapping classes
    for classroom in classrooms:
        for day in days_of_week:
            for time in time_slots:
                constraint_expr = []
                for lesson in lessons:
                    if lesson["type"] in ["FaceToFace", "Hybrid"]:
                        for start_time in range(
                            max(8, time - lesson["duration"] + 1), min(time + 1, 17 - lesson["duration"] + 1)
                        ):
                            if start_time < lunch_start and start_time + lesson["duration"] > lunch_start:
                                continue
                            if start_time >= lunch_start and start_time < lunch_end:
                                continue

                            for instructor in lesson["instructors"]:
                                if (lesson["name"], lesson["group"], instructor, classroom, day, start_time) in x:
                                    constraint_expr.append(
                                        x[(lesson["name"], lesson["group"], instructor, classroom, day, start_time)]
                                    )
                if constraint_expr:
                    solver.Add(sum(constraint_expr) <= 1)

    # Constraint 4: No overlapping mandatory classes (whether different or same lessons)
    # The only exception is different groups of the same lesson can overlap
    for grade in grades:
        for day in days_of_week:
            for time in time_slots:
                # Get all lessons for this grade
                grade_lessons = [lesson for lesson in lessons if lesson["grade"] == grade]

                # Create constraint for all lessons in the same grade
                for lesson1 in grade_lessons:
                    # Check all possible start times that would overlap with current time slot
                    for start_time in range(
                        max(8, time - lesson1["duration"] + 1), min(time + 1, 17 - lesson1["duration"] + 1)
                    ):
                        if start_time < lunch_start and start_time + lesson1["duration"] > lunch_start:
                            continue
                        if start_time >= lunch_start and time < lunch_end:
                            continue

                        # Get all variables for this lesson at this time
                        lesson1_expr = []
                        for instructor in lesson1["instructors"]:
                            if lesson1["type"] in ["FaceToFace", "Hybrid"]:
                                for classroom in classrooms:
                                    if (
                                        lesson1["name"],
                                        lesson1["group"],
                                        instructor,
                                        classroom,
                                        day,
                                        start_time,
                                    ) in x:
                                        lesson1_expr.append(
                                            x[
                                                (
                                                    lesson1["name"],
                                                    lesson1["group"],
                                                    instructor,
                                                    classroom,
                                                    day,
                                                    start_time,
                                                )
                                            ]
                                        )
                            else:  # Online classes
                                if (lesson1["name"], lesson1["group"], instructor, None, day, start_time) in x:
                                    lesson1_expr.append(
                                        x[(lesson1["name"], lesson1["group"], instructor, None, day, start_time)]
                                    )

                        # For each other lesson in the same grade that's not a different group of the same lesson
                        for lesson2 in grade_lessons:
                            if (
                                lesson1["name"] != lesson2["name"]
                            ):  # Skip if they're the same lesson (different groups allowed to overlap)
                                # If either lesson is mandatory, or they have different obligations, they can't overlap
                                if lesson1["obligation"] == "mandatory" or lesson2["obligation"] == "mandatory":
                                    for start_time2 in range(
                                        max(8, time - lesson2["duration"] + 1),
                                        min(time + 1, 17 - lesson2["duration"] + 1),
                                    ):
                                        if (
                                            start_time2 < lunch_start
                                            and start_time2 + lesson2["duration"] > lunch_start
                                        ):
                                            continue
                                        if start_time2 >= lunch_start and start_time2 < lunch_end:
                                            continue

                                        lesson2_expr = []
                                        for instructor in lesson2["instructors"]:
                                            if lesson2["type"] in ["FaceToFace", "Hybrid"]:
                                                for classroom in classrooms:
                                                    if (
                                                        lesson2["name"],
                                                        lesson2["group"],
                                                        instructor,
                                                        classroom,
                                                        day,
                                                        start_time2,
                                                    ) in x:
                                                        lesson2_expr.append(
                                                            x[
                                                                (
                                                                    lesson2["name"],
                                                                    lesson2["group"],
                                                                    instructor,
                                                                    classroom,
                                                                    day,
                                                                    start_time2,
                                                                )
                                                            ]
                                                        )
                                            else:  # Online classes
                                                if (
                                                    lesson2["name"],
                                                    lesson2["group"],
                                                    instructor,
                                                    None,
                                                    day,
                                                    start_time2,
                                                ) in x:
                                                    lesson2_expr.append(
                                                        x[
                                                            (
                                                                lesson2["name"],
                                                                lesson2["group"],
                                                                instructor,
                                                                None,
                                                                day,
                                                                start_time2,
                                                            )
                                                        ]
                                                    )

                                        # If both lessons have variables at these times, add constraint
                                        if lesson1_expr and lesson2_expr:
                                            solver.Add(sum(lesson1_expr) + sum(lesson2_expr) <= 1)

    # Constraint 5: Different groups of same lesson can overlap in time but need different classrooms
    for lesson_name in set(lesson["name"] for lesson in lessons):
        lesson_groups = [lesson for lesson in lessons if lesson["name"] == lesson_name]
        if len(lesson_groups) > 1 and lesson_groups[0]["type"] in ["FaceToFace", "Hybrid"]:
            for day in days_of_week:
                for time in time_slots:
                    for classroom in classrooms:
                        constraint_expr = []
                        for lesson in lesson_groups:
                            for instructor in lesson["instructors"]:
                                if (lesson["name"], lesson["group"], instructor, classroom, day, time) in x:
                                    constraint_expr.append(
                                        x[(lesson["name"], lesson["group"], instructor, classroom, day, time)]
                                    )
                        if constraint_expr:
                            # Same classroom can't be used by different groups at same time
                            # But different groups can overlap if using different classrooms
                            solver.Add(sum(constraint_expr) <= 1)

    # Constraint 6: Each instructor can only teach one group of a lesson
    for lesson_name in set(lesson["name"] for lesson in lessons):
        lesson_groups = [lesson for lesson in lessons if lesson["name"] == lesson_name]
        if len(lesson_groups) > 1:  # If the lesson has multiple groups
            # For each instructor that can teach this lesson
            for instructor in set(instr for lesson in lesson_groups for instr in lesson["instructors"]):
                instructor_group_vars = []
                for lesson in lesson_groups:
                    # Collect all variables for this instructor across all days and times
                    for day in days_of_week:
                        for time in range(8, 17 - lesson["duration"] + 1):
                            if time < lunch_start and time + lesson["duration"] > lunch_start:
                                continue
                            if time >= lunch_start and time < lunch_end:
                                continue

                            if lesson["type"] in ["FaceToFace", "Hybrid"]:
                                for classroom in classrooms:
                                    if (lesson["name"], lesson["group"], instructor, classroom, day, time) in x:
                                        instructor_group_vars.append(
                                            x[(lesson["name"], lesson["group"], instructor, classroom, day, time)]
                                        )
                            else:  # Online classes
                                if (lesson["name"], lesson["group"], instructor, None, day, time) in x:
                                    instructor_group_vars.append(
                                        x[(lesson["name"], lesson["group"], instructor, None, day, time)]
                                    )

                if instructor_group_vars:
                    solver.Add(sum(instructor_group_vars) <= 1)  # Instructor can only teach one group

    # Solve
    solver.SetTimeLimit(300000)  # 5 minutes time limit
    status = solver.Solve()

    return_text = ""

    # Print results
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("\nSolution found:\n")
        return_text += "Solution found:\n\n"
        for lesson in lessons:
            for instructor in lesson["instructors"]:
                for day in days_of_week:
                    for time in range(8, 17 - lesson["duration"] + 1):
                        if time < lunch_start and time + lesson["duration"] > lunch_start:
                            continue
                        if time >= lunch_start and time < lunch_end:
                            continue

                        if lesson["type"] in ["FaceToFace", "Hybrid"]:
                            for classroom in classrooms:
                                if (lesson["name"], lesson["group"], instructor, classroom, day, time) in x:
                                    if (
                                        x[
                                            (lesson["name"], lesson["group"], instructor, classroom, day, time)
                                        ].solution_value()
                                        == 1
                                    ):
                                        print(
                                            f"Lesson: {lesson['name']} (Grade {lesson['grade']}, Group {lesson['group']}) - Instructor: {instructor}"
                                        )
                                        return_text += f"Lesson: {lesson['name']} (Grade {lesson['grade']}, Group {lesson['group']}) - Instructor: {instructor}\n"
                                        print(f"Day: {day}, Time: {time}:00 - {time + lesson['duration']}:00")
                                        return_text += f"Day: {day}, Time: {time}:00 - {time + lesson['duration']}:00\n"
                                        print(f"Type: {lesson['type']}, Classroom: {classroom}")
                                        return_text += f"Type: {lesson['type']}, Classroom: {classroom}\n"
                                        print(f"Obligation: {lesson['obligation']}\n")
                                        return_text += f"Obligation: {lesson['obligation']}\n\n"
                        else:
                            if (lesson["name"], lesson["group"], instructor, None, day, time) in x:
                                if (
                                    x[(lesson["name"], lesson["group"], instructor, None, day, time)].solution_value()
                                    == 1
                                ):
                                    print(
                                        f"Lesson: {lesson['name']} (Grade {lesson['grade']}, Group {lesson['group']}) - Instructor: {instructor}"
                                    )
                                    return_text += f"Lesson: {lesson['name']} (Grade {lesson['grade']}, Group {lesson['group']}) - Instructor: {instructor}\n"
                                    print(f"Day: {day}, Time: {time}:00 - {time + lesson['duration']}:00")
                                    return_text += f"Day: {day}, Time: {time}:00 - {time + lesson['duration']}:00\n"
                                    print(f"Type: {lesson['type']} (No classroom needed)")
                                    return_text += f"Type: {lesson['type']} (No classroom needed)\n"
                                    print(f"Obligation: {lesson['obligation']}\n")
                                    return_text += f"Obligation: {lesson['obligation']}\n\n"
        return return_text
    else:
        print("No solution found within the time limit.")
        return None
