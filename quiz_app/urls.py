from django.urls import path
from .views import index,register, user_login, user_logout, QuizList, question, google_login, leaderBoard, answer, create_order, success, about, faqs, contact, responsible_gaming
urlpatterns = [
    path('',index, name='landing_page'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='signuppage'),
    path('quiz/<int:id>/', question, name='question'),
    path('google/', google_login, name='google'),
    path('leaderboard/', leaderBoard, name='leaderboard'),
    path('answer/<int:id>/', answer, name='answer'),
    path('create_order/', create_order, name='create_order'),
    path('success/', success, name='success'),
    path('about/', about, name='about'),
    path('faqs/', faqs, name='faqs'),
    path('contact/', contact, name='contact'),
    path('responsible_gaming/', responsible_gaming, name='responsible_gaming'),
]
