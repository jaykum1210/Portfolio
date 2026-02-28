from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Email configuration from environment variables
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
RECEIVER_EMAIL = 'jaykum122005@gmail.com'

@app.route('/contact', methods=['POST'])
def contact():
    """
    Handle contact form submissions.
    Receives JSON with email, subject, and message fields.
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Extract form fields
        user_email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')
        
        # Validate required fields
        if not user_email or not subject or not message:
            return jsonify({
                'success': False,
                'message': 'Please fill in all required fields (email, subject, message).'
            }), 400
        
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f'Portfolio Contact: {subject}'
        
        # Email body with formatted content
        body = f"""
        New contact form submission from your portfolio website.
        
        ---------------------------
        Sender Email: {user_email}
        Subject: {subject}
        ---------------------------
        
        Message:
        {message}
        
        ---------------------------
        This email was sent from Jay Kumawat's Portfolio Contact Form
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email via Gmail SMTP
        # Port 587 for TLS (recommended)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Upgrade connection to secure TLS
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        # Send the email
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
        server.quit()
        
        # Return success response
        return jsonify({
            'success': True,
            'message': 'Message sent successfully!'
        }), 200
        
    except smtplib.SMTPAuthenticationError:
        # Authentication failed (wrong email/password)
        return jsonify({
            'success': False,
            'message': 'Email server authentication failed. Please check your credentials.'
        }), 500
        
    except smtplib.SMTPException as e:
        # SMTP server error
        return jsonify({
            'success': False,
            'message': f'Email server error: {str(e)}'
        }), 500
        
    except Exception as e:
        # Any other unexpected error
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500


@app.route('/')
def home():
    """Root endpoint - API is running."""
    return jsonify({
        'message': 'Jay Kumawat Portfolio Backend API is running!',
        'endpoints': {
            'POST /contact': 'Submit contact form'
        }
    })


# Run the app
if __name__ == '__main__':
    # Debug mode is helpful during development
    app.run(debug=True, port=5000)
