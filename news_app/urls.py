from django.urls import path
from .views import LoginView,SignUpView,LogoutView,NewsHeadlinesView

urlpatterns = [
    path('signup', SignUpView.as_view() ),
    path('login', LoginView.as_view() ),
    path('logout', LogoutView.as_view() ),
    path('top-headlines-news', NewsHeadlinesView.as_view() ),
    
]