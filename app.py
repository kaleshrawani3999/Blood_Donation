from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector
import smtplib
from email.mime.text import MIMEText
import random
import os

# AI
from openai import OpenAI

app = Flask(__name__)
app.secret_key = "secretkey123"

# OpenAI client
client = OpenAI(api_key="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")


# ---------------- AI CHATBOT ----------------
@app.route("/ai-chat", methods=["POST"])
def ai_chat():

    data = request.get_json()
    user_message = data.get("message")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"You are a blood donation assistant."},
                {"role":"user","content":user_message}
            ]
        )

        reply = response.choices[0].message.content

    except Exception as e:
        print("AI error:", e)
        reply = "AI error occurred"

    return jsonify({"reply": reply})

# ---------------- DATABASE ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="blood_donation"
)

cursor = db.cursor(buffered=True)


# ---------------- HOME ----------------
@app.route("/")
def home():

    cursor.execute("SELECT blood_group, COUNT(*) FROM donors GROUP BY blood_group")
    result = cursor.fetchall()

    blood_data = {
        "A+":0,"A-":0,
        "B+":0,"B-":0,
        "O+":0,"O-":0,
        "AB+":0,"AB-":0
    }

    for group,count in result:
        blood_data[group] = count

    return render_template("index.html", blood_data=blood_data)


# ---------------- ADD CAMP ----------------
@app.route('/add-camp', methods=['GET','POST'])
def add_camp():

    if request.method == 'POST':

        camp_name = request.form['camp_name']
        camp_date = request.form['camp_date']
        location = request.form['location']
        description = request.form['description']

        cursor.execute(
        "INSERT INTO camps (camp_name,camp_date,location,description) VALUES (%s,%s,%s,%s)",
        (camp_name,camp_date,location,description)
        )

        db.commit()

        return redirect('/admin-dashboard')

    return render_template("add_camp.html")


# ---------------- CAMPS PAGE ----------------
@app.route('/camps')
def camps():

    cursor.execute("SELECT * FROM camps")

    camps = cursor.fetchall()

    return render_template("camps.html", camps=camps)

# ---------------- FORGOT
@app.route('/forgot-password', methods=['GET','POST'])
def forgot_password():

    if request.method == 'POST':

        username = request.form['username']
        new_password = request.form['new_password']

        cursor.execute(
            "UPDATE admin SET password=%s WHERE username=%s",
            (new_password, username)
        )

        db.commit()

        return redirect('/admin-login')

    return render_template("forgot_password.html")
# ---------------- REGISTER DONOR ----------------
@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        blood = request.form['blood']
        location = request.form['location']
        password = request.form['password']

        lat = request.form.get('lat')
        lon = request.form.get('lon')

        cursor.execute("""
        INSERT INTO donors
        (name,email,phone,blood_group,location,password,latitude,longitude)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """,(name,email,phone,blood,location,password,lat,lon))

        db.commit()

        return redirect('/')

    return render_template('register.html')

# -----------------ABOUT PAGE------------
@app.route('/about')
def about():
    return render_template('about.html')

# ---------------- EMAIL FUNCTION ----------------
def send_blood_alert(email, blood_group, location, priority):

    try:

        sender_email = "kaleshrawani3999@gmail.com"
        sender_password = "psdk byjl rcug iaho"

        message = f"""
 🚨 Blood Request Alert

Blood Group Needed: {blood_group}
Location: {location}
Priority Level: {priority}
Please contact hospital if you can donate.
Please donate if possible.
 Blood Donation Management System
"""

        msg = MIMEText(message)
        msg['Subject'] = "Emergency Blood Request"
        msg['From'] = sender_email
        msg['To'] = email

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()

    except Exception as e:
        print("Email error:", e)


# ---------------- SEARCH DONOR ----------------
@app.route('/search', methods=['GET','POST'])
def search():

    donors = []
    cursor.execute("SELECT * FROM donors")

    if request.method == 'POST':

        blood = request.form['blood']
        location = request.form['location']

        cursor.execute(
            "SELECT * FROM donors WHERE blood_group=%s AND location=%s",
            (blood, location)
        )

        donors = cursor.fetchall()

    return render_template('search.html', donors=donors)


