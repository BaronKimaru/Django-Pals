
from django.contrib import admin
from django.urls import path, re_path

from .views import (
            HomePageView, 
            UserProfileListView, 
            fetch_profile, 
            send_pal_request, 
            accept_pal_request, 
            cancel_pal_request
                )


urlpatterns = [
    path(r'', HomePageView.as_view(), name="get_users_list"),
    path('users/', UserProfileListView.as_view(), name="get_users_list"),
    re_path(r'^(?P<slug>\w+)/$', fetch_profile, name="fetch_profile"),
    path('pal_request/send/<int:id>', send_pal_request, name="send_pal_request"),
    path('pal_request/accept/<int:id>', accept_pal_request, name="accept_pal_request"),
    path('pal_request/cancel/<int:id>', cancel_pal_request, name="cancel_pal_request"),
    
]
