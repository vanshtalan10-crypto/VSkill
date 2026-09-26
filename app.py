from flask import Flask, request, redirect, url_for
import sqlite3

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


STYLE = """
<style>
*{box-sizing:border-box}
body{
    margin:0;
    font-family:Arial,Helvetica,sans-serif;
    background:#f5f7fb;
    color:#172033;
}
a{text-decoration:none;color:inherit}
.navbar{
    background:#ffffff;
    border-bottom:1px solid #e5e7eb;
    position:sticky;
    top:0;
    z-index:100;
}
.nav-inner{
    max-width:1180px;
    margin:auto;
    padding:16px 20px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:20px;
}
.logo{
    font-size:25px;
    font-weight:900;
    color:#2563eb;
}
.nav-links{
    display:flex;
    gap:24px;
    align-items:center;
}
.nav-links a{
    color:#475467;
    font-weight:600;
}
.nav-links a:hover{color:#2563eb}
.nav-btn{
    background:#2563eb!important;
    color:#fff!important;
    padding:10px 18px;
    border-radius:10px;
}
.container{
    max-width:1180px;
    margin:auto;
    padding:0 20px;
}
.hero{
    padding:90px 20px;
    background:linear-gradient(135deg,#eff6ff,#ffffff);
}
.hero-inner{
    max-width:1180px;
    margin:auto;
    display:grid;
    grid-template-columns:1.1fr .9fr;
    gap:50px;
    align-items:center;
}
.badge{
    display:inline-block;
    background:#dbeafe;
    color:#1d4ed8;
    padding:8px 14px;
    border-radius:30px;
    font-weight:700;
}
.hero h1{
    font-size:54px;
    line-height:1.05;
    margin:20px 0;
}
.hero h1 span{color:#2563eb}
.hero p{
    color:#667085;
    font-size:18px;
    line-height:1.7;
}
.hero-buttons{
    display:flex;
    gap:12px;
    margin-top:30px;
}
.btn{
    display:inline-block;
    padding:14px 22px;
    border-radius:11px;
    font-weight:700;
}
.btn-primary{
    background:#2563eb;
    color:white;
}
.btn-light{
    background:white;
    border:1px solid #d0d5dd;
}
.hero-card{
    background:white;
    border-radius:24px;
    padding:12px;
    box-shadow:0 20px 60px rgba(0,0,0,.1);
}
.hero-card img{
    width:100%;
    height:360px;
    object-fit:cover;
    border-radius:18px;
}
.section{
    padding:75px 0;
}
.section-title{
    text-align:center;
    margin-bottom:40px;
}
.section-title h2{
    font-size:36px;
    margin-bottom:10px;
}
.section-title p{color:#667085}
.course-grid{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:22px;
}
.course-card{
    background:white;
    border-radius:18px;
    overflow:hidden;
    border:1px solid #eaecf0;
    transition:.2s;
}
.course-card:hover{
    transform:translateY(-5px);
    box-shadow:0 15px 35px rgba(0,0,0,.08);
}
.course-card img{
    width:100%;
    height:175px;
    object-fit:cover;
}
.course-content{padding:20px}
.course-content h3{margin:0 0 10px}
.course-content p{
    color:#667085;
    line-height:1.5;
    min-height:48px;
}
.course-meta{
    display:flex;
    justify-content:space-between;
    margin-top:15px;
    color:#667085;
    font-size:14px;
}
.rating{color:#d97706;font-weight:700}
.features{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:22px;
}
.feature{
    background:white;
    padding:28px;
    border-radius:18px;
    border:1px solid #eaecf0;
}
.feature-icon{
    font-size:32px;
    margin-bottom:15px;
}
.stats{
    background:#111827;
    color:white;
    padding:55px 20px;
}
.stats-grid{
    max-width:1000px;
    margin:auto;
    display:grid;
    grid-template-columns:repeat(4,1fr);
    text-align:center;
}
.stat h3{
    font-size:34px;
    margin:0 0 8px;
}
.stat p{color:#cbd5e1}
.verify-section{
    padding:70px 20px;
    background:#eff6ff;
}
.verify-box{
    max-width:850px;
    margin:auto;
    background:white;
    padding:40px;
    border-radius:22px;
    box-shadow:0 15px 45px rgba(0,0,0,.08);
}
.verify-box h2{
    text-align:center;
    margin-top:0;
}
.verify-box p{
    text-align:center;
    color:#667085;
}
.verify-form{
    display:flex;
    gap:12px;
    margin-top:25px;
}
.verify-form input{
    flex:1;
    padding:15px;
    border:1px solid #d0d5dd;
    border-radius:10px;
    font-size:16px;
}
.verify-form button{
    padding:15px 24px;
    border:0;
    background:#2563eb;
    color:white;
    border-radius:10px;
    font-weight:700;
    cursor:pointer;
}
.footer{
    background:#111827;
    color:#cbd5e1;
    padding:40px 20px;
    text-align:center;
}
.verify-page{
    min-height:70vh;
    padding:60px 20px;
}
.certificate{
    position:relative;
    max-width:850px;
    margin:35px auto 0;
    padding:50px;
    background:#fff;
    border:8px solid #1d4ed8;
    border-radius:10px;
    text-align:center;
    overflow:hidden;
}
.sample-watermark{
    position:absolute;
    left:0;
    right:0;
    top:40%;
    font-size:75px;
    font-weight:900;
    color:rgba(220,38,38,.08);
    transform:rotate(-20deg);
    pointer-events:none;
}
.cert-title{
    font-size:34px;
    font-weight:900;
}
.cert-sub{
    color:#667085;
    margin:10px 0 30px;
}
.student{
    font-size:30px;
    font-weight:900;
    margin:15px 0;
}
.course-name{
    color:#2563eb;
    font-size:22px;
    font-weight:800;
}
.cert-grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:15px;
    margin-top:30px;
    text-align:left;
}
.cert-item{
    padding:16px;
    background:#f8fafc;
    border-radius:10px;
}
.cert-item span{
    display:block;
    color:#667085;
    font-size:13px;
    margin-bottom:6px;
}
.cert-item strong{font-size:17px}
.cert-id{
    color:#dc2626!important;
    font-size:20px!important;
}
.demo-badge{
    display:inline-block;
    margin-top:25px;
    padding:9px 18px;
    border-radius:30px;
    background:#fee2e2;
    color:#b91c1c;
    font-weight:800;
}
.error{
    margin-top:20px;
    padding:14px;
    background:#fee2e2;
    color:#991b1b;
    border-radius:10px;
    text-align:center;
}
.admin-box{
    max-width:850px;
    margin:50px auto;
    background:white;
    padding:35px;
    border-radius:22px;
    box-shadow:0 15px 45px rgba(0,0,0,.08);
}
.admin-grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:18px;
}
.admin-grid input{
    width:100%;
    padding:14px;
    border:1px solid #d0d5dd;
    border-radius:10px;
    margin-top:7px;
}
.admin-full{grid-column:1/-1}
.admin-btn{
    margin-top:20px;
    padding:14px 25px;
    background:#2563eb;
    color:white;
    border:0;
    border-radius:10px;
    font-weight:700;
}
.success{
    margin-bottom:20px;
    padding:14px;
    background:#dcfce7;
    color:#166534;
    border-radius:10px;
}
@media(max-width:900px){
    .course-grid{grid-template-columns:repeat(2,1fr)}
    .hero-inner{grid-template-columns:1fr}
    .features{grid-template-columns:1fr}
}
@media(max-width:650px){
    .nav-links{display:none}
    .hero h1{font-size:40px}
    .course-grid{grid-template-columns:1fr}
    .stats-grid{grid-template-columns:1fr 1fr;gap:25px}
    .verify-form{flex-direction:column}
    .cert-grid{grid-template-columns:1fr}
    .certificate{padding:30px 15px}
    .admin-grid{grid-template-columns:1fr}
    .admin-full{grid-column:auto}
}
</style>
"""


