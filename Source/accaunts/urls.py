from django.urls import path

from accaunts.views import login_view, logout_view

app_name = "accaunts"

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout')
]
