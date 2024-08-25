from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .filters import PostFilter
from .forms import PostForm, CommentForm
from .models import Post, Comment


def postlist(request):
    posts = Post.objects.filter(status=False).order_by('-date_posted')

    filterset = PostFilter(request.GET, queryset=posts)

    paginator = Paginator(filterset.qs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'posts': page_obj,
        'filterset': filterset
    }

    return render(request, 'posts.html', context)


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.request.user
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = self.request.user
            comment.post = self.object
            comment.save()
            return redirect('/')

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != self.request.user:
            return redirect(reverse_lazy('post_list'))
        return super().dispatch(request, *args, **kwargs)


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_del.html'
    success_url = reverse_lazy('post_list')

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != self.request.user:
            return redirect(reverse_lazy('post_list'))
        return super().dispatch(request, *args, **kwargs)


@login_required
def accept_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.post.author == request.user:
        comment.status = 'Accepted'
        comment.save()
        post = comment.post
        post.status = True
        post.save()
    return redirect('account_profile_comments')


@login_required
def reject_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.post.author == request.user:
        comment.status = 'Rejected'
        comment.save()
    return redirect('account_profile_comments')
