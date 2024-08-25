from django.urls import path
from .views import SignUp, ConfirmEmailCodeView, profile_posts, profile_comments

urlpatterns = [
    path('', profile_posts, name='account_profile'),
    path('comments', profile_comments, name='account_profile_comments'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('confirm-email/', ConfirmEmailCodeView.as_view(), name='confirm_email'),
]