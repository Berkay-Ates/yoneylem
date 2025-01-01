from weasyprint import HTML, CSS
import tempfile
import os


def generate_schedule_pdf(solution_data, output_path="schedule.pdf"):
    css_content = """
        @page {
            size: A3 portrait;
            margin: 0.5cm;
        }
        
        body { 
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }
        
        .schedule-title {
            text-align: center;
            margin: 5px 0 10px 0;
            padding: 5px;
            background-color: #FFFF00;
            border: 1px solid #808000;
        }
        
        .university {
            font-size: 16pt;
            font-weight: bold;
            margin-bottom: 2px;
        }
        
        .department {
            font-size: 14pt;
            font-weight: bold;
            margin-bottom: 2px;
        }
        
        .subtitle {
            font-size: 12pt;
            font-weight: bold;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 8pt;
            table-layout: fixed;
        }
        
        th, td {
            border: 1px solid black;
            padding: 1px;
            text-align: center;
            vertical-align: top;
            height: 18px;
            overflow: hidden;
        }
        
        td:empty {
            height: 8px !important;
            padding: 0;
            border-top: 1px dotted #ccc;
            border-bottom: 1px dotted #ccc;
        }
        
        .time-cell {
            width: 60px;
            background-color: #f0f0f0;
            font-size: 6pt;
            padding: 1px;
            white-space: nowrap;
            text-align: center;
        }
        
        .time-range {
            margin-top: 1px;
            font-weight: normal;
            color: #333;
            text-align: center;
            padding: 1px 0;
        }
        
        .day-monday { background-color: #FFE4E1; }
        .day-tuesday { background-color: #E0FFFF; }
        .day-wednesday { background-color: #E6E6FA; }
        .day-thursday { background-color: #F0FFF0; }
        .day-friday { background-color: #FFF0F5; }
        
        .grade-header {
            background-color: #4a4a4a;
            color: white;
            font-weight: bold;
            font-size: 9pt;
            height: 25px;
            padding: 2px;
        }
        
        .course-cell { 
            min-height: 18px; 
            padding: 1px;
            margin: 0;
            position: relative;
        }
        
        .face-to-face { 
            background-color: #98FB98;
            border-left: 3px solid #228B22;
        }
        .online { 
            background-color: #B3E0FF;
            border-left: 3px solid #0066CC;
        }
        .hybrid { 
            background-color: #FFA07A;
            border-left: 3px solid #FF4500;
        }
        
        .course-code {
            font-weight: bold;
            font-size: 7pt;
            padding: 1px;
            margin: 0;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            text-align: center;
            background: rgba(255,255,255,0.4);
            border-radius: 2px;
        }

        .course-code.mandatory {
            color: #800000;  /* Dark red for mandatory courses */
        }

        .course-code.elective {
            color: #006400;  /* Dark green for elective courses */
        }
        
        .course-info {
            font-size: 7pt;
            color: #444;
            text-align: center;
            padding: 1px;
            margin: 1px 0;
            background: rgba(255,255,255,0.5);
            border-radius: 2px;
            font-weight: bold;
        }
        
        .groups-container {
            display: flex;
            flex-direction: row;
            gap: 1px;
            margin-top: 1px;
            background: rgba(255,255,255,0.2);
            padding: 1px;
            border-radius: 2px;
        }
        
        .group-info {
            flex: 1;
            font-size: 6pt;
            padding: 1px;
            background: rgba(255,255,255,0.3);
            border-radius: 2px;
            border-left: 1px dotted rgba(0,0,0,0.2);
        }
        
        .group-info:first-child {
            border-left: none;
        }
        
        .group-header {
            font-weight: bold;
            color: #444;
            border-bottom: 1px dotted #999;
            margin-bottom: 2px;
            font-size: 6pt;
            text-align: center;
            background: rgba(255,255,255,0.4);
            border-radius: 2px;
            padding: 2px;
        }
        
        .course-instructor {
            font-style: italic;
            font-size: 6pt;
            margin: 1px 0;
            line-height: 1.2;
            text-align: center;
        }
        
        .course-details { 
            font-size: 6pt;
            color: #444;
            line-height: 1.2;
            text-align: center;
            margin-top: 2px;
        }
        
        .electives-container {
            display: flex;
            flex-direction: column;
            gap: 1px;
            margin-top: 1px;
            border-top: 2px dashed #666;
            padding-top: 1px;
        }
        
        .elective-course {
            width: 100%;
            background: rgba(255,255,255,0.2);
            border-radius: 2px;
            padding: 1px;
            position: relative;
        }
        
        .elective-course:not(:last-child) {
            border-bottom: 1px dashed #666;
            padding-bottom: 1px;
            margin-bottom: 1px;
        }
        
        .day-label {
            font-weight: bold;
            display: block;
            margin-bottom: 0;
            color: #444;
            border-bottom: 1px solid #999;
            padding-bottom: 0;
            background-color: rgba(0,0,0,0.1);
            font-size: 6pt;
            line-height: 1.1;
        }
    """

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    grades = [1, 2, 3, 4]
    times = list(range(8, 18))

    # Create schedule grid with support for multiple groups
    schedule_grid = {day: {grade: {time: [] for time in times} for grade in grades} for day in days}

    # Populate schedule grid
    for lesson in solution_data:
        day = lesson["day"]
        grade = lesson["grade"]
        start_time = lesson["start_time"]
        duration = lesson["duration"]

        # Add lesson only to the start time slot
        schedule_grid[day][grade][start_time].append(lesson)

    # Generate HTML
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        <div class="schedule-title">
            <div class="university">Yıldız Technical University</div>
            <div class="department">Department of Computer Engineering</div>
            <div class="subtitle">Course Schedule</div>
        </div>
        <table>
            <tr>
                <th class="time-cell"></th>
    """

    for grade in grades:
        html_content += f'<th class="grade-header">{grade}. Grade</th>'
    html_content += "</tr>"

    def generate_lesson_cell_content(lessons):
        if not lessons:
            return ""

        # First, separate mandatory and elective courses
        mandatory_courses = {}
        elective_courses = {}

        for lesson in lessons:
            course_name = lesson["name"]
            course_data = {
                "lessons": [],
                "duration": lesson["duration"],
                "type": lesson["type"],
                "is_elective": lesson.get("is_elective", False),
            }

            if lesson.get("is_elective", False):
                if course_name not in elective_courses:
                    elective_courses[course_name] = course_data
                elective_courses[course_name]["lessons"].append(lesson)
            else:
                if course_name not in mandatory_courses:
                    mandatory_courses[course_name] = course_data
                mandatory_courses[course_name]["lessons"].append(lesson)

        content = ""

        # Handle mandatory courses
        for course_name, course_data in mandatory_courses.items():
            type_class = course_data["type"].lower().replace(" ", "-")
            content += f'<div class="course-cell {type_class}">'
            content += f'<div class="course-code mandatory">{course_name} ({course_data["duration"]} hours)</div>'
            content += f'<div class="course-info">Mandatory - {course_data["type"]}</div>'

            # Groups container
            content += '<div class="groups-container">'
            for lesson in sorted(course_data["lessons"], key=lambda x: x.get("group", 1)):
                content += f"""
                    <div class="group-info">
                        <div class="group-header">Group {lesson.get("group", 1)}</div>
                        <div class="course-instructor">{lesson["instructor"]}</div>
                        {f'<div class="course-details">{lesson["classroom"]}</div>' if lesson.get("classroom") and lesson["type"] != "Online" else ""}
                    </div>
                """
            content += "</div></div>"

        # Handle elective courses
        if elective_courses:
            content += '<div class="electives-container">'
            for course_name, course_data in elective_courses.items():
                type_class = course_data["type"].lower().replace(" ", "-")
                content += f'<div class="elective-course {type_class}">'
                content += f'<div class="course-code elective">{course_name} ({course_data["duration"]} hours)</div>'
                content += f'<div class="course-info">Elective - {course_data["type"]}</div>'

                # Groups container for this elective course
                content += '<div class="groups-container">'
                for lesson in sorted(course_data["lessons"], key=lambda x: x.get("group", 1)):
                    content += f"""
                        <div class="group-info">
                            <div class="group-header">Group {lesson.get("group", 1)}</div>
                            <div class="course-instructor">{lesson["instructor"]}</div>
                            {f'<div class="course-details">{lesson["classroom"]}</div>' if lesson.get("classroom") and lesson["type"] != "Online" else ""}
                        </div>
                    """
                content += "</div></div>"
            content += "</div>"

        return content

    # Generate rows for each day and time
    current_day = None
    for day in days:
        for time in times:
            row_html = "<tr>"

            # Generate time cell with proper formatting
            time_cell_content = f"{time:02d}:00 - {(time+1):02d}:00"

            if current_day != day:
                row_html += f"""<td class="time-cell day-{day.lower()}">
                    <span class="day-label">{day}</span>
                    <div class="time-range">{time_cell_content}</div></td>"""
                current_day = day
            else:
                row_html += f'<td class="time-cell day-{day.lower()}">{time_cell_content}</td>'

            # Add cells for each grade
            for grade in grades:
                lessons_at_time = schedule_grid[day][grade][time]
                cell_added = False

                # Check if this time slot is part of a previous lesson's duration
                is_continuation = False
                for prev_time in range(max(8, time - 5), time):
                    prev_lessons = schedule_grid[day][grade][prev_time]
                    for prev_lesson in prev_lessons:
                        if prev_time + prev_lesson["duration"] > time:
                            is_continuation = True
                            break
                    if is_continuation:
                        break

                if not is_continuation:
                    if not lessons_at_time:
                        row_html += "<td></td>"
                    else:
                        # Calculate rowspan based on the maximum duration of lessons starting at this time
                        max_duration = max(lesson["duration"] for lesson in lessons_at_time)
                        row_html += f'<td rowspan="{max_duration}" class="course-cell {lessons_at_time[0]["type"].lower().replace(" ", "-")}">'
                        row_html += generate_lesson_cell_content(lessons_at_time)
                        row_html += "</td>"
                    cell_added = True

            row_html += "</tr>"
            html_content += row_html

    html_content += """
        </table>
    </body>
    </html>
    """

    # Create temporary files for HTML and CSS
    with tempfile.NamedTemporaryFile(suffix=".html", mode="w", encoding="utf-8", delete=False) as html_file:
        html_file.write(html_content)
        html_path = html_file.name

    with tempfile.NamedTemporaryFile(suffix=".css", mode="w", encoding="utf-8", delete=False) as css_file:
        css_file.write(css_content)
        css_path = css_file.name

    try:
        HTML(html_path).write_pdf(output_path, stylesheets=[CSS(filename=css_path)])
    finally:
        os.unlink(html_path)
        os.unlink(css_path)


def format_solver_solution(solver_output):
    """
    Convert solver output to the format needed by generate_schedule_pdf.
    """
    formatted_data = []
    current_lesson = {}

    # Clean and split the output into lines
    lines = [line.strip() for line in solver_output.strip().splitlines() if line.strip()]

    for line in lines:
        if line.startswith("Lesson:"):
            if current_lesson:
                formatted_data.append(current_lesson)
            current_lesson = {}
            # Parse lesson line with group information
            lesson_parts = line.split(" - ")
            lesson_info = lesson_parts[0].replace("Lesson: ", "")
            name_grade_group = lesson_info.split(" (Grade ")
            name = name_grade_group[0].strip()
            grade_group = name_grade_group[1].replace(")", "").split(", Group ")
            current_lesson["name"] = name
            current_lesson["grade"] = int(grade_group[0])
            current_lesson["group"] = int(grade_group[1]) if len(grade_group) > 1 else 1
            current_lesson["instructor"] = lesson_parts[1].replace("Instructor: ", "").strip()

        elif line.startswith("Day:"):
            day_time = line.split(", ")
            current_lesson["day"] = day_time[0].replace("Day: ", "").strip()
            time_range = day_time[1].replace("Time: ", "").split(" - ")
            current_lesson["start_time"] = int(time_range[0].split(":")[0])
            current_lesson["duration"] = int(time_range[1].split(":")[0]) - current_lesson["start_time"]

        elif line.startswith("Type:"):
            type_info = line.split(", ")
            current_lesson["type"] = type_info[0].replace("Type: ", "").split(" ")[0].strip()
            if len(type_info) > 1:
                current_lesson["classroom"] = type_info[1].replace("Classroom: ", "").strip()

        elif line.startswith("Obligation:"):
            obligation = line.replace("Obligation:", "").strip()
            current_lesson["is_elective"] = obligation.lower() != "mandatory"

    # Append the last lesson if it exists
    if current_lesson:
        formatted_data.append(current_lesson)

    return formatted_data
