from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    
    path('', views.event_list, name='list'),
    
    path('<int:pk>/', views.event_detail, name='detail'),
    
    path('create/' , views.event_create , name='create'),
    
    path('<int:pk>/dashboard', views.event_dashboard, name='dashboard'),
    
    path('<int:pk>/update', views.event_update, name='update'),
    
    path('<int:pk>/delete', views.event_delete, name='delete'),
    
    path('my-events/', views.my_events, name='my_events'),
    
    
]  