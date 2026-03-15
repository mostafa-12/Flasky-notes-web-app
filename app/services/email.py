from flask import current_app
from itsdangerous import URLSafeTimedSerializer
from flask import url_for
from app.extensions import mail
from flask_mailman import EmailMessage



def send_verify_token(email):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    data = {"email" : email}
    token = serializer.dumps(data, salt="email-verify")
    verify_url = url_for(
            "email.verification",
            token=token,
            _external=True
        )
    body = f"""
Hello,

Thank you for signing up.

Please verify your email address by clicking the link below:

{verify_url}

This link will expire in 1 hour.

If you did not create this account, you can safely ignore this email.

Notes App Team
"""
    msg = EmailMessage(
        "Verify your email address",
        body=body,
        to=[email]
    )
    msg.send()
    print("verification message send successfully")