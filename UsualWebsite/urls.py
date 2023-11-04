from django.urls import path
from . import views

urlpatterns =[
    path('',views.session.homePage,name='homePage'),
    path('searchresults/',views.session.searchPage,name='searchPage'),
    path('checkout/',views.session.checkout,name='checkout'),
    path('register/',views.session.register,name="Register"),
    path('seller/',views.session.seller,name="seller"),
]