from ortools.linear_solver import pywraplp


data = {
    "instructors": [
        {"name": "AEL", "lessons": ["Math101"], "preferred_days": ["Tuesday", "Wednesday", "Thursday", "Friday"]},
        {
            "name": "BANUDIRI",
            "lessons": ["Math101", "Chemistry301"],
            "preferred_days": ["Tuesday", "Wednesday", "Friday"],
        },
        {
            "name": "JaneSmith",
            "lessons": ["Biology101", "Philosophy101"],
            "preferred_days": ["Tuesday", "Thursday", "Friday"],
        },
        {
            "name": "JohnDoe",
            "lessons": ["Physics201", "Philosophy101"],
            "preferred_days": ["Tuesday", "Thursday", "Friday"],
        },
        {
            "name": "AliceJohnson",
            "lessons": ["English101", "History201"],
            "preferred_days": ["Monday", "Tuesday", "Thursday"],
        },
        {
            "name": "RobertBrown",
            "lessons": ["Philosophy101", "Math102"],
            "preferred_days": ["Monday", "Wednesday", "Friday"],
        },
        {
            "name": "EmmaThomas",
            "lessons": ["Spanish101", "French101"],
            "preferred_days": ["Monday", "Wednesday", "Friday"],
        },
        {
            "name": "MichaelChen",
            "lessons": ["ComputerScience101", "Math103"],
            "preferred_days": ["Tuesday", "Thursday"],
        },
        {
            "name": "SarahPatel",
            "lessons": ["Art101", "History202"],
            "preferred_days": ["Monday", "Wednesday", "Friday"],
        },
        {
            "name": "DavidKim",
            "lessons": ["Music101", "Drama101"],
            "preferred_days": ["Tuesday", "Thursday", "Friday"],
        },
        {"name": "LauraWilson", "lessons": ["Chemistry301"], "preferred_days": ["Tuesday"]},
    ],
    "lessons": [
        {"name": "Math101", "instructors": ["AEL", "BANUDIRI"], "grade": 1, "type": "FaceToFace", "duration": 3},
        {"name": "Biology101", "instructors": ["JaneSmith"], "grade": 2, "type": "Online", "duration": 3},
        {"name": "English101", "instructors": ["AliceJohnson"], "grade": 4, "type": "FaceToFace", "duration": 2},
        {"name": "Physics201", "instructors": ["JohnDoe"], "grade": 2, "type": "FaceToFace", "duration": 3},
        {
            "name": "Philosophy101",
            "instructors": ["RobertBrown", "JohnDoe", "JaneSmith"],
            "grade": 1,
            "type": "FaceToFace",
            "duration": 1,
        },
        {"name": "History201", "instructors": ["AliceJohnson"], "grade": 2, "type": "Hybrid", "duration": 2},
        {"name": "Math102", "instructors": ["RobertBrown"], "grade": 1, "type": "FaceToFace", "duration": 3},
        {
            "name": "Chemistry301",
            "instructors": ["LauraWilson", "BANUDIRI"],
            "grade": 3,
            "type": "Online",
            "duration": 3,
        },
        {
            "name": "Spanish101",
            "instructors": ["EmmaThomas"],
            "grade": 2,
            "type": "FaceToFace",
            "duration": 2,
        },
        {
            "name": "French101",
            "instructors": ["EmmaThomas"],
            "grade": 3,
            "type": "Hybrid",
            "duration": 2,
        },
        {
            "name": "ComputerScience101",
            "instructors": ["MichaelChen"],
            "grade": 4,
            "type": "FaceToFace",
            "duration": 2,
        },
        {
            "name": "Math103",
            "instructors": ["MichaelChen"],
            "grade": 3,
            "type": "Online",
            "duration": 2,
        },
        {
            "name": "Art101",
            "instructors": ["SarahPatel"],
            "grade": 1,
            "type": "FaceToFace",
            "duration": 2,
        },
        {
            "name": "History202",
            "instructors": ["SarahPatel"],
            "grade": 4,
            "type": "Hybrid",
            "duration": 2,
        },
        {
            "name": "Music101",
            "instructors": ["DavidKim"],
            "grade": 1,
            "type": "FaceToFace",
            "duration": 1,
        },
        {
            "name": "Drama101",
            "instructors": ["DavidKim"],
            "grade": 2,
            "type": "FaceToFace",
            "duration": 2,
        },
    ],
    "classrooms": [
        "MusicRoom301",
        "ArtStudio302",
        "LanguageLab303",
        "ComputerLab304",
        "Room101",
        "Lab202",
        "Room103",
        "Lab204",
        "Room205",
        "Lab206",
        "Room207",
        "Lab208",
    ],
}


def get_instructor_by_name(instructors, name):
    for instructor in instructors:
        if instructor["name"] == name:
            return instructor
    return None


