from users.models import User


def authenticate(name: str, password: str):
    if '@' in name:
        user = User.objects.get(email=name.lower())
    else:
        user = User.objects.get(username=name)

    if user.check_password(password):
        return user
    return
