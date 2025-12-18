# app.py
# Interactive lesson plan template with PDF export, duration, standards, and differentiation
# Run with: python app.py

from flask import Flask, render_template_string, request, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER
import io

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Interactive Lesson Plan</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f6f8;
            margin: 0;
            padding: 0;
        }
        header {
            background: #1f2933;
            color: white;
            padding: 1.5rem;
            text-align: center;
        }
        main {
            max-width: 900px;
            margin: 2rem auto;
            background: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        h2 { border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; }
        label { display: block; margin-top: 1rem; font-weight: bold; }
        input, textarea, select {
            width: 100%; padding: 0.6rem; margin-top: 0.4rem;
            border-radius: 4px; border: 1px solid #cbd5e1;
        }
        textarea { min-height: 90px; }
        button {
            margin-top: 1.5rem; padding: 0.8rem 1.2rem;
            background: #2563eb; color: white; border: none;
            border-radius: 6px; cursor: pointer; font-size: 1rem;
        }
        button.secondary { background: #475569; }
        button:hover { opacity: 0.9; }
        .output {
            margin-top: 2rem; padding: 1.5rem;
            background: #f8fafc; border-left: 5px solid #2563eb;
        }
        @media print {
            header, form, .secondary { display: none; }
            body { background: white; }
            main { box-shadow: none; margin: 0; }
        }
    </style>
</head>
<body>
<header>
    <h1>Interactive Lesson Plan Builder</h1>
    <p>Create, preview, and export lesson plans</p>
</header>

<main>
<form method="POST">
    <h2>Lesson Details</h2>

    <label>Lesson Title</label>
    <input type="text" name="title" required>

    <label>Grade Level</label>
    <select name="grade">
        <option>Choose Grade Level</option>
        <option>Kindergarten</option>
        <option>Grade 1</option>
        <option>Grade 2</option>
        <option>Grade 3</option>
        <option>Grade 4</option>
        <option>Grade 5</option>
        <option>Grade 6</option>
        <option>Grade 7</option>
        <option>Grade 8</option>
        <option>Grade 9</option>
        <option>Grade 10</option>
        <option>Grade 11/option>
        <option>Grade 12/option>
    </select>

    <label>Duration (minutes)</label>
    <input type="number" name="duration">

    <label>Learning Objective</label>
    <textarea name="objective"></textarea>

    <label>Standards (ex: NGSS, Common Core)</label>
    <textarea name="standards"></textarea>

    <label>Materials Needed</label>
    <textarea name="materials"></textarea>

    <label>Warm-Up Activity</label>
    <textarea name="warmup"></textarea>

    <label>Main Activity</label>
    <textarea name="activity"></textarea>

    <label>Differentiation / Accommodations</label>
    <textarea name="differentiation"></textarea>

    <label>Assessment</label>
    <textarea name="assessment"></textarea>

    <button type="submit">Generate Lesson Plan</button>
</form>

{% if lesson %}
<div class="output">
    <h2>{{ lesson.title }}</h2>
    <p><strong>Grade:</strong> {{ lesson.grade }} | <strong>Duration:</strong> {{ lesson.duration }} min</p>

    <h3>Objective</h3><p>{{ lesson.objective }}</p>
    <h3>Standards</h3><p>{{ lesson.standards }}</p>
    <h3>Materials</h3><p>{{ lesson.materials }}</p>
    <h3>Warm-Up</h3><p>{{ lesson.warmup }}</p>
    <h3>Main Activity</h3><p>{{ lesson.activity }}</p>
    <h3>Differentiation</h3><p>{{ lesson.differentiation }}</p>
    <h3>Assessment</h3><p>{{ lesson.assessment }}</p>

    <form method="POST" action="/export">
        {% for key, value in lesson.items() %}
        <input type="hidden" name="{{ key }}" value="{{ value }}">
        {% endfor %}
        <button class="secondary">Export to PDF</button>
    </form>
</div>
{% endif %}
</main>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    lesson = None
    if request.method == 'POST':
        lesson = dict(request.form)
    return render_template_string(TEMPLATE, lesson=lesson)

@app.route('/export', methods=['POST'])
def export_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=LETTER)
    styles = getSampleStyleSheet()
    content = []

    for key, value in request.form.items():
        title = key.replace('_', ' ').title()
        content.append(Paragraph(f"<b>{title}</b>: {value}", styles['Normal']))
        content.append(Spacer(1, 12))

    doc.build(content)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="lesson_plan.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
