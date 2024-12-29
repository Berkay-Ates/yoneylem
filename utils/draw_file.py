from weasyprint import HTML, CSS
import tempfile
import os


def generate_schedule_pdf(solution_data, output_path="schedule.pdf"):
    """
    Generates a PDF schedule with grades as columns and days/times as rows.
    """
    css_content = """
        @page {
            size: A4 portrait;
            margin: 1cm;
        }
        
        body {
            font-family: Arial, sans-serif;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 8pt;
        }
        
        th, td {
            border: 1px solid black;
            padding: 1px;
            text-align: center;
            vertical-align: top;
            height: 12px;
        }
        
        td:empty {
            height: 8px;
            padding: 0;
        }
        
        .time-cell {
            width: 40px;
            background-color: #f0f0f0;
            font-size: 7pt;
            height: 12px;
            padding: 1px;
        }
        
        .grade-header {
            background-color: #e0e0e0;
            font-weight: bold;
            font-size: 9pt;
            height: 15px;
        }
        
        .course-cell {
            min-height: 15px;
            padding: 2px;
        }
        
        .face-to-face {
            background-color: #90EE90;
        }
        
        .online {
            background-color: #ADD8E6;
        }
        
        .hybrid {
            background-color: #FFB6C1;
        }
        
        .course-code {
            font-weight: bold;
            color: red;
            margin-bottom: 1px;
            font-size: 8pt;
        }
        
        .course-instructor {
            font-style: italic;
            font-size: 7pt;
        }
        
        .course-details {
            font-size: 7pt;
        }
        
        .title {
            text-align: center;
            font-size: 11pt;
            font-weight: bold;
            margin: 8px 0;
            background-color: yellow;
            padding: 3px;
        }
    """

    # Constants
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    grades = [1, 2, 3, 4]
    times = list(range(8, 21))  # 8:00 to 20:00

    # Create schedule grid
    schedule_grid = {day: {grade: {time: None for time in times} for grade in grades} for day in days}

    # Populate schedule grid
    for lesson in solution_data:
        day = lesson["day"]
        grade = lesson["grade"]
        start_time = lesson["start_time"]
        for t in range(start_time, start_time + lesson["duration"]):
            schedule_grid[day][grade][t] = lesson

    # Generate HTML
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        <div class="title">YTÜ Bilgisayar Mühendisliği Bölümü Ders Programı</div>
        <table>
            <tr>
                <th class="time-cell"></th>
    """

    # Add grade headers
    for grade in grades:
        html_content += f'<th class="grade-header">{grade}. Grade</th>'
    html_content += "</tr>"

    # Generate rows for each day and time
    for day in days:
        first_row_of_day = True
        for time in times:
            row_html = "<tr>"

            # Add time cell with day name if it's first row of the day
            if first_row_of_day:
                row_html += f'<td class="time-cell">{day}<br/>{time:02d}:00</td>'
                first_row_of_day = False
            else:
                row_html += f'<td class="time-cell">{time:02d}:00</td>'

            # Add cells for each grade
            for grade in grades:
                lesson = schedule_grid[day][grade][time]

                if lesson is None:
                    row_html += "<td></td>"
                elif time == lesson["start_time"]:
                    # Only create cell content at the start time
                    course_type_class = f"course-cell {lesson['type'].lower().replace(' ', '-')}"
                    row_html += f"""
                        <td rowspan="{lesson['duration']}" class="{course_type_class}">
                            <div class="course-code">{lesson['name']} ({lesson['duration']} hour)</div>
                            <div class="course-instructor">{lesson['instructor']}</div>
                            <div class="course-details">
                                ({lesson['type']})
                                {f"<br>{lesson['classroom']}" if lesson['classroom'] else ""}
                            </div>
                        </td>
                    """
                # Skip cell if it's covered by a rowspan from above

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
        # Generate PDF
        HTML(html_path).write_pdf(output_path, stylesheets=[CSS(filename=css_path)])
    finally:
        # Clean up temporary files
        os.unlink(html_path)
        os.unlink(css_path)


def format_solver_solution(solver_output):
    """
    Convert solver output to the format needed by generate_schedule_pdf.

    Args:
        solver_output: List of strings containing the solver's output in the format:
        "Lesson: Math101 (Grade 1) - Instructor: AEL"
        "Day: Monday, Time: 8:00 - 11:00"
        "Type: FaceToFace, Classroom: Room101"

    Returns:
        List of dictionaries in the format needed by generate_schedule_pdf
    """
    formatted_data = []
    current_lesson = {}

    for line in solver_output:
        if line.startswith("Lesson:"):
            if current_lesson:
                formatted_data.append(current_lesson)
            current_lesson = {}
            # Parse lesson line
            lesson_parts = line.split(" - ")
            lesson_info = lesson_parts[0].replace("Lesson: ", "")
            name, grade = lesson_info.split(" (Grade ")
            current_lesson["name"] = name.strip()
            current_lesson["grade"] = int(grade.replace(")", ""))
            current_lesson["instructor"] = lesson_parts[1].replace("Instructor: ", "").strip()

        elif line.startswith("Day:"):
            # Parse day and time
            day_time = line.split(", ")
            current_lesson["day"] = day_time[0].replace("Day: ", "").strip()
            time_range = day_time[1].replace("Time: ", "").split(" - ")
            current_lesson["start_time"] = int(time_range[0].replace(":00", ""))
            current_lesson["duration"] = int(time_range[1].replace(":00", "")) - current_lesson["start_time"]

        elif line.startswith("Type:"):
            # Parse type and classroom
            type_info = line.split(", ")
            current_lesson["type"] = type_info[0].replace("Type: ", "").strip()
            if len(type_info) > 1:
                current_lesson["classroom"] = type_info[1].replace("Classroom: ", "").strip()
            else:
                current_lesson["classroom"] = None

    # Add the last lesson
    if current_lesson:
        formatted_data.append(current_lesson)

    return formatted_data
