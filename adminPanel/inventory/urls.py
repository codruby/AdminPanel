from django.conf.urls import url
from views import ListInventory, EditProductView, DeleteProductView, CreateProductView, HotelDetailView, \
    CreatePredefinedProductView, EditPredefinedProductView, test, return_list, ListFormForInvoice, InvoiceClass, \
    get_file, AddInvoiceProduct, DeleteInvoiceProduct

urlpatterns = [
    # give $ to end this url other wise, all the url will match with this
    # and you will not be able to see the expected response
    url(r'^$', ListInventory.as_view(), name='list_inventory'),
    url(r'^edit/(?P<inventory_id>[0-9]+)/$', EditProductView.as_view(), name='update_product'),
    url(r'^delete/(?P<inventory_id>[0-9]+)/$', DeleteProductView.as_view(), name='delete_product'),
    url(r'^create/$', CreateProductView.as_view(), name='create_product'),

    # Hotel Details
    url(r'hotel_details/(?P<hotel_id>[0-9]+)/$', HotelDetailView.as_view(), name='hotel_details'),
    # create predefined product
    url(r'^create_predefined/(?P<hotel_id>[0-9]+)/$', CreatePredefinedProductView.as_view(), name='create_pre_product'),
    # update predefined product
    url(r'^update_predefined/(?P<hotel_id>[0-9]+)/(?P<predefined_id>[0-9]+)/$', EditPredefinedProductView.as_view(),
        name='update_pre_product'),
    # list invoice products
    url(r'^generate_invoice/(?P<hotel_id>[0-9]+)/(?P<invoice_date>[-0-9]+)$', ListFormForInvoice.as_view(), name='listform_for_invoice'),
    # get invoice list + update invoice products
    url(r'^invoice/(?P<hotel_id>[0-9]+)$', InvoiceClass.as_view(), name='invoice'),
    # add product to invoice
    url(r'^add_product_invoice/(?P<hotel_id>[0-9]+)/$', AddInvoiceProduct.as_view(), name='add_product_invoice'),
    # delete invoice products (allow everything in product_name regex using .+)
    url(r'^delete_product_invoice/(?P<hotel_id>[0-9]+)/(?P<invoice_date>[-0-9]+)/(?P<product_name>.+)/$',
        DeleteInvoiceProduct.as_view(), name='delete_product_invoice'),

    # Return the products based on query.
    url(r'return_list/$', return_list, name="return_list"),
    url(r'test$', test, name="test"),

    # download file request
    url(r'get_file/(?P<invoice_name>[a-zA-Z0-9-_ ]+)$', get_file, name="get_file"),

]