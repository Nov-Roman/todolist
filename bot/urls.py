from django.urls import path
from bot.views import BotView

urlpatterns = [
    path('verify', BotView.as_view(), name='bot'),
]
