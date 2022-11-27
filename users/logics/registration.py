from users.models import User


def is_email_taken(email):
    return User.objects.filter(email=email.lower()).exists()


def is_username_taken(username):
    return User.objects.filter(username=username).exists()
