from django.urls import path

from .views import PostCreate, PostDetail, PostUpdate, PostDelete, accept_comment, reject_comment

urlpatterns = [
    path('create/', PostCreate.as_view(), name='post_create'),

    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

    path('comment/<int:pk>/accept/', accept_comment, name='accept_comment'),
    path('comment/<int:pk>/reject/', reject_comment, name='reject_comment'),
]
