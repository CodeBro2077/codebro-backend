from users.models import User


def authenticate(name: str, password: str):
    if '@' in name:
        try:
            user = User.objects.get(email=name.lower())
        except User.DoesNotExist:
            return

    else:
        try:
            user = User.objects.get(username=name)
        except User.DoesNotExist:
            return

    if user.check_password(password):
        return user
    return
