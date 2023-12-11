from django.urls import path
from .views import advertisement_list, advertisement_detail, create_advertisement, edit_advertisement, \
    delete_advertisement, create_comment, delete_comment, register, login_view, logout_view

urlpatterns = [
    path('', advertisement_list, name='advertisement_list'),
    path('advertisement/<int:pk>/', advertisement_detail, name='advertisement_detail'),
    path('advertisement/create/', create_advertisement, name='create_advertisement'),
    path('advertisement/<int:pk>/edit/', edit_advertisement, name='edit_advertisement'),
    path('advertisement/<int:pk>/delete/', delete_advertisement, name='delete_advertisement'),
    path('advertisement/<int:pk>/comment/', create_comment, name='create_comment'),
    path('comment/<int:pk>/delete/', delete_comment, name='delete_comment'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