def solve_schedule(data):
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        return

    # Input data
    instructors = data["instructors"]
    lessons = data["lessons"]
    classrooms = data["classrooms"]

    time_slots = list(range(8, 17))  # 8:00 AM to 4:00 PM
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    grades = [1, 2, 3, 4]

    # Decision variables - only for start times
    x = {}
    for lesson in lessons:
        for instructor in lesson["instructors"]:
            instructor_days = get_instructor_by_name(instructors, instructor)["preferred_days"]
            for day in instructor_days:
                # Only create variables for valid start times
                for time in range(8, 17 - lesson["duration"]):
                    if lesson["type"] in ["FaceToFace", "Hybrid"]:
                        for classroom in classrooms:
                            x[(lesson["name"], instructor, classroom, day, time)] = solver.BoolVar(
                                f'x_{lesson["name"]}_{instructor}_{classroom}_{day}_{time}'
                            )
                    else:  # Online classes don't need classrooms
                        x[(lesson["name"], instructor, None, day, time)] = solver.BoolVar(
                            f'x_{lesson["name"]}_{instructor}_None_{day}_{time}'
                        )

    # Constraint 1: Each lesson must be scheduled exactly once
    for lesson in lessons:
        constraint_expr = []
        for instructor in lesson["instructors"]:
            instructor_days = get_instructor_by_name(instructors, instructor)["preferred_days"]
            for day in instructor_days:
                for time in range(8, 17 - lesson["duration"]):
                    if lesson["type"] in ["FaceToFace", "Hybrid"]:
                        for classroom in classrooms:
                            if (lesson["name"], instructor, classroom, day, time) in x:
                                constraint_expr.append(x[(lesson["name"], instructor, classroom, day, time)])
                    else:
                        if (lesson["name"], instructor, None, day, time) in x:
                            constraint_expr.append(x[(lesson["name"], instructor, None, day, time)])
        solver.Add(sum(constraint_expr) == 1)

    # Constraint 2: No instructor can teach during overlapping time slots
    for instructor in instructors:
        for day in days_of_week:
            for time in time_slots:
                constraint_expr = []
                for lesson in lessons:
                    if instructor["name"] in lesson["instructors"]:
                        # Check all possible start times that would overlap with current time slot
                        for start_time in range(
                            max(8, time - lesson["duration"] + 1), min(time + 1, 17 - lesson["duration"])
                        ):
                            if lesson["type"] in ["FaceToFace", "Hybrid"]:
                                for classroom in classrooms:
                                    if (lesson["name"], instructor["name"], classroom, day, start_time) in x:
                                        constraint_expr.append(
                                            x[(lesson["name"], instructor["name"], classroom, day, start_time)]
                                        )
                            else:
                                if (lesson["name"], instructor["name"], None, day, start_time) in x:
                                    constraint_expr.append(
                                        x[(lesson["name"], instructor["name"], None, day, start_time)]
                                    )
                if constraint_expr:
                    solver.Add(sum(constraint_expr) <= 1)

    # Constraint 3: No classroom can have overlapping classes
    for classroom in classrooms:
        for day in days_of_week:
            for time in time_slots:
                constraint_expr = []
                for lesson in lessons:
                    if lesson["type"] in ["FaceToFace", "Hybrid"]:
                        # Check all possible start times that would overlap with current time slot
                        for start_time in range(
                            max(8, time - lesson["duration"] + 1), min(time + 1, 17 - lesson["duration"])
                        ):
                            for instructor in lesson["instructors"]:
                                if (lesson["name"], instructor, classroom, day, start_time) in x:
                                    constraint_expr.append(x[(lesson["name"], instructor, classroom, day, start_time)])
                if constraint_expr:
                    solver.Add(sum(constraint_expr) <= 1)

    # Constraint 4: No overlapping classes for the same grade level
    for grade in grades:
        for day in days_of_week:
            for time in time_slots:
                constraint_expr = []
                grade_lessons = [lesson for lesson in lessons if lesson["grade"] == grade]
                for lesson in grade_lessons:
                    # Check all possible start times that would overlap with current time slot
                    for start_time in range(
                        max(8, time - lesson["duration"] + 1), min(time + 1, 17 - lesson["duration"])
                    ):
                        for instructor in lesson["instructors"]:
                            if lesson["type"] in ["FaceToFace", "Hybrid"]:
                                for classroom in classrooms:
                                    if (lesson["name"], instructor, classroom, day, start_time) in x:
                                        constraint_expr.append(
                                            x[(lesson["name"], instructor, classroom, day, start_time)]
                                        )
                            else:
                                if (lesson["name"], instructor, None, day, start_time) in x:
                                    constraint_expr.append(x[(lesson["name"], instructor, None, day, start_time)])
                if constraint_expr:
                    solver.Add(sum(constraint_expr) <= 1)

    # Solve
    status = solver.Solve()

    # Print results
    if status == pywraplp.Solver.OPTIMAL:
        print("\nOptimal schedule found:\n")
        for lesson in lessons:
            for instructor in lesson["instructors"]:
                for day in days_of_week:
                    for time in range(8, 17 - lesson["duration"]):
                        if lesson["type"] in ["FaceToFace", "Hybrid"]:
                            for classroom in classrooms:
                                if (lesson["name"], instructor, classroom, day, time) in x:
                                    if x[(lesson["name"], instructor, classroom, day, time)].solution_value() == 1:
                                        print(
                                            f"Lesson: {lesson['name']} (Grade {lesson['grade']}) - Instructor: {instructor}"
                                        )
                                        print(f"Day: {day}, Time: {time}:00 - {time + lesson['duration']}:00")
                                        print(f"Type: {lesson['type']}, Classroom: {classroom}\n")
                        else:
                            if (lesson["name"], instructor, None, day, time) in x:
                                if x[(lesson["name"], instructor, None, day, time)].solution_value() == 1:
                                    print(
                                        f"Lesson: {lesson['name']} (Grade {lesson['grade']}) - Instructor: {instructor}"
                                    )
                                    print(f"Day: {day}, Time: {time}:00 - {time + lesson['duration']}:00")
                                    print(f"Type: {lesson['type']} (No classroom needed)\n")
    else:
        print("No optimal solution found.")


if __name__ == "__main__":
    solve_schedule()
