
from django.contrib import admin
from django.urls import path

from .views import (
            ProfileListView, 
            fetch_profile, 
            send_pal_request, 
            accept_pal_request, 
            cancel_pal_request
                )


urlpatterns = [
    path('<slug>', fetch_profile, name="fetch_profile"),
    path('', ProfileListView.as_view(), name="get_users_list"),
    path('pal_request/send/<int:id>', send_pal_request, name="send_pal_request"),
    path('pal_request/accept/<int:id>', accept_pal_request, name="accept_pal_request"),
    path('pal_request/cancel/<int:id>', cancel_pal_request, name="cancel_pal_request"),
    
]
