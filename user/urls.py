from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('info/', views.user_info, name='user_info'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.change_password, name='change_password'),
    path('comments/', views.comments, name='comments'),
    path('deletecomment/<int:id>', views.deletecomment, name='deletecomment'),
    path('addcontent/', views.addcontent, name='addcontent'),
    path('contents/', views.contents, name='contents'),
    path('contentedit/<int:id>', views.contentedit, name='contentedit'),
    path('contentdelete/<int:id>', views.contentdelete, name='contentdelete'),
    path('contenaddimage/<int:id>', views.contenaddimage, name='contenaddimage'),
]