from django.urls import path
from . import views

urlpatterns = [path('signup/', views.SignUpView.as_view()),
               path('code_verify/', views.VerifyView.as_view()),
               path('update_properties/', views.UpdateUserPropertiesView.as_view()),\
               path('transaction/', views.TransactionView.as_view()),
               path('token_refresh/', views.TokenRefreshView.as_view())
               ]

