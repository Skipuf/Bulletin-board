from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView

from subscription.forms import CreateSubscription
from subscription.models import SubscriptionMessages
from accounts.models import User_login


class SubscriptionMessagesCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('subscription.add_subscriptionmessages',)
    model = SubscriptionMessages
    form_class = CreateSubscription
    template_name = 'subscription_messages_create.html'


@login_required
def subscribe(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')

        if user_id and action:
            profile = User_login.objects.get(id=user_id)

            if action == 'subscribe':
                profile.is_subscribed = True
            else:
                profile.is_subscribed = False

            profile.save()
            return redirect('account_profile')