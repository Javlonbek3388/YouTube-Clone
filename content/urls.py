from django.urls import path, include
from .views import (VideoListView, VideoCreateView, VideoRetrieveView, VideoUpdateView, VideoDeleteView, LikeView, CommentViewSet)
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'video-like', LikeView, basename='video-likes')
# router.register(r'video-comment', CommentViewSet, basename='vide-comment')

urlpatterns = [
    path('', include(router.urls)),
    path('video-list/', VideoListView.as_view(), name='Video-list'),
    path('create/', VideoCreateView.as_view(), name='Video-create'),
    path('retrieve/<uuid:pk>/', VideoRetrieveView.as_view(), name='Video-retrieve'),
    path('update/<uuid:pk>/', VideoUpdateView.as_view(), name='Video-update'),
    path('delete/<uuid:pk>/', VideoDeleteView.as_view(), name='Video-delete'),
    path('video-comment/', CommentViewSet.as_view(), name='Video-comment')
]
