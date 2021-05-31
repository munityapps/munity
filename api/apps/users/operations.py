from .models import User
from rest_framework.exceptions import PermissionDenied

def update_user_password(pk, old_password, new_password):
    """
        Check and update user password:
            - check if old password correspond with user password
            - update user password
            - save user
    """
    user = User.objects.get(pk=pk)
    user_password_is_correct = user.check_password(old_password)

    if old_password and user_password_is_correct:
        user.set_password(new_password)
        user.save()
    else:
        raise PermissionDenied("wrong_password")
