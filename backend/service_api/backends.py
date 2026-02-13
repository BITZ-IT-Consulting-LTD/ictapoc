from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        
        try:
            # Try to fetch by username or email (case-insensitive)
            user = User.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).first()
            if not user:
                 # Run the default password hasher once to reduce the timing difference
                User().set_password(password)
                return None
        except Exception:
            return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
