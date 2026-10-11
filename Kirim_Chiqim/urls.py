from django.urls import path
from . import views

urlpatterns = [path('signup/', views.SignUpView.as_view()),
               path('code_verify/', views.VerifyView.as_view()),
               path('update_properties/', views.UpdateUserPropertiesView.as_view())]

