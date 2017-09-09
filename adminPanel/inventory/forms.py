from django.forms import ModelForm
from models import BaseInventory


class BaseInventoryForm(ModelForm):

    class Meta:
        model = BaseInventory
        fields = ['product_name', 'quantity', 'rate_per_unit']