# ---------------- CHANGE PASSWORD----------
@app.route("/change-password", methods=["GET","POST"])
def change_password():

    if request.method == "POST":

        old = request.form["old_password"]
        new = request.form["new_password"]

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="blood_donation"
        )

        cursor = db.cursor(buffered=True)

        cursor.execute("SELECT password FROM admin WHERE id=1")
        current = cursor.fetchone()[0]

        if old == current:

            cursor.execute(
            "UPDATE admin SET password=%s WHERE id=1",
            (new,)
            )

            conn.commit()

            return "Password Updated"

        else:
            return "Old password incorrect"

    return render_template("change_password.html")
# ---------------- BLOOD REQUEST ----------------
@app.route('/request', methods=['GET','POST'])
def request_blood():

    if request.method == 'POST':

        name = request.form['name']
        blood = request.form['blood']
        hospital = request.form['hospital']
        contact = request.form['contact']
        location = request.form['location']
        priority = request.form['priority']

        cursor.execute("""
        INSERT INTO requests (patient_name,blood_group,hospital,contact,location,priority)
        VALUES (%s,%s,%s,%s,%s,%s)
        """,(name,blood,hospital,contact,location,priority))

        db.commit()

        cursor.execute("SELECT email FROM donors WHERE blood_group=%s",(blood,))
        donors = cursor.fetchall()

        for donor in donors:
            send_blood_alert(donor[0], blood, location, priority)

        cursor.execute("""
        SELECT name,phone,location
        FROM donors
        WHERE blood_group=%s AND location=%s
        """,(blood,location))

        matched_donors = cursor.fetchall()

        return render_template("matched_donors.html",
                               donors=matched_donors,
                               blood=blood)

    return render_template('request.html')


# ---------------- ADMIN LOGIN ----------------
@app.route('/admin-login', methods=['GET','POST'])
def admin_login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        cursor.execute(
            "SELECT * FROM admin WHERE username=%s AND password=%s",
            (username,password)
        )

        admin = cursor.fetchone()

        if admin:
            session['admin'] = username
            return redirect('/admin-dashboard')

    return render_template('admin_login.html')


# ---------------- ADMIN DASHBOARD ----------------
@app.route('/admin-dashboard')
def admin_dashboard():

    if 'admin' not in session:
        return redirect('/admin-login')

    # donors list
    cursor.execute("SELECT * FROM donors")
    donors = cursor.fetchall()

    # requests list
    cursor.execute("SELECT * FROM requests")
    requests = cursor.fetchall()

    # total donors
    cursor.execute("SELECT COUNT(*) FROM donors")
    total_donors = cursor.fetchone()[0]

    # total requests
    cursor.execute("SELECT COUNT(*) FROM requests")
    total_requests = cursor.fetchone()[0]

    # urgent requests
    cursor.execute("SELECT COUNT(*) FROM requests WHERE priority='Urgent'")
    urgent_requests = cursor.fetchone()[0]

    # critical requests
    cursor.execute("SELECT COUNT(*) FROM requests WHERE priority='Critical'")
    critical_requests = cursor.fetchone()[0]

    # blood group stats
    cursor.execute("SELECT blood_group,COUNT(*) FROM donors GROUP BY blood_group")
    blood_stats = cursor.fetchall()

    return render_template(
        "admin_dashboard.html",
        donors=donors,
        requests=requests,
        total_donors=total_donors,
        total_requests=total_requests,
        urgent_requests=urgent_requests,
        critical_requests=critical_requests,
        blood_stats=blood_stats
    )
# ---------------- DELETE DONOR ----------------
@app.route('/delete-donor/<int:id>')
def delete_donor(id):

    if 'admin' not in session:
        return redirect('/admin-login')

    cursor.execute("DELETE FROM donors WHERE id=%s", (id,))
    db.commit()

    return redirect('/admin-dashboard')


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('admin',None)
    return redirect('/admin-login')


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
