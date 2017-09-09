from django.shortcuts import render
from django.utils import timezone
from django.core.urlresolvers import reverse_lazy
from models import BaseInventory, HotelPredefinedProducts, Invoice
from forms import BaseInventoryForm
from vanilla import CreateView, DeleteView, ListView, UpdateView, DetailView, View
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, reverse
from account.models import HotelUser
import json
from collections import OrderedDict
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class ListInventory(ListView):
    """
    For listing base inventory.
    Class will use the model and find file with name model_list.html. It will list all the data from the model
    and add in the template and display.
    """
    model = BaseInventory

    def get_queryset(self):
        """
        Returns the base queryset for the view.

        Either used as a list of objects to display, or as the queryset
        from which to perform the individual object lookup.
        """
        if self.queryset is not None:
            return self.queryset._clone()

        if self.model is not None:
            return self.model._default_manager.all().order_by("product_name")

        msg = "'%s' must either define 'queryset' or 'model', or override 'get_queryset()'"
        raise ImproperlyConfigured(msg % self.__class__.__name__)


@method_decorator(login_required, name='dispatch')
class CreateProductView(CreateView):
    """
    This functionality is used for adding a new product to base inventory.
    This API is called from baseinventory_list.html --> create_form.html and redirects to baseinventory_list.html
    """
    lookup_field = 'inventory_id'
    model = BaseInventory
    form_class = BaseInventoryForm
    template_name = "inventory/create_form.html"

    def post(self, request, *args, **kwargs):
        amount = float(request.POST.get("quantity")) * float(request.POST.get("rate_per_unit"))

        BaseInventory.objects.create(product_name=request.POST.get("product_name"),
                                     quantity=request.POST.get("quantity"),
                                     units=request.POST.get("units"),
                                     rate_per_unit=request.POST.get("rate_per_unit"),
                                     amount=amount
                                     )
        return HttpResponseRedirect(reverse('inventory:list_inventory'))


@method_decorator(login_required, name='dispatch')
class EditProductView(UpdateView):
    """
    This functionality is used for updating the specific product of base inventory.
    This API is called from baseinventory_list.html --> update_form.html and redirects to baseinventory_list.html
    """
    lookup_field = 'inventory_id'
    model = BaseInventory

    def post(self, request, *args, **kwargs):
        inventory_id = kwargs["inventory_id"]
        amount = float(request.POST.get("quantity")) * float(request.POST.get("rate_per_unit"))

        update_product = BaseInventory.objects.get(inventory_id=inventory_id)
        update_product.product_name = request.POST.get("product_name")
        update_product.quantity = request.POST.get("quantity")
        update_product.units = request.POST.get("units")
        update_product.rate_per_unit = request.POST.get("rate_per_unit")
        update_product.amount = amount
        update_product.save()
        return HttpResponseRedirect(reverse('inventory:list_inventory'))


@method_decorator(login_required, name='dispatch')
class DeleteProductView(DeleteView):
    """
    This functionality is used for deleting the specific product of base inventory.
    This API is called from baseinventory_list.html --> update_form.html and redirects to baseinventory_list.html
    """
    lookup_field = 'inventory_id'
    model = BaseInventory

    def get(self, request, *args, **kwargs):
        inventory_id = kwargs["inventory_id"]
        BaseInventory.objects.get(inventory_id=inventory_id).delete()
        return HttpResponseRedirect(reverse('inventory:list_inventory'))


@method_decorator(login_required, name='dispatch')
class HotelDetailView(DetailView):
    """
    This functionality lists a particular hotel's predefined products. Page functionality has features for adding
    and editing predefined products, generating invoice and listing all invoices.
    API is called from hoteluser_list.html. (In account app)
    """
    lookup_field = 'hotel_id'

    def get(self, request, *args, **kwargs):
        hotel_id = kwargs["hotel_id"]
        try:
            hotel_name = HotelUser.objects.get(hotel_id=hotel_id).hotel_name
        except Exception, e:
            hotel_name = ""

        if hotel_name:
            products = HotelPredefinedProducts.objects.filter(hotel_id=hotel_id).order_by('product_name')
            res_list = list()
            for product in products:
                res = OrderedDict()
                res['predefined_id'] = product.predefined_id
                res['product_name'] = product.product_name
                res['quantity'] = product.quantity
                res['units'] = product.units
                res['rate_per_unit'] = product.rate_per_unit
                res['amount'] = product.amount

                res_list.append(res)

            return render(request, 'inventory/hotel_details.html', {"data": res_list, "hotel_name": hotel_name,
                                                                    "hotel_id": hotel_id})


