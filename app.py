from flask import Flask, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DB_NAME = "vskill.db"

COURSES = [
    ("Python Programming", "Learn Python from basics to practical programming.", "4 Months", "4.9"),
    ("Data Analytics", "Learn Excel, SQL, Python and data visualization.", "5 Months", "4.8"),
    ("Web Development", "Build modern websites with HTML, CSS, JavaScript and Flask.", "6 Months", "4.9"),
    ("SQL & Database", "Master SQL, database design and queries.", "3 Months", "4.8"),
    ("Java Programming", "Learn Java programming and object-oriented development.", "5 Months", "4.7"),
    ("Advanced Excel", "Master advanced Excel, formulas, dashboards and reports.", "2 Months", "4.8"),
    ("Digital Marketing", "Learn SEO, social media, ads and digital strategy.", "3 Months", "4.7"),
    ("AI & Machine Learning", "Explore Python, AI concepts and machine learning.", "6 Months", "4.9"),
]

IMAGES = [
    "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1556761175-b413da4baf72?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1555949963-aa79dcee981c?auto=format&fit=crop&w=900&q=80",
]

STYLE = """
<style>
*{box-sizing:border-box}
body{margin:0;font-family:Arial,sans-serif;background:#f6f8fb;color:#172033}
nav{background:#111827;color:white;padding:18px 7%;display:flex;align-items:center;justify-content:space-between}
.logo{font-size:25px;font-weight:800}
nav a{color:white;text-decoration:none;margin-left:22px}
.hero{padding:75px 7%;background:linear-gradient(135deg,#111827,#2563eb);color:white}
.hero-inner{max-width:1150px;margin:auto}
.badge{display:inline-block;background:#ffffff22;padding:8px 14px;border-radius:20px}
h1{font-size:52px;line-height:1.05;margin:20px 0}
.container{max-width:1150px;margin:40px auto;padding:0 20px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:22px}
.card{background:white;border-radius:16px;overflow:hidden;box-shadow:0 8px 30px #00000012}
.card img{width:100%;height:160px;object-fit:cover}
.card-body{padding:20px}
.btn{display:inline-block;background:#2563eb;color:white;padding:12px 18px;border-radius:9px;text-decoration:none;border:0;cursor:pointer}
.form-box{max-width:600px;margin:50px auto;background:white;padding:30px;border-radius:16px;box-shadow:0 8px 30px #00000012}
input,select{width:100%;padding:13px;margin:8px 0 16px;border:1px solid #d1d5db;border-radius:8px}
.notice{background:#fff7ed;border:1px solid #fdba74;padding:14px;border-radius:10px;margin:20px 0}
.certificate{max-width:100%;border-radius:10px;box-shadow:0 8px 30px #0002}
footer{margin-top:60px;background:#111827;color:white;text-align:center;padding:30px}
</style>
"""

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            course TEXT NOT NULL,
            certificate_id TEXT UNIQUE NOT NULL,
            marks INTEGER NOT NULL,
            grade TEXT NOT NULL,
            result TEXT NOT NULL,
            result_date TEXT NOT NULL
        )
    """)
    existing = conn.execute(
        "SELECT id FROM results WHERE certificate_id = ?",
        ("VS2609260117",)
    ).fetchone()

    if not existing:
        conn.execute("""
            INSERT INTO results
            (student_name, course, certificate_id, marks, grade, result, result_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            "Demo Student",
            "Data Analytics",
            "VS2609260117",
            75,
            "A",
            "PASS",
            "26 September 2026"
        ))

    conn.commit()
    conn.close()

def nav():
    return """
<nav>
<div class="logo">VSkill</div>
<div>
<a href="/">Home</a>
<a href="/courses">Courses</a>
<a href="/results">Results</a>
<a href="/about">About</a>
<a href="/contact">Contact</a>
<a href="/admin">Admin</a>
</div>
</nav>
"""

def footer():
    return """
<footer>
<p>VSkill Demo Platform</p>

<p>Not an official credential verification service.</p>
</footer>
"""

def page(title, body):
    return "<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>" + title + "</title>" + STYLE + "</head><body>" + nav() + body + footer() + "</body></html>"

