from django.urls import path

from . import views


urlpatterns = [
    path('', views.MemberListCreateApi.as_view()),
    path('<int:pk>/match/', views.MemberLikeApi.as_view()),
]
