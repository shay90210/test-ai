from flask import Flask, render_template_string, request

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
        h2 {
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 0.5rem;
        }
        label {
            display: block;
            margin-top: 1rem;
            font-weight: bold;
        }
        input, textarea, select {
            width: 100%;
            padding: 0.6rem;
            margin-top: 0.4rem;
            border-radius: 4px;
            border: 1px solid #cbd5e1;
        }
        textarea {
            min-height: 100px;
        }
        button {
            margin-top: 1.5rem;
            padding: 0.8rem 1.2rem;
            background: #2563eb;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 1rem;
        }
        button:hover {
            background: #1e40af;
        }
        .output {
            margin-top: 2rem;
            padding: 1.5rem;
            background: #f1f5f9;
            border-left: 5px solid #2563eb;
        }
        .tag {
            display: inline-block;
            background: #e0e7ff;
            color: #1e3a8a;
            padding: 0.3rem 0.6rem;
            border-radius: 999px;
            margin-right: 0.5rem;
            font-size: 0.85rem;
        }
    </style>
</head>
<body>
    <header>
        <h1>Interactive Lesson Plan Builder</h1>
        <p>Create and preview a structured lesson plan</p>
    </header>

    <main>
        <form method="POST">
            <h2>Lesson Details</h2>

            <label>Lesson Title</label>
            <input type="text" name="title" required>

            <label>Grade Level</label>
            <select name="grade">
                <option>K–2</option>
                <option>3–5</option>
                <option>6–8</option>
                <option>9–12</option>
            </select>

            <label>Learning Objective</label>
            <textarea name="objective"></textarea>

            <label>Materials Needed</label>
            <textarea name="materials"></textarea>

            <label>Warm-Up Activity</label>
            <textarea name="warmup"></textarea>

            <label>Main Activity</label>
            <textarea name="activity"></textarea>

            <label>Assessment</label>
            <textarea name="assessment"></textarea>

            <button type="submit">Generate Lesson Plan</button>
        </form>

        {% if lesson %}
        <div class="output">
            <h2>{{ lesson.title }}</h2>
            <span class="tag">Grade: {{ lesson.grade }}</span>

            <h3>Objective</h3>
            <p>{{ lesson.objective }}</p>

            <h3>Materials</h3>
            <p>{{ lesson.materials }}</p>

            <h3>Warm-Up</h3>
            <p>{{ lesson.warmup }}</p>

            <h3>Main Activity</h3>
            <p>{{ lesson.activity }}</p>

            <h3>Assessment</h3>
            <p>{{ lesson.assessment }}</p>
        </div>
        {% endif %}
    </main>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
        if request.method == 'POST':
            lesson = {
                'title': request.form['title'],
                'grade': request.form['grade'],
                'objective': request.form['objective'],
                'materials': request.form['materials'],
                'warmup': request.form['warmup'],
                'activity': request.form['activity'],
                'assessment': request.form['assessment']
            }
        return render_template_string(TEMPLATE, lesson=lesson)

if __name__ == '__main__':
    app.run(debug=True)
