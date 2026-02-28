from django.urls import path
from . import views
from .views import register_user
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("start/", views.start_interview),
    path("submit/", views.submit_answer),
    path("history/", views.interview_history),
    path("dashboard/", views.dashboard_summary),
    path("register/", register_user),

    # 🔥 ADD THIS LINE
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
]