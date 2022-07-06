from django.urls import path
from  .views import HomeView,search,ContactView,find
from . import views
urlpatterns = [
    # path('',views.home,name="home")
    path('', HomeView.as_view(),name='home'),
    path('search/',views.search,name='search'),    
    path('find/',views.find,name='find'), 
    path('contact',ContactView.as_view(),name='contact'),  
    # path('contact',views.contact,name='contact')
]
