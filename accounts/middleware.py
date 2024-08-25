from django.shortcuts import redirect
from django.urls import reverse
from .models import User_login


class EmailVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                user_login = User_login.objects.get(user_id=request.user)
                if not user_login.verified:
                    if request.path != reverse('confirm_email') and request.path != reverse('logout'):
                        return redirect('confirm_email')
            except User_login.DoesNotExist:
                pass

        response = self.get_response(request)
        return response
