from django.contrib.auth.views import LoginView
from django.urls import path


from .views import (
    set_cookie_view,
    get_cookie_view,
    set_session_view,
    get_session_view,
    logout_view,
    MyLogoutView,
    AboutMeView,
    ProfileUpdateView,
    UserDetailView,
    UserListView,
    RegisterView,
    FooBarView,
    HelloView,
)

app_name = 'myauth'

urlpatterns = [
    path("login/",
         LoginView.as_view(
             template_name="myauth/login.html",
             redirect_authenticated_user = True
         ),
         name="login"
         ),
    path("logout/", logout_view, name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("hello/", HelloView.as_view(), name="hello"),

    path("about-me/", AboutMeView.as_view(), name='about-me'),
    path('user-list/', UserListView.as_view(), name='user-list'),
    path('about-user/<int:pk>/', UserDetailView.as_view(), name='about-user'),
    path('user/<int:pk>/update/', ProfileUpdateView.as_view(), name='update-profile'),


    path("cookie/get/", get_cookie_view, name="cookie-get"),
    path("cookie/set/", set_cookie_view, name="cookie-set"),

    path("session/get/", get_session_view, name="session-get"),
    path("session/set/", set_session_view, name="session-set"),
    path("foo-bar/", FooBarView.as_view(), name="foo-bar"),
]