NAV = """
<nav class="navbar">
<div class="nav-inner">
<a href="/" class="logo">VSkill</a>
<div class="nav-links">
<a href="/">Home</a>
<a href="/courses">Courses</a>
<a href="/results">Results</a>
<a href="/about">About</a>
<a href="/contact">Contact</a>
<a href="/admin" class="nav-btn">Admin</a>
</div>
</div>
</nav>
"""


def course_cards():
    cards = ""

    for index, course in enumerate(COURSES):
        name, description, duration, rating = course

        cards += """
        <div class="course-card">
            <img src="""" + IMAGES[index] + """" alt="Course">
            <div class="course-content">
                <h3>""" + name + """</h3>
                <p>""" + description + """</p>
                <div class="course-meta">
                    <span>""" + duration + """</span>
                    <span class="rating">★ """ + rating + """</span>
                </div>
            </div>
        </div>
        """

    return cards


@app.route("/")
def home():
    cards = course_cards()

    return """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VSkill - Learn Skills That Matter</title>
""" + STYLE + """
</head>
<body>

""" + NAV + """

<section class="hero">
<div class="hero-inner">
<div>
<span class="badge">DEMO LEARNING PLATFORM</span>
<h1>Learn Skills.<br><span>Build Your Future.</span></h1>
<p>
VSkill is a modern demo learning platform designed to help students
explore technology, business and professional skills.
</p>

<div class="hero-buttons">
<a href="/courses" class="btn btn-primary">Explore Courses</a>
<a href="/results" class="btn btn-light">Verify Certificate</a>
</div>
</div>

<div class="hero-card">
<img src="https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1000&q=80" alt="Students">
</div>
</div>
</section>

<section class="section">
<div class="container">
<div class="section-title">
<h2>Popular Courses</h2>
<p>Build practical skills with structured learning paths.</p>
</div>

<div class="course-grid">
""" + cards + """
</div>
</div>
</section>

<section class="stats">
<div class="stats-grid">
<div class="stat">
<h3>8+</h3>
<p>Courses</p>
</div>
<div class="stat">
<h3>4.8★</h3>
<p>Average Rating</p>
</div>
<div class="stat">
<h3>10K+</h3>
<p>Demo Learners</p>
</div>
<div class="stat">
<h3>100%</h3>
<p>Learning Focused</p>
</div>
</div>
</section>

<section class="section">
<div class="container">
<div class="section-title">
<h2>Why Learn With VSkill?</h2>
<p>Designed around practical learning.</p>
</div>

<div class="features">

<div class="feature">
<div class="feature-icon">🎯</div>
<h3>Practical Learning</h3>
<p>Focus on useful skills, projects and real-world concepts.</p>
</div>

<div class="feature">
<div class="feature-icon">📚</div>
<h3>Structured Courses</h3>
<p>Organized learning paths for beginners and students.</p>
</div>

<div class="feature">
<div class="feature-icon">🏆</div>
<h3>Certificate Demo</h3>
<p>Practice certificate verification through this demo system.</p>
</div>

</div>
</div>
</section>

<section class="verify-section">
<div class="verify-box">
<h2>Verify a Certificate</h2>
<p>Enter a demo Certificate ID to view the sample result.</p>

<form action="/results" method="POST" class="verify-form">
<input name="certificate_id" placeholder="Example: VS2609260117" required>
<button type="submit">Verify</button>
</form>

</div>
</section>

<footer class="footer">
<p>© 2026 VSkill Demo Platform</p>
<p>DEMO / SAMPLE — Not an official credential verification service.</p>
</footer>

</body>
</html>
"""


