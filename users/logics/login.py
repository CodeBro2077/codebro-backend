from users.models import User


def authenticate(name: str, password: str):
    try:
        if '@' in name:
            user = User.objects.get(email=name.lower())

        else:
            user = User.objects.get(username=name)

    except User.DoesNotExist:
        return

    if user.check_password(password):
        return user
    return
