from django.urls import path

from .views import SubscriptionMessagesCreate, subscribe

urlpatterns = [
    path('create/', SubscriptionMessagesCreate.as_view(), name='Subscription_Messages_create'),
    path('subscribe/', subscribe, name='subscribe'),
]
