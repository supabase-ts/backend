from django.urls import path

from user.views.appointment import AppointmentAPIView
from user.views.authentication import RegisterAPIView, LoginAPIView
from user.views.features import ChatbotAPIView, MatchmakingAPIView
from user.views.profile import MoneyInOutAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('talk/', ChatbotAPIView.as_view(), name='talk'),
    path('in-out/', MoneyInOutAPIView.as_view(), name='in-out'),
    path('matchmaking/', MatchmakingAPIView.as_view(), name='matchmaker'),
    path('appointment/', AppointmentAPIView.as_view(), name='appointment'),
]