@app.route("/courses")
def courses():
    return """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Courses - VSkill</title>
""" + STYLE + """
</head>
<body>

""" + NAV + """

<section class="section">
<div class="container">

<div class="section-title">
<h2>All Courses</h2>
<p>Explore the VSkill demo course catalog.</p>
</div>

<div class="course-grid">
""" + course_cards() + """
</div>

</div>
</section>

<footer class="footer">
<p>VSkill Demo Platform</p>
</footer>

</body>
</html>
"""


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

        if result is None:
            message = "Certificate ID not found. Please check the ID."

    html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Certificate Verification - VSkill Demo</title>
""" + STYLE + """
</head>
<body>

""" + NAV + """

<section class="verify-page">

<div class="verify-box">
<h2>Certificate Verification</h2>
<p>DEMO / SAMPLE certificate verification system.</p>

<form method="POST" class="verify-form">
<input name="certificate_id" placeholder="Enter Certificate ID" required>
<button type="submit">Verify Certificate</button>
</form>
"""

    if message:
        html += """
<div class="error">
""" + message + """
</div>
"""

    if result is not None:
        html += """
<div style="max-width:1000px;margin:35px auto;text-align:center;">
    <img
        src="/static/certificate.png"
        alt="Demo Certificate"
        style="width:100%;height:auto;display:block;border-radius:8px;"
    >

    <a
        href="/static/certificate.png"
        download="VSkill-Demo-Certificate.png"
        style="display:inline-block;margin-top:22px;padding:14px 25px;background:#2563eb;color:white;border-radius:10px;text-decoration:none;font-weight:700;"
    >
        Download Certificate
    </a>
