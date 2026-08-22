from django.urls import path
from .views import item_list, item_list_api, api_demo

urlpatterns = [
    path('', item_list, name='item_list'),
    path('api/items/', item_list_api, name='item_list_api'),
    path('api-demo/', api_demo, name='api_demo'),
]