from app import app


def generate_confirmation_token(email):
    # return token_urlsafe(20)
    serializer = URlSafeTimeSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECRET'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email