</div>
    html += """
</div>
</section>

<footer class="footer">
<p>VSkill Demo Platform</p>
<p>DEMO / SAMPLE — For study and demonstration purposes.</p>
</footer>

</body>
</html>
"""

    return html


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
                student_name,
                course,
                certificate_id,
                int(marks),
                grade,
                result_value,
                result_date
            ))

            conn.commit()
            conn.close()

            message = "Demo result uploaded successfully."

        except Exception as e:
            message = "Could not upload result: " + str(e)

    html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Admin - VSkill Demo</title>
""" + STYLE + """
</head>
<body>

""" + NAV + """

<section class="verify-page">

<div class="admin-box">

<h2>Demo Result Upload</h2>
<p>For study/demo use only.</p>
"""

    if message:
        html += """
<div class="success">
""" + message + """
</div>
"""

    html += """
<form method="POST">

<div class="admin-grid">

<div>
<label>Student Name</label>
<input name="student_name" required>
</div>

<div>
<label>Course</label>
<input name="course" required>
</div>

<div>
<label>Certificate ID</label>
<input name="certificate_id" placeholder="VS-DEMO-2602" required>
</div>

<div>
<label>Marks</label>
<input name="marks" type="number" min="0" max="100" required>
</div>

<div>
<label>Grade</label>
<input name="grade" placeholder="A" required>
</div>

<div>
<label>Result</label>
<input name="result" value="PASS" required>
</div>

<div class="admin-full">
<label>Result Date</label>
<input name="result_date" value="26 September 2026" required>
</div>

</div>

<button class="admin-btn" type="submit">
Upload Demo Result
</button>

</form>

</div>
</section>

<footer class="footer">
<p>VSkill Demo Platform</p>
</footer>

</body>
</html>
"""

    return html


@app.route("/about")
def about():
    return """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>About - VSkill</title>
""" + STYLE + """
</head>
<body>
""" + NAV + """
<section class="section">
<div class="container">
<div class="section-title">
<h2>About VSkill</h2>
<p>VSkill is a study/demo learning platform created for educational purposes.</p>
</div>
<div class="feature">
<h3>Learning Platform Demo</h3>
<p>
This website demonstrates a modern course portal with course listings,
certificate result lookup and demo result management.
</p>
</div>
</div>
</section>
<footer class="footer">
<p>VSkill Demo Platform</p>
</footer>
</body>
</html>
"""


@app.route("/contact")
def contact():
    return """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Contact - VSkill</title>
""" + STYLE + """
</head>
<body>
""" + NAV + """
<section class="section">
<div class="container">
<div class="section-title">
<h2>Contact</h2>
<p>Demo contact page.</p>
</div>

<div class="feature">
<h3>VSkill Demo Support</h3>
<p>Email: demo@vskill.local</p>
<p>This is a demonstration website for study purposes.</p>
</div>

</div>
</section>
<footer class="footer">
<p>VSkill Demo Platform</p>
</footer>
</body>
</html>
"""


if __name__ == "__main__":
    init_db()
    app.run(debug=True)

