from django.urls import path
from . import views

app_name = 'airline'
urlpatterns=[
    path('', views.index, name='index'),
    path('passager/<int:passager_id>', views.passager, name='passager'),
    path('flight/<int:fli_id>', views.flight, name='flight'),
    path('airport/<int:airport_id>', views.airport, name='airport'),
    path('upload_airport/', views. upload_airport, name='upload_airport'),
    path('upload_flight/', views. upload_flight, name='upload_flight')
]