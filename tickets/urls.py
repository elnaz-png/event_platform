from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [

    path('purchase/<int:event_id>/', views.ticket_purchase, name='purchase'),
    path('my-tickets/', views.ticket_list, name='list'),

]