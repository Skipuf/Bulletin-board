from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView

from announcement.models import Post, Comment

from .models import User_key, User_login
from .filters import CommentsFilter, PostFilter
from .forms import SignUpForm, EmailCodeForm


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.filter(email=email).first()
        if user:
            form.add_error('email', 'Указанный вами email уже занят!')
            return self.form_invalid(form)
        return super(SignUp, self).form_valid(form)


class ConfirmEmailCodeView(LoginRequiredMixin, FormView):
    template_name = 'confirm_email.html'
    form_class = EmailCodeForm
    success_url = reverse_lazy('post_list')
    context_object_name = 'form'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        user_login = User_login.objects.get(user_id=user)

        if user_login.verified:
            return redirect(reverse_lazy('post_list'))

        return super(ConfirmEmailCodeView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        key = form.cleaned_data['key']

        # Проверка наличия ключа для пользователя
        user_key = User_key.objects.filter(user_id=user).first()
        if not user_key:
            form.add_error('key', 'Ваш код устарел.')
            form.add_error('key', 'Мы отправили вам новый код.')
            User_key.objects.create(user_id=user)
            return self.form_invalid(form)

        # Проверка правильности ключа
        if not User_key.objects.filter(user_id=user, key=key).exists():
            form.add_error('key', 'Ваш код неверный!')
            return self.form_invalid(form)

        user_login = User_login.objects.get(user_id=user)
        user_login.verified = True
        user_login.save()

        return super(ConfirmEmailCodeView, self).form_valid(form)


@login_required
def profile_posts(request):
    user = request.user
    posts = Post.objects.filter(author=user, status=False).order_by('-date_posted')
    user_login = User_login.objects.get(user_id=user)

    filterset = PostFilter(request.GET, queryset=posts)

    paginator = Paginator(filterset.qs, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'userprofile': user_login,
        'page_obj': page_obj,
        'posts': page_obj,
        'filterset': filterset
    }

    return render(request, 'profile.html', context)


@login_required
def profile_comments(request):
    user = request.user
    comments = Comment.objects.filter(post__author=user, post__status=False, status="Not defined").order_by('-date_posted')

    filterset = CommentsFilter(request.GET, queryset=comments)

    paginator = Paginator(filterset.qs, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'comments': page_obj,
        'filterset': filterset
    }

    return render(request, 'profile_comments.html', context)