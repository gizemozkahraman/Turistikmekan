from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addccomment/<int:id>', views.addccomment, name='addccomment'),

]