@app.route("/")
def home():
    cards = ""
    for i, course in enumerate(COURSES):
        cards += """
        <div class="card">
            <img src="{img}">
            <div class="card-body">
                <h3>{name}</h3>
                <p>{desc}</p>
                <p><b>{duration}</b> · ⭐ {rating}</p>
            </div>
        </div>
        """.format(
            img=IMAGES[i],
            name=course[0],
            desc=course[1],
            duration=course[2],
            rating=course[3]
        )

    body = """
<section class="hero">
<div class="hero-inner">

<h1>Learn Skills.<br>Build Your Future.</h1>
<p>Explore practical courses and build career-ready skills.</p>
<a class="btn" href="/courses">Explore Courses</a>
</div>
</section>

<div class="container">
<div class="notice">

It is not an official VSkill credential verification service.
</div>

<h2>Popular Courses</h2>
<div class="grid">""" + cards + """</div>

<h2>Certificate</h2>
<p></p>
<a class="btn" href="/results">Check Result</a>
</div>
"""
    return page("VSkill - Learn Skills That Matter", body)

@app.route("/courses")
def courses():
    cards = ""
    for i, course in enumerate(COURSES):
        cards += """
        <div class="card">
            <img src="{img}">
            <div class="card-body">
                <h3>{name}</h3>
                <p>{desc}</p>
                <p><b>Duration:</b> {duration}</p>
                <p><b>Rating:</b> ⭐ {rating}</p>
            </div>
        </div>
        """.format(
            img=IMAGES[i],
            name=course[0],
            desc=course[1],
            duration=course[2],
            rating=course[3]
        )

    return page("Courses - VSkill", '<div class="container"><h1>Courses</h1><div class="grid">' + cards + '</div></div>')

@app.route("/results", methods=["GET", "POST"])
def results():
    result = None
    message = ""

    if request.method == "POST":
        certificate_id = request.form.get("certificate_id", "").strip()
        conn = get_db()
        result = conn.execute(
            "SELECT * FROM results WHERE certificate_id = ?",
            (certificate_id,)
        ).fetchone()
        conn.close()

        if not result:
            message = "No result found for this ID."

    body = """
<div class="container">
<div class="form-box">
<h1>Certificate Result</h1>
<form method="POST">
<label>Certificate ID</label>
<input name="certificate_id" placeholder="Enter certificate ID" required>
<button class="btn" type="submit">Check Result</button>
</form>
"""

    if message:
        body += "<p>" + message + "</p>"

    if result:
        certificate_path = os.path.join(app.static_folder, "certificate.png")
        if os.path.exists(certificate_path):
            body += """
            <hr>
            <h2>Certificate Preview</h2>
            <img class="certificate" src="/static/certificate.png" alt="Certificate preview">
            <br><br>
            <a class="btn" href="/static/certificate.png" download="VSkill-Certificate.png">Download Certificate</a>
            """

    body += "</div></div>"
    return page("Results - VSkill", body)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    message = ""

    if request.method == "POST":
        student_name = request.form.get("student_name", "").strip()
        course = request.form.get("course", "").strip()
        certificate_id = request.form.get("certificate_id", "").strip()
        marks = request.form.get("marks", "").strip()
        grade = request.form.get("grade", "").strip()
        result_value = request.form.get("result", "").strip()
        result_date = request.form.get("result_date", "").strip()

        try:
            conn = get_db()
            conn.execute("""
                INSERT INTO results
                (student_name, course, certificate_id, marks, grade, result, result_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                student_name, course, certificate_id,
                int(marks), grade, result_value, result_date
            ))
            conn.commit()
            conn.close()
            message = "Result uploaded successfully."
        except Exception as e:
            message = "Could not save result: " + str(e)

    body = """
<div class="container">
<div class="form-box">
<h1>Admin - Result Upload</h1>

"""

    if message:
        body += "<p><b>" + message + "</b></p>"

    body += """
<form method="POST">
<label>Student Name</label>
<input name="student_name" required>

<label>Course</label>
<input name="course" required>

<label>Certificate ID</label>
<input name="certificate_id" required>

<label>Marks</label>
<input name="marks" type="number" required>

<label>Grade</label>
<input name="grade" required>

<label>Result</label>
<select name="result">
<option>PASS</option>
<option>FAIL</option>
</select>

<label>Result Date</label>
<input name="result_date" required>

<button class="btn" type="submit">Upload Result</button>
</form>
</div>
</div>
"""
    return page("Admin - VSkill", body)

@app.route("/about")
def about():
    return page("About - VSkill", """
<div class="container">
<h1>About VSkill</h1>
<p>VSkill is a study/demo learning portal created for educational and development purposes.</p>
<div class="notice"><b>Important:</b> This project is a DEMO/SAMPLE and is not an official credential verification platform.</div>
</div>
""")

@app.route("/contact")
def contact():
    return page("Contact - VSkill", """
<div class="container">
<div class="form-box">
<h1>Contact</h1>
<p>This demo project does not process real support requests.</p>
<p>For study and demonstration purposes only.</p>
</div>
</div>
""")

init_db()

if __name__ == "__main__":
    app.run(debug=True)



