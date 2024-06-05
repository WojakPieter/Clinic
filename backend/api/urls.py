from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name='login'),
    path('notes/', views.GetNotesView.as_view(), name='note'),
    path("register/", views.RegisterView.as_view(), name='register'),
    path("user/", views.GetUserView.as_view(), name="user"),
    path("refresh_token/", views.RefreshTokenView.as_view(), name="refresh"),
    path("patients/", views.GetPatientsView.as_view(), name="patients"),
    path("add_note/", views.AddNoteView.as_view(), name="add_note")
]
