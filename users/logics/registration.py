from users.models import User


def is_email_taken(email):
    return User.objects.filter(email=email.lower()).exists()