@method_decorator(login_required, name='dispatch')
class CreatePredefinedProductView(CreateView):
    """
    This functionality includes Creating of predefined products from hotel's detail's page.
    API is called from hotel_details.html and redirects to hotel details page.
    """
    lookup_field = 'hotel_id'
    model = HotelPredefinedProducts
    # form_class = BaseInventoryForm
    # template_name = "inventory/create_form.html"

    def post(self, request, *args, **kwargs):
        hotel_id = kwargs["hotel_id"]
        hotel_id_instance = HotelUser.objects.get(hotel_id=hotel_id)
        hotel_name_instance = HotelUser.objects.get(hotel_name=hotel_id_instance.hotel_name)

        inventory_id = BaseInventory.objects.get(product_name=request.POST.get("product_name")).inventory_id
        inventory_id_instance = BaseInventory.objects.get(inventory_id=inventory_id)

        amount = float(request.POST.get("quantity")) * float(inventory_id_instance.rate_per_unit)

        HotelPredefinedProducts.objects.create(hotel_id=hotel_id_instance, hotel_name=hotel_name_instance,
                                               product_id=inventory_id_instance,
                                               product_name=request.POST.get("product_name"),
                                               quantity=request.POST.get("quantity"),
                                               units=request.POST.get("units"),
                                               rate_per_unit=float(inventory_id_instance.rate_per_unit),
                                               amount=amount,
                                               )
        return HttpResponseRedirect(reverse('inventory:hotel_details', kwargs={"hotel_id": hotel_id}))


@method_decorator(login_required, name='dispatch')
class EditPredefinedProductView(UpdateView):
    """
    This functionality includes updating of predefined products from hotel's detail's page.
    API is called from hotel_details.html and redirects to hotel details page.
    """
    lookup_field = 'hotel_id'
    model = HotelPredefinedProducts

    # form_class = BaseInventoryForm
    # template_name = "inventory/create_form.html"

    def post(self, request, *args, **kwargs):
        hotel_id = kwargs["hotel_id"]
        predefined_id = kwargs["predefined_id"]

        inventory_id = BaseInventory.objects.get(product_name=request.POST.get("product_name"))

        amount = float(request.POST.get("quantity")) * float(inventory_id.rate_per_unit)

        update_product = HotelPredefinedProducts.objects.get(hotel_id=hotel_id, predefined_id=predefined_id)
        update_product.product_name = request.POST.get("product_name")
        update_product.quantity = request.POST.get("quantity")
        update_product.units = request.POST.get("units")
        update_product.amount = amount

        update_product.save()

        return HttpResponseRedirect(reverse('inventory:hotel_details', kwargs={"hotel_id": hotel_id}))


@method_decorator(login_required, name='dispatch')
class ListFormForInvoice(ListView):
    """
    This functionality is used to display the invoice items. If the invoice is being created for the first time,
    then predefined products are shown else products from the edited invoice would be shown.
    API is called from hotel_details.html and renders generate_invoice.html
    """

    def get(self, request, *args, **kwargs):
        hotel_id = kwargs['hotel_id']
        print kwargs['invoice_date']
        try:
            hotel_name = HotelUser.objects.get(hotel_id=hotel_id).hotel_name
        except Exception, e:
            hotel_name = ""

        res_list = list()
        if hotel_name:
            invoice_name = hotel_name + "_" + kwargs['invoice_date']
            if Invoice.objects.filter(invoice_name=invoice_name).exists():
                products = Invoice.objects.filter(invoice_name=invoice_name)
                for product in products:
                    res_list = product.invoice_data
                return render(request, 'inventory/generate_invoice.html', {"data": res_list,
                                                                           "hotel_id": hotel_id, "has_invoice": 1})

            else:
                products = HotelPredefinedProducts.objects.filter(hotel_id=hotel_id).order_by('product_name')
                for product in products:
                    res = OrderedDict()
                    res['predefined_id'] = product.predefined_id
                    res['product_name'] = product.product_name
                    res['quantity'] = product.quantity
                    res['units'] = product.units
                    res['rate_per_unit'] = product.rate_per_unit

                    res_list.append(res)

                return render(request, 'inventory/generate_invoice.html', {"data": res_list, "hotel_id": hotel_id,
                                                                           "has_invoice": 0})


