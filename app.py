from flask import Flask, render_template, request, flash, redirect, url_for
import os
from email.message import EmailMessage
import smtplib
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
email_address = os.getenv('EMAIL_ADDRESS')
email_password = os.getenv('EMAIL_PASSWORD')
email_receiver = os.getenv('EMAIL_RECEIVER')
secret_key = os.getenv('SECRET_KEY')

app.secret_key = secret_key

def send_email(name, email, message):
    msg = EmailMessage()
    msg['Subject'] = f'Portfolio Contact from {name}'
    msg['From'] = os.getenv('EMAIL_ADDRESS')
    msg['To'] = os.getenv('EMAIL_RECEIVER')
    msg.set_content(f"Name: {name}\nEmail: {email}\nMessage:\n{message}")
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.getenv('EMAIL_ADDRESS'), os.getenv('EMAIL_PASSWORD'))
        smtp.send_message(msg)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        if not name or not email or not message:
            flash('Please fill in all fields', 'danger')
        else:
            try:
                send_email(name, email, message)
                flash('Message sent successfully!', 'success')
            except Exception as e:
                flash(f'Failed to send message: {e}', 'danger')
        return redirect(url_for('index'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)