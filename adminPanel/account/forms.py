from django.forms import ModelForm
from models import HotelUser


class HotelUserForm(ModelForm):

    class Meta:
        model = HotelUser
        fields = ['hotel_id', 'hotel_name']
