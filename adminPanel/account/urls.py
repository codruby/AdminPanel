from django.conf.urls import url
from .views import index, LoginView, ListHotels, LogoutView, CreateHotels, EditHotels

urlpatterns = [
    # give $ to end this url other wise, all the url will match with this
    # and you will not be able to see the expected response
    # url(r'^$', index, name='index'),
    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
    url(r'hotels$', ListHotels.as_view(), name='list_hotels'),
    url(r'create_hotel/$', CreateHotels.as_view(), name='create_hotel'),
    url(r'edit_hotel/(?P<hotel_id>[0-9]+)/$', EditHotels.as_view(), name='update_hotel'),

]
