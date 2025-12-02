from django.urls import path
from . import views

app_name = 'discounts'

urlpatterns = [
   
    path('create/<int:event_id>/', views.discount_create, name='create'),
    
    path('delete/<int:pk>/', views.discount_delete, name='delete'),
]