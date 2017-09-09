from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render, render_to_response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template import Context, Template, RequestContext
from vanilla import CreateView, UpdateView, ListView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
# from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, reverse
from models import HotelUser
from forms import HotelUserForm
from django.views.generic import View
from inventory.models import HotelPredefinedProducts
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    """
    This functionality is used for rendering the login page
    """
    print request.method
    return render(request, template_name='account/index.html')


class LoginView(CreateView):

    def get(self, request, *args, **kwargs):
        """
        This functionality is used for rendering the login page
        """
        return render(request, template_name='account/index.html')

    #@method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        """
        This functionality is used for logging the user in.
        On successful login it redirects to baseinventory_list.html
        """
        login_id = request.POST.get("login_id")
        password = request.POST.get("password")
        user = authenticate(login_id=login_id, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
            return HttpResponseRedirect(reverse('inventory:list_inventory'))
        else:
            return render(request, template_name='account/index.html')


@method_decorator(login_required, name='dispatch')
class ListHotels(ListView):
    """
    This functionality is used for listing all the hotel accounts.
    This API is called from base_dashboard.html (side nav bar option)
    """
    model = HotelUser
    def get_queryset(self):
        """
        Returns the base queryset for the view.

        Either used as a list of objects to display, or as the queryset
        from which to perform the individual object lookup.
        """
        if self.queryset is not None:
            return self.queryset._clone()

        if self.model is not None:
            return self.model._default_manager.all().order_by("hotel_name")

        msg = "'%s' must either define 'queryset' or 'model', or override 'get_queryset()'"
        raise ImproperlyConfigured(msg % self.__class__.__name__)


@method_decorator(login_required, name='dispatch')
class CreateHotels(CreateView):
    lookup_field = 'hotel_id'
    model = HotelUser

    def post(self, request, *args, **kwargs):
        """
        This functionality is used for creating a new hotel account.
        This API is called from hoteluser_list.html --> account/create_hoteluser_form.html
        """
        HotelUser.objects.create(hotel_name=request.POST.get("hotel_name"),
                                 contact_person=request.POST.get("contact_person"),
                                 contact_number=request.POST.get("contact_number"),
                                 contact_email=request.POST.get("contact_email"),
                                 hotel_address_line_1=request.POST.get("hotel_address_line_1"),
                                 hotel_address_line_2=request.POST.get("hotel_address_line_2"),
                                 hotel_address_line_3=request.POST.get("hotel_address_line_3")
                                 )

        return HttpResponseRedirect(reverse('account:list_hotels'))


@method_decorator(login_required, name='dispatch')
class EditHotels(UpdateView):
    lookup_field = 'hotel_id'
    model = HotelUser

    def post(self, request, *args, **kwargs):
        """
        This functionality is used for updating details of a specific hotel account.
        This API is called from hoteluser_list.html --> account/update_hoteluser_form.html
        """
        hotel_id = kwargs["hotel_id"]

        # Change hotel name in predefined table when changing the name of hotel
        HotelPredefinedProducts.objects.filter(hotel_id=hotel_id).update(hotel_name=request.POST.get("hotel_name"))

        update_product = HotelUser.objects.get(hotel_id=hotel_id)
        update_product.hotel_name = request.POST.get("hotel_name")
        update_product.contact_person = request.POST.get("contact_person")
        update_product.contact_number = request.POST.get("contact_number")
        update_product.contact_email = request.POST.get("contact_email")
        update_product.hotel_address_line_1 = request.POST.get("hotel_address_line_1")
        update_product.hotel_address_line_2 = request.POST.get("hotel_address_line_2")
        update_product.hotel_address_line_3 = request.POST.get("hotel_address_line_3")
        update_product.save()

        return HttpResponseRedirect(reverse('account:list_hotels'))


class LogoutView(View):

    def get(self, request):
        """
        This functionality is used for logging out the user.
        This API is called from the log out button in the top nav bar.
        """
        logout(request)
        return HttpResponseRedirect(reverse('account:login'))



