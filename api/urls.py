from django.urls import path
from .views import *

urlpatterns = [


    path('get_all/<str:model>/', get_all),
    path('get/<str:model>/<str:pk>/', get),
    path('create/<str:model>/', create),
    path('update/<str:model>/<str:pk>/', update),
    path('delete/<str:model>/<str:pk>/', delete),
    path('analytic/', analytic),

]