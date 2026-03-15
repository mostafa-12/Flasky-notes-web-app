from flask import current_app, url_for, redirect, flash
from itsdangerous import URLSafeTimedSerializer
from flask import jsonify
from itsdangerous import SignatureExpired, BadSignature
from app.email import Email
from app.models import User
from app.extensions import db

@Email.route("/verification/<path:token>")
def verification(token):
    try:
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        data = serializer.loads(token, salt="email-verify", max_age=3600)
        print("token valid")
    except SignatureExpired:
        print("expired")
        return jsonify({
        'status': 401,
        'message': 'The token has expired'
    }), 401
    except BadSignature:
        print("bad")
        return jsonify({
            "status" : 400,
            "message": "Invalid or tampered signature"
            }), 400
    except Exception as error:
        return jsonify ({
            "status" : 500,
            "message" : "Unexpected error"
        }), 500
        
    user = User.query.filter_by(email = data["email"]).first_or_404() 
    user.account_status = True
    print("user set status to true")
    db.session.add(user)
    db.session.commit()
    print("updated in db")
    flash("your account has been verified successfully", "success")
    return redirect(url_for("auth.login"))       