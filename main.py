from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
import os
import pyotp
import random
import string

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'Umangmodi003@gmail.com'  # Update with your email
app.config['MAIL_PASSWORD'] = 'uuhxwzpcyodnwmfw'  # Update with your email password
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'  # Update with your sender email

mail = Mail(app)

## Generate OTP
def generate_otp():
    otp = ''.join(random.choices(string.digits, k=4))
    return otp

# Route for rendering OTP form and sending OTP via email
@app.route('/', methods=['GET', 'POST'])
def send_otp():
    if request.method == 'POST':
        email = request.form['email']
        otp = generate_otp()

        # HTML structure for the email body
        email_body = f"""
        <html>
        <head></head>
        <body>
            <h2>OTP Verification</h2>
            <p>Dear User,</p>
            <p>Your OTP for verification is:</p>
            <p style="font-size: 24px; font-weight: bold; color: #007bff;">{otp}</p>
            <p>Please enter this OTP on the verification page.</p>
        </body>
        </html>
        """

        # Send OTP email via Flask-Mail
        msg = Message('OTP Verification', recipients=[email])
        msg.html = email_body
        mail.send(msg)

        # Store OTP secret in session for verification (optional)
        session['otp_secret'] = otp

        flash('OTP sent successfully via email.', 'success')
        return redirect(url_for('verify_otp', email=email))

    return render_template('otp_form.html')

# Route for verifying OTP
@app.route('/verify/<email>', methods=['GET', 'POST'])
def verify_otp(email):
    if request.method == 'POST':
        entered_otp = request.form['otp']
        otp_secret = session.get('otp_secret')
        
        # Verify entered OTP
        if otp_secret == entered_otp:
            # Clear OTP secret from session after successful verification
            session.pop('otp_secret', None)
            flash('OTP verified successfully.', 'success')
            return redirect(url_for('success'))
        else:
            flash('Invalid OTP. Please try again.', 'danger')

    return render_template('verify_otp.html', email=email)



# Route for success page
@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)