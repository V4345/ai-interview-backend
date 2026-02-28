from django.urls import path
from . import views
from .views import register_user

urlpatterns = [
    path("start/", views.start_interview),
    path("submit/", views.submit_answer),
    path("history/", views.interview_history),
    path("dashboard/", views.dashboard_summary),
    path("register/", register_user)

]