@method_decorator(login_required, name='dispatch')
class InvoiceClass(View):

    def get(self, request, *args, **kwargs):
        """
        This functionality lists all invoices for a particular hotel. API call is made from hotel_details.html
        """
        hotel_id = kwargs['hotel_id']
        try:
            hotel_name = HotelUser.objects.get(hotel_id=hotel_id).hotel_name
        except Exception, e:
            hotel_name = ""

        invoices = Invoice.objects.filter(invoice_name__startswith=hotel_name).order_by("-updated_at")
        invoice_list = list()
        for elem in invoices:
            res = OrderedDict()
            res['invoice_name'] = elem.invoice_name
            res['last_modified'] = timezone.localtime(elem.updated_at)

            invoice_list.append(res)
        return render(request, 'inventory/invoice_list.html', {"data": invoice_list, "hotel_id": hotel_id,
                                                               "hotel_name": hotel_name})

    def post(self, request, *args, **kwargs):
        """
        This functionality generates new invoice for current date.User may choose to save invoice temporarily
        or may save and move the final invoice to orders. If the user check save to order option and give a pay date
        then the invoice is saved and downloaded automatically at the moment.
        API is called from hotel_details.html --> generate_invoice.html
        """
        hotel_id = kwargs['hotel_id']
        try:
            hotel_name = HotelUser.objects.get(hotel_id=hotel_id).hotel_name
        except Exception, e:
            hotel_name = ""

        invoice_name = hotel_name + "_" + request.POST.get("invoice_date")

        invoice_data = list()
        dumb_list = []
        for key, value in request.POST.iteritems():
            if "p_name" in key:
                dumb_list.append(str(key).split("-")[1])

        for elem in dumb_list:
            res1 = dict()
            res1['predefined_id'] = elem
            res1['product_name'] = request.POST.get("p_name-" + elem)
            res1['quantity'] = request.POST.get("quantity-" + elem)
            res1['units'] = request.POST.get("units-" + elem)
            res1['rate_per_unit'] = request.POST.get("rate_per_unit-" + elem)
            invoice_data.append(res1)

        # sort invoice data so that it come sorted while listing
        sorted_invoice_data = sorted(invoice_data, key=lambda x: x['product_name'].lower())

        pay_date = None
        # move inside for changing pay date issues for orders

        if "save_checkbox" in request.POST:
            pay_date = request.POST.get("pay_date")
            # import datetime
            # try:
            #     datetime.datetime.strptime(pay_date, '%d-%m-%Y')
            # except ValueError:
            #     raise ValueError("Incorrect data format, should be DD-MM-YYYY")

        # Check whether invoice already exists
        if Invoice.objects.filter(invoice_name=invoice_name).exists():
            e = Invoice.objects.get(invoice_name=invoice_name)
            e.invoice_data = sorted_invoice_data
            e.pay_date = pay_date
            e.save()
        else:
            Invoice.objects.create(invoice_name=invoice_name, invoice_data=sorted_invoice_data, pay_date=pay_date)

        # if "save_checkbox" in request.POST:
        #     # Change here
        #     from utilities.utilities import create_invoice_excel1
        #     import xlsxwriter
        #     from io import BytesIO
        #     import cStringIO as StringIO
        #     output = StringIO.StringIO()
        #
        #     output = create_invoice_excel1()
        #     # path = "/home/divya/workspace/latest/rabbit-project/adminPanel/inventory/sample.xlsx"
        #     # import os
        #     # if os.path.exists(path):
        #     #     with open(path, "rb") as excel:
        #     #         data = excel.read()
        #
        #     response = HttpResponse(output.read(),
        #                             content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        #     response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
        #
        #     return response
        #
        # # send back to generate_invoice.html page only
        # return HttpResponseRedirect(reverse_lazy('inventory:listform_for_invoice',
        #                                          kwargs={'hotel_id': hotel_id,
        #                                                  'invoice_date': request.POST.get("invoice_date")}))
        # return HttpResponseRedirect(reverse_lazy('inventory:hotel_details', kwargs={'hotel_id': hotel_id}))

        if "save_checkbox" in request.POST:
            # Change here
            from utilities.utilities import create_invoice_excel_dynamic
            import xlsxwriter
            from io import BytesIO
            import cStringIO as StringIO
            output = StringIO.StringIO()

            # changes from here
            invoice_product_list = list()
            address_dict = dict()

            for prod in sorted_invoice_data:
                invoice_product_list.append([prod["product_name"], 1, prod["units"], prod["rate_per_unit"],
                                             prod["quantity"], prod["quantity"],
                                             str(float(prod["quantity"]) * float(prod["rate_per_unit"]))])

            # for getting address of the hotel

            hotel_details = HotelUser.objects.get(hotel_id=hotel_id)
            address_dict["hotel_name"] = hotel_details.hotel_name
            address_dict["address_line_1"] = hotel_details.hotel_address_line_1
            address_dict["address_line_2"] = hotel_details.hotel_address_line_2
            address_dict["address_line_3"] = hotel_details.hotel_address_line_3
            address_dict["contact_number"] = hotel_details.contact_number
            address_dict["contact_email"] = hotel_details.contact_email

            output = create_invoice_excel_dynamic(invoice_product_list, address_dict)
            # path = "/home/divya/workspace/latest/rabbit-project/adminPanel/inventory/sample.xlsx"
            # import os
            # if os.path.exists(path):
            #     with open(path, "rb") as excel:
            #         data = excel.read()

            response = HttpResponse(output.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename={}.xlsx'.format(invoice_name.replace(" ", ""))

            return response

            # send back to generate_invoice.html page only
        return HttpResponseRedirect(reverse_lazy('inventory:listform_for_invoice',
                                                 kwargs={'hotel_id': hotel_id,
                                                         'invoice_date': request.POST.get("invoice_date")}))
    # return HttpResponseRedirect(reverse_lazy('inventory:hotel_details', kwargs={'hotel_id': hotel_id}))


@method_decorator(login_required, name='dispatch')
class AddInvoiceProduct(View):

    def post(self, request, *args, **kwargs):
        """
        This functionality is used to add a new product from base inventory to current invoice.
        The add product to invoice button would be enable only if there is an invoice saved for current date, therefore
        first save and invoice then add the product to that invoice.
        API is called from generate_invoice.html --> add_product_to_invoice.html
        """
        hotel_id = kwargs['hotel_id']
        try:
            hotel_name = HotelUser.objects.get(hotel_id=hotel_id).hotel_name
        except Exception, e:
            hotel_name = ""
        invoice_name = hotel_name + "_" + request.POST.get("invoice_date")

        print invoice_name, hotel_name
        print request.POST
        # print request.POST.get("product_name")

        # get the rate per unit from base inventory
        inventory_id_instance = BaseInventory.objects.get(product_name=request.POST.get("product_name"))
        rate_per_unit = inventory_id_instance.rate_per_unit

        # make the dictionary to append to invoice_data
        res = dict()
        res['product_name'] = request.POST.get("product_name")
        res['quantity'] = request.POST.get("quantity")
        res['units'] = request.POST.get("units")
        res['rate_per_unit'] = rate_per_unit
        res['predefined_id'] = None

        # filter the invoice, get the invoice data and append the dictionary and save back
        if Invoice.objects.filter(invoice_name=invoice_name).exists():
            products = Invoice.objects.filter(invoice_name=invoice_name)
            for product in products:
                res_list = product.invoice_data
                res_list.append(res)
                # sort invoice data so that it come sorted while listing
                sorted_invoice_data = sorted(res_list, key=lambda x: x['product_name'].lower())

                Invoice.objects.filter(invoice_name=invoice_name).update(invoice_data=sorted_invoice_data)

        return HttpResponseRedirect(reverse_lazy('inventory:listform_for_invoice',
                                                 kwargs={'hotel_id': hotel_id,
                                                         'invoice_date': request.POST.get("invoice_date")}))


@method_decorator(login_required, name='dispatch')
class DeleteInvoiceProduct(View):

    def post(self, request, *args, **kwargs):
        """
        This functionality is used to delete a  product from the current invoice.
        API is called from generate_invoice.html and renders generate_invoice.html
        """
        hotel_id = kwargs['hotel_id']
        product_name = kwargs['product_name']
        try:
            hotel_name = HotelUser.objects.get(hotel_id=hotel_id).hotel_name
        except Exception, e:
            hotel_name = ""

        if hotel_name:
            invoice_name = hotel_name + "_" + kwargs['invoice_date']
            if Invoice.objects.filter(invoice_name=invoice_name).exists():
                products = Invoice.objects.filter(invoice_name=invoice_name)
                for product in products:
                    res_list = product.invoice_data
                    for i in reversed(range(len(res_list))):
                        if res_list[i].get('product_name') == product_name:
                            res_list.pop(i)

                    # sort invoice data so that it come sorted while listing
                    sorted_invoice_data = sorted(res_list, key=lambda x: x['product_name'].lower())

                    Invoice.objects.filter(invoice_name=invoice_name).update(invoice_data=sorted_invoice_data)

        return HttpResponseRedirect(reverse_lazy('inventory:listform_for_invoice',
                                                 kwargs={'hotel_id': hotel_id,
                                                         'invoice_date': kwargs['invoice_date']}))


def test(request):
    return render(request, 'inventory/test.html')


def return_list(request):
    """
    This functionality is used in search box to fetch query-related products from base inventory. It is used so that
    base inventory products could only be added to hotel's predefined products.
    API is called from hotel_details.html --> create_predefined_products.html(from jquery function)
    """
    print "here"
    query = request.GET.get('q', '')
    if len(query) > 0:
        results = BaseInventory.objects.filter(product_name__icontains=query)
        result_list = []
        for item in results:
            result_list.append(item.product_name)
    else:
        result_list = []
    print result_list
    response_text = json.dumps(result_list, separators=(',', ':'))
    return HttpResponse(response_text, content_type="application/json")


def get_file(request, invoice_name):
    file = "/sample.xlsx"
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = dir_path + file
    # print path
    if os.path.exists(path):
        # print "got the file"
        with open(path, "rb") as excel:
            data = excel.read()

        response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=Report.xlsx'

        return response