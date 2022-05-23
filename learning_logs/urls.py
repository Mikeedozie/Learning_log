from django.urls import path
from . import views




urlpatterns = [
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('topics/<topic_id>', views.entries, name='entries'),
    path('topics/new_topic/', views.new_topic, name='new_topic'),
    path('topics/<topic_id>/new_entry', views.new_entry, name='new_entry'),
    path('topics/<entry_id>/edit_entry', views.edit_entry, name='edit_entry'),
    
]
