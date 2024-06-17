from django.urls import path

import chat.views

urlpatterns = [
    path('get_user/', chat.views.get_user),
    path('chat/<int:chat_id>/', chat.views.chat),
    path('reciver/<int:chat_id>/', chat.views.reciver ),
    path('sender/', chat.views.sender),
]