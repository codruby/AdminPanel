# #!/usr/bin/python
import csv
import datetime
from django.db import connection
from django.core.wsgi import get_wsgi_application
from django.contrib.auth.hashers import make_password
import os
import sys
from mailer import mail

from pymongo import MongoClient
from collections import OrderedDict
from dateUtility import calculate_next_date

# sys.path.append('/home/user/workspace/latest_projects/b2b')
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# sys.path.append('/home/user/workspace/latest_projects/b2b/b2b')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ['DJANGO_SETTINGS_MODULE'] = 'adminPanel.settings'
application = get_wsgi_application()

from inventory.models import BaseInventory, Invoice, HotelPredefinedProducts
from account.models import RabbitUser, HotelUser


def create_hotel_account():
    with open('HotelContactMasterSheet.csv') as file:
        reader = csv.reader(file)
        i = 0
        for row in reader:
            if i == 0:
                i += 1
            else:
                print "Checking for Hotel: ", row[0]
                if HotelUser.objects.filter(login_id=row[9]).exists():
                    print "Hotel Account Already Exists"
                else:
                    hotel_user = HotelUser.objects.create(hotel_name=row[0], contact_person=row[1],
                                                          contact_number=row[2], contact_email=row[3],
                                                          mop=row[4], hotel_address=row[5], hotel_latitude=row[6],
                                                          hotel_longitude=row[7],
                                                          login_id=row[9], login_password=row[10])
                    hotel_user.login_password = make_password(row[10])
                    hotel_user.save()
                    print "New Hotel Account Created for: ", row[0]


def create_user_account():
    with open('user_accounts.csv') as file:
        reader = csv.reader(file)
        i = 0
        for row in reader:
            if i == 0:
                i += 1
            else:
                print "Checking for User: ", row[0]
                if RabbitUser.objects.filter(login_id=row[3]).exists():
                    print "User Account Already Exists"
                else:
                    hotel_user = RabbitUser.objects.create(name=row[0], mobile=row[1],
                                                           email=row[2], login_id=row[3])
                    hotel_user.password = make_password(row[4])
                    hotel_user.save()
                    print "New User Account Created for: ", row[0]


def dump_product_catalog():
    """
    Dump data in base inventory. Dumping all categories in base inventory for all products.
    :return:
    """
    BaseInventory.objects.all().delete()

    # Perform raw sql query in django
    cursor = connection.cursor()
    cursor.execute('''alter sequence base_inventory_inventory_id_seq restart with 1;''')

    with open('testproducts.csv') as file:
        reader = csv.reader(file)
        i = 0
        for row in reader:
            if i == 0:
                i += 1
            else:
                BaseInventory.objects.create(product_name=row[0], instock_unit=row[1], price=row[2])


def create_invoice_excel():
    import xlsxwriter
    print ">>> Generating Invoice File..."
    # invoice_name = "Sham Savera_28-5-2017"
    # invoice = Invoice.objects.filter(invoice_name=invoice_name)
    # for detail in invoice:
    #     invoice_data =  detail.invoice_data
    # print invoice_data
    """
    # initialize a workbook with name
    workbook = xlsxwriter.Workbook('hello.xlsx')
    # add a sheet to the workbook
    worksheet = workbook.add_worksheet()
    # merger cells, input= cell range to merge, what to write in merged cells
    # we can also give format of merged cells to change font, colours etc in 3rd parameter
    worksheet.merge_range('A1:E1', '')
    # first we need to merge the cells so that border does not appear and then insert image
    # for inserting image in the given cell,
    # input= cell number/range, image_name, scaling parameters (resizing the image)
    worksheet.merge_range('I1:I3', "")
    worksheet.insert_image('I1:I3', 'abc.png', {'x_scale': 0.09, 'y_scale': 0.09})
    # close workbook
    workbook.close()
    """
    # initialize a workbook with name
    workbook = xlsxwriter.Workbook('sample.xlsx')
    # format = workbook.add_format()
    # format.set_border(0)
    # add a sheet to the workbook
    worksheet = workbook.add_worksheet()

    # for company name
    company_name_size_format = workbook.add_format({"font_size": 16})
    worksheet.merge_range('A1:E1', "", company_name_size_format)
    # for inserting logo
    worksheet.merge_range('I1:I3', "")
    worksheet.insert_image('I1:I3', '', {'x_scale': 0.09, 'y_scale': 0.09})
    # for company address
    company_address_size_format = workbook.add_format({"font_size": 9})
    worksheet.merge_range('A2:B2', "", company_address_size_format)
    worksheet.merge_range('A3:B3', "", company_address_size_format)
    worksheet.merge_range('A4:B4', "", company_address_size_format)
    worksheet.merge_range('A5:B5', "", company_address_size_format)

    # invoice details block
    invoice_detail_format_1 = workbook.add_format({"font_size": 9, "bold": True, "bg_color": "silver", "border": 1})
    invoice_detail_format_2 = workbook.add_format({"font_size": 10, "border": 1})
    # 1st line
    worksheet.merge_range('G4:H4', "INVOICE #", invoice_detail_format_1)
    worksheet.write('I4', "Date", invoice_detail_format_1)
    # 2nd line
    worksheet.merge_range('G5:H5', "12345678", invoice_detail_format_2)
    worksheet.write('I5', "28-May-2017", invoice_detail_format_2)
    # 3rd  line
    worksheet.merge_range('G6:H6', "CUSTOMER ID", invoice_detail_format_1)
    worksheet.write('I6', "TERMS", invoice_detail_format_1)
    # 4th line
    worksheet.merge_range('G7:H7', "", invoice_detail_format_2)
    worksheet.write('I7', "Cash & Carry", invoice_detail_format_2)
    # 5th line
    worksheet.merge_range('G8:I8', "SHIP TO", invoice_detail_format_1)

    # Bill to header line
    worksheet.merge_range('A8:C8', "BILL TO", invoice_detail_format_1)

    # bill to and ship to blocks
    bill_to_ship_to_format_1 = workbook.add_format({"font_size": 10})
    bill_to_ship_to_format_2 = workbook.add_format({"font_size": 11})

    # line 1 -- Hotel Name
    worksheet.merge_range('A9:C9', "Hotel Name", bill_to_ship_to_format_1)
    worksheet.merge_range('G9:I9', "Hotel Name", bill_to_ship_to_format_1)
    # line 2 -- address line 1
    worksheet.merge_range('A10:C10', "Address line 1", bill_to_ship_to_format_2)
    worksheet.merge_range('G10:I10', "Address line 1", bill_to_ship_to_format_2)
    # line 3 -- address line 2
    worksheet.merge_range('A11:C11', "Address line 2", bill_to_ship_to_format_2)
    worksheet.merge_range('G11:I11', "Address line 2", bill_to_ship_to_format_2)
    # line 4 -- address line 3
    worksheet.merge_range('A12:C12', "Address line 3", bill_to_ship_to_format_2)
    worksheet.merge_range('G12:I12', "Address line 3", bill_to_ship_to_format_2)
    # line 5 -- mobile number
    worksheet.merge_range('A13:C13', "Mobile Number", bill_to_ship_to_format_2)
    worksheet.merge_range('G13:I13', "Mobile Number", bill_to_ship_to_format_2)
    # line 6 -- email
    worksheet.merge_range('A14:C14', "Email", bill_to_ship_to_format_2)
    worksheet.merge_range('G14:I14', "Email", bill_to_ship_to_format_2)
    # Black line
    worksheet.merge_range('A15:I15', "")

    # ###Invoice Starts Main Block ###

    # Invoice Header
    invoice_header_format = workbook.add_format({"bold": True, "font_size": 11, "bg_color": "silver", "border": 1})
    worksheet.write('A16', "S. No.", invoice_header_format)
    worksheet.write('B16', "Product Name", invoice_header_format)
    worksheet.write('C16', "Quantity", invoice_header_format)
    worksheet.write('D16', "Unit", invoice_header_format)
    worksheet.write('E16', "Price/Unit", invoice_header_format)
    worksheet.write('F16', "Order Quantity", invoice_header_format)
    worksheet.write('G16', "Delivered Quantity", invoice_header_format)
    worksheet.write('H16', "Order Price", invoice_header_format)
    worksheet.write('I16', "Extra Qty", invoice_header_format)

    # Invoice Products, we need to populate invoice products now
    product_list = [["Maidha (Lime)", "1", "Kgs", "24", "100", "100", "2400"],
                    ["Maidha (Sweet)", "1", "Kgs", "24", "100", "100", "2400"],
                    ["Basmati XXXL", "1", "Kgs", "24", "100", "100", "2400"]]
    row = 17
    i = 1
    invoice_product_format = workbook.add_format({"font_size": 11, "border": 1, "align": "center"})
    for product in product_list:
        worksheet.write('A'+str(row), i, invoice_product_format)
        worksheet.write('B' + str(row), product[0], invoice_product_format)
        worksheet.write('C' + str(row), product[1], invoice_product_format)
        worksheet.write('D' + str(row), product[2], invoice_product_format)
        worksheet.write('E' + str(row), product[3], invoice_product_format)
        worksheet.write('F' + str(row), product[4], invoice_product_format)
        worksheet.write('G' + str(row), product[5], invoice_product_format)
        worksheet.write('H' + str(row), product[6], invoice_product_format)
        worksheet.write('I' + str(row), "", invoice_product_format)
        row += 1
        i += 1

    # after invoice products
    worksheet.merge_range('A{}:E{}'.format(str(row), str(row)), "", invoice_product_format)
    worksheet.merge_range('A{}:F{}'.format(str(row), str(row)), "", invoice_product_format)
    worksheet.merge_range('A{}:G{}'.format(str(row), str(row)), "", invoice_product_format)
    worksheet.merge_range('A{}:H{}'.format(str(row), str(row)), "", invoice_product_format)
    worksheet.merge_range('A{}:I{}'.format(str(row), str(row)), "", invoice_product_format)
    row += 1
    invoice_value_format = workbook.add_format({"font_size": 11, "border": 1, "bold": True})
    worksheet.merge_range('A{}:E{}'.format(str(row), str(row)), "Thank You For Business!", invoice_product_format)
    worksheet.merge_range('G{}:H{}'.format(str(row), str(row)), "Total", invoice_value_format)
    worksheet.write('I' + str(row), "45454545", invoice_value_format)

    # End block
    queries_section_format = workbook.add_format({"font_size": 10, "align": "center"})
    row += 1
    worksheet.merge_range('A{}:I{}'.format(str(row), str(row)), "")
    row += 1
    worksheet.merge_range('A{}:I{}'.format(str(row), str(row)), "")
    row += 1
    worksheet.merge_range('A{}:I{}'.format(str(row), str(row)),
                          "If you have any questions about this invoice, please contact", queries_section_format)
    row += 1
    worksheet.merge_range('A{}:I{}'.format(str(row), str(row)),
                          "", queries_section_format)

    # close workbook
    workbook.close()


def create_invoice_excel1():
    import xlsxwriter
    import cStringIO as StringIO
    from io import BytesIO
    print ">>> Generating Invoice File..."

    output = StringIO.StringIO()
    # initialize a workbook with name
    workbook = xlsxwriter.Workbook(output)
    # format = workbook.add_format()
    # format.set_border(0)
    # add a sheet to the workbook
    worksheet = workbook.add_worksheet()

    # for company name
    company_name_size_format = workbook.add_format({"font_size": 16})
    worksheet.merge_range('A1:E1', "", company_name_size_format)
    # for inserting logo
    image_file = open("", "rb")
    image_data = BytesIO(image_file.read())
    image_file.close()
    worksheet.merge_range('I1:I3', "")
    worksheet.insert_image('I1:I3', '', {"image_data": image_data, 'x_scale': 0.09, 'y_scale': 0.09})

    # for company address
    company_address_size_format = workbook.add_format({"font_size": 9})
    worksheet.merge_range('A2:B2', "", company_address_size_format)
    worksheet.merge_range('A3:B3', "", company_address_size_format)
    worksheet.merge_range('A4:B4', "", company_address_size_format)
    worksheet.merge_range('A5:B5', "", company_address_size_format)

    # invoice details block
    invoice_detail_format_1 = workbook.add_format({"font_size": 9, "bold": True, "bg_color": "silver", "border": 1})
    invoice_detail_format_2 = workbook.add_format({"font_size": 10, "border": 1})
    # 1st line
    worksheet.merge_range('G4:H4', "INVOICE #", invoice_detail_format_1)
    worksheet.write('I4', "Date", invoice_detail_format_1)
    # 2nd line
    worksheet.merge_range('G5:H5', "12345678", invoice_detail_format_2)
    worksheet.write('I5', "28-May-2017", invoice_detail_format_2)
    # 3rd  line
    worksheet.merge_range('G6:H6', "CUSTOMER ID", invoice_detail_format_1)
    worksheet.write('I6', "TERMS", invoice_detail_format_1)
    # 4th line
    worksheet.merge_range('G7:H7', "", invoice_detail_format_2)
    worksheet.write('I7', "Cash & Carry", invoice_detail_format_2)
    # 5th line
    worksheet.merge_range('G8:I8', "SHIP TO", invoice_detail_format_1)

    # Bill to header line
    worksheet.merge_range('A8:C8', "BILL TO", invoice_detail_format_1)

    # bill to and ship to blocks
    bill_to_ship_to_format_1 = workbook.add_format({"font_size": 10})
    bill_to_ship_to_format_2 = workbook.add_format({"font_size": 11})

    # line 1 -- Hotel Name
    worksheet.merge_range('A9:C9', "Hotel Name", bill_to_ship_to_format_1)
    worksheet.merge_range('G9:I9', "Hotel Name", bill_to_ship_to_format_1)
    # line 2 -- address line 1
    worksheet.merge_range('A10:C10', "Address line 1", bill_to_ship_to_format_2)
    worksheet.merge_range('G10:I10', "Address line 1", bill_to_ship_to_format_2)
    # line 3 -- address line 2
    worksheet.merge_range('A11:C11', "Address line 2", bill_to_ship_to_format_2)
    worksheet.merge_range('G11:I11', "Address line 2", bill_to_ship_to_format_2)
    # line 4 -- address line 3
    worksheet.merge_range('A12:C12', "Address line 3", bill_to_ship_to_format_2)
    worksheet.merge_range('G12:I12', "Address line 3", bill_to_ship_to_format_2)
    # line 5 -- mobile number
    worksheet.merge_range('A13:C13', "Mobile Number", bill_to_ship_to_format_2)
    worksheet.merge_range('G13:I13', "Mobile Number", bill_to_ship_to_format_2)
    # line 6 -- email
    worksheet.merge_range('A14:C14', "Email", bill_to_ship_to_format_2)
    worksheet.merge_range('G14:I14', "Email", bill_to_ship_to_format_2)
    # Black line
    worksheet.merge_range('A15:I15', "")

    # ###Invoice Starts Main Block ###

    # Invoice Header
    invoice_header_format = workbook.add_format({"bold": True, "font_size": 11, "bg_color": "silver", "border": 1})
    worksheet.write('A16', "S. No.", invoice_header_format)
    worksheet.write('B16', "Product Name", invoice_header_format)
    worksheet.write('C16', "Quantity", invoice_header_format)
    worksheet.write('D16', "Unit", invoice_header_format)
    worksheet.write('E16', "Price/Unit", invoice_header_format)
    worksheet.write('F16', "Order Quantity", invoice_header_format)
    worksheet.write('G16', "Delivered Quantity", invoice_header_format)
    worksheet.write('H16', "Order Price", invoice_header_format)
    worksheet.write('I16', "Extra Qty", invoice_header_format)

    # Invoice Products, we need to populate invoice products now
    product_list = [["Maidha (Lime)", "1", "Kgs", "24", "100", "100", "2400"],
                    ["Maidha (Sweet)", "1", "Kgs", "24", "100", "100", "2400"],
                    ["Basmati XXXL", "1", "Kgs", "24", "100", "100", "2400"]]
    row = 17
    i = 1
    invoice_product_format = workbook.add_format({"font_size": 11, "border": 1, "align": "center"})
    for product in product_list:
        worksheet.write('A'+str(row), i, invoice_product_format)
        worksheet.write('B' + str(row), product[0], invoice_product_format)
        worksheet.write('C' + str(row), product[1], invoice_product_format)
        worksheet.write('D' + str(row), product[2], invoice_product_format)
        worksheet.write('E' + str(row), product[3], invoice_product_format)
        worksheet.write('F' + str(row), product[4], invoice_product_format)
        worksheet.write('G' + str(row), product[5], invoice_product_format)
        worksheet.write('H' + str(row), product[6], invoice_product_format)
        worksheet.write('I' + str(row), "", invoice_product_format)
        row += 1
        i += 1

    # after invoice products
    worksheet.merge_range('A{}:E{}'.format(str(row), str(row)), "", invoice_product_format)
    worksheet.merge_range('A{}:F{}'.format(str(row), str(row)), "", invoice_product_format)
    worksheet.merge_range('A{}:G{}'.format(str(row), str(row)), "", invoice_product_format)
    worksheet.merge_range('A{}:H{}'.format(str(row), str(row)), "", invoice_product_format)
    worksheet.merge_range('A{}:I{}'.format(str(row), str(row)), "", invoice_product_format)
    row += 1
    invoice_value_format = workbook.add_format({"font_size": 11, "border": 1, "bold": True})
    worksheet.merge_range('A{}:E{}'.format(str(row), str(row)), "Thank You For Business!", invoice_product_format)
    worksheet.merge_range('G{}:H{}'.format(str(row), str(row)), "Total", invoice_value_format)
    worksheet.write('I' + str(row), "45454545", invoice_value_format)

    # End block
    queries_section_format = workbook.add_format({"font_size": 10, "align": "center"})
    row += 1
    worksheet.merge_range('A{}:I{}'.format(str(row), str(row)), "")
    row += 1
    worksheet.merge_range('A{}:I{}'.format(str(row), str(row)), "")
    row += 1
    worksheet.merge_range('A{}:I{}'.format(str(row), str(row)),
                          "If you have any questions about this invoice, please contact", queries_section_format)
    row += 1
    worksheet.merge_range('A{}:I{}'.format(str(row), str(row)),
                          "", queries_section_format)

    # close workbook
    workbook.close()
    output.seek(0)
    return output


def create_invoice_excel_dynamic(product_list, address_dict):
    import xlsxwriter
    import cStringIO as StringIO
    from io import BytesIO
    print ">>> Generating Invoice File..."

    output = StringIO.StringIO()
    # initialize a workbook with name
    workbook = xlsxwriter.Workbook(output)
    # format = workbook.add_format()
    # format.set_border(0)
    # add a sheet to the workbook
    worksheet = workbook.add_worksheet()

    # for company name
    company_name_size_format = workbook.add_format({"font_size": 16})
    worksheet.merge_range('A1:E1', "", company_name_size_format)
    # for inserting logo
    image_file = open("", "rb")
    # image_file = open("abc.png", "rb")

    image_data = BytesIO(image_file.read())
    image_file.close()
    worksheet.merge_range('I1:I3', "")
    worksheet.insert_image('I1:I3', '', {"image_data": image_data, 'x_scale': 0.09, 'y_scale': 0.09})

    # for company address
    company_address_size_format = workbook.add_format({"font_size": 9})
    worksheet.merge_range('A2:B2', "", company_address_size_format)
    worksheet.merge_range('A3:B3', "", company_address_size_format)
    worksheet.merge_range('A4:B4', "", company_address_size_format)
    worksheet.merge_range('A5:B5', "", company_address_size_format)

    # invoice details block
    invoice_detail_format_1 = workbook.add_format({"font_size": 9, "bold": True, "bg_color": "silver", "border": 1})
    invoice_detail_format_2 = workbook.add_format({"font_size": 10, "border": 1})
    # 1st line
    worksheet.merge_range('G4:H4', "INVOICE #", invoice_detail_format_1)
    worksheet.write('I4', "Date", invoice_detail_format_1)
    # 2nd line
    worksheet.merge_range('G5:H5', "12345678", invoice_detail_format_2)
    worksheet.write('I5', "28-May-2017", invoice_detail_format_2)
    # 3rd  line
    worksheet.merge_range('G6:H6', "CUSTOMER ID", invoice_detail_format_1)
    worksheet.write('I6', "TERMS", invoice_detail_format_1)
    # 4th line
    worksheet.merge_range('G7:H7', "", invoice_detail_format_2)
    worksheet.write('I7', "Cash & Carry", invoice_detail_format_2)
    # 5th line
    worksheet.merge_range('G8:I8', "SHIP TO", invoice_detail_format_1)

    # Bill to header line
    worksheet.merge_range('A8:C8', "BILL TO", invoice_detail_format_1)

    # bill to and ship to blocks
    bill_to_ship_to_format_1 = workbook.add_format({"font_size": 10})
    bill_to_ship_to_format_2 = workbook.add_format({"font_size": 11, "align": "left"})

    # for dynamic invoice creation we will use the address dict
    # line 1 -- Hotel Name
    worksheet.merge_range('A9:C9', address_dict["hotel_name"], bill_to_ship_to_format_1)
    worksheet.merge_range('G9:I9', address_dict["hotel_name"], bill_to_ship_to_format_1)
    # line 2 -- address line 1
    worksheet.merge_range('A10:C10', address_dict["address_line_1"], bill_to_ship_to_format_2)
    worksheet.merge_range('G10:I10', address_dict["address_line_1"], bill_to_ship_to_format_2)
    # line 3 -- address line 2
    worksheet.merge_range('A11:C11', address_dict["address_line_2"], bill_to_ship_to_format_2)
    worksheet.merge_range('G11:I11', address_dict["address_line_2"], bill_to_ship_to_format_2)
    # line 4 -- address line 3
    worksheet.merge_range('A12:C12', address_dict["address_line_3"], bill_to_ship_to_format_2)
    worksheet.merge_range('G12:I12', address_dict["address_line_3"], bill_to_ship_to_format_2)
    # line 5 -- mobile number
    worksheet.merge_range('A13:C13', address_dict["contact_number"], bill_to_ship_to_format_2)
    worksheet.merge_range('G13:I13', address_dict["contact_number"], bill_to_ship_to_format_2)
    # line 6 -- email
    worksheet.merge_range('A14:C14', address_dict["contact_email"], bill_to_ship_to_format_2)
    worksheet.merge_range('G14:I14', address_dict["contact_email"], bill_to_ship_to_format_2)

    # Black line
    worksheet.merge_range('A15:I15', "")

    # ###Invoice Starts Main Block ###

    # Invoice Header
    invoice_header_format = workbook.add_format({"bold": True, "font_size": 11, "bg_color": "silver", "border": 1})
    worksheet.write('A16', "S. No.", invoice_header_format)
    worksheet.write('B16', "Product Name", invoice_header_format)
    worksheet.write('C16', "Quantity", invoice_header_format)
    worksheet.write('D16', "Unit", invoice_header_format)
    worksheet.write('E16', "Price/Unit", invoice_header_format)
    worksheet.write('F16', "Order Quantity", invoice_header_format)
    worksheet.write('G16', "Delivered Quantity", invoice_header_format)
    worksheet.write('H16', "Order Price", invoice_header_format)
    worksheet.write('I16', "Extra Qty", invoice_header_format)

    # Invoice Products, we need to populate invoice products now
    # product_list = [["Maidha (Lime)", "1", "Kgs", "24", "100", "100", "2400"],
    #                 ["Maidha (Sweet)", "1", "Kgs", "24", "100", "100", "2400"],
    #                 ["Basmati XXXL", "1", "Kgs", "24", "100", "100", "2400"]]
    row = 17
    i = 1
    invoice_product_format = workbook.add_format({"font_size": 11, "border": 1, "align": "center"})
    total_price = 0
    for product in product_list:
        total_price += float(product[6])
        worksheet.write('A'+str(row), i, invoice_product_format)
        worksheet.write('B' + str(row), product[0], invoice_product_format)
        worksheet.write('C' + str(row), product[1], invoice_product_format)
        worksheet.write('D' + str(row), product[2], invoice_product_format)
        worksheet.write('E' + str(row), product[3], invoice_product_format)
        worksheet.write('F' + str(row), product[4], invoice_product_format)
        worksheet.write('G' + str(row), product[5], invoice_product_format)
        worksheet.write('H' + str(row), product[6], invoice_product_format)
        worksheet.write('I' + str(row), "", invoice_product_format)
        row += 1
        i += 1

    # after invoice products
    worksheet.merge_range('A{}:E{}'.format(str(row), str(row)), "", invoice_product_format)
    worksheet.merge_range('A{}:F{}'.format(str(row), str(row)), "", invoice_product_format)
    worksheet.merge_range('A{}:G{}'.format(str(row), str(row)), "", invoice_product_format)
    worksheet.merge_range('A{}:H{}'.format(str(row), str(row)), "", invoice_product_format)
    worksheet.merge_range('A{}:I{}'.format(str(row), str(row)), "", invoice_product_format)
    row += 1
    invoice_value_format = workbook.add_format({"font_size": 11, "border": 1, "bold": True})
    worksheet.merge_range('A{}:E{}'.format(str(row), str(row)), "Thank You For Business!", invoice_product_format)
    worksheet.merge_range('G{}:H{}'.format(str(row), str(row)), "Total", invoice_value_format)
    worksheet.write('I' + str(row), str(total_price), invoice_value_format)

    # End block
    queries_section_format = workbook.add_format({"font_size": 10, "align": "center"})
    row += 1
    worksheet.merge_range('A{}:I{}'.format(str(row), str(row)), "")
    row += 1
    worksheet.merge_range('A{}:I{}'.format(str(row), str(row)), "")
    row += 1
    worksheet.merge_range('A{}:I{}'.format(str(row), str(row)),
                          "If you have any questions about this invoice, please contact", queries_section_format)
    row += 1
    worksheet.merge_range('A{}:I{}'.format(str(row), str(row)),
                          "", queries_section_format)

    # close workbook
    workbook.close()
    output.seek(0)
    return output


def alert_for_payment():
    invoices = Invoice.objects.all()
    current_date = datetime.datetime.now().date()

    # Send email alert
    """
    Change mail 
    """
    recipient_list = ['mail']
    subject = "Reminder for Collection of Payment from Hotels"
    text = "Hello,<br><br>Kindly collect the payment from below hotels on the respective dates.<br><br>"
    text += '<!DOCTYPE html><html><head><title>HTML Tables</title></head><body><table border="1">' \
            '<tr><th>Hotel Name</th><th>Amount</th>' \
            '<th>Pay Date</th></tr>'

    html = ""
    for invoice in invoices:
        if invoice.pay_date:
            date_object = datetime.datetime.strptime(str(invoice.pay_date), "%d-%m-%Y").strftime("%Y-%m-%d")
            alert_date = datetime.datetime.strptime(str(date_object), "%Y-%m-%d")
            current_date_formatted = datetime.datetime.strptime(str(current_date), "%Y-%m-%d")

            time_diff = (alert_date-current_date_formatted).days
            if time_diff <= 2:
                invoice_name = str(invoice.invoice_name).split("_")
                hotel_name = invoice_name[0]

                amount = 0
                for data in invoice.invoice_data:
                    amount += (float(data["rate_per_unit"]) * float(data["quantity"]))

                html += '<tr><th>{}</th><th>{}</th><th>{}</th></tr>'.format(hotel_name, amount, invoice.pay_date)

    if html:
        text += html
        text += "</table></body></html><br><br>Regards,<br>Technology Team"
        mail(recipient_list, subject, text, "")
        print "Mail sent"
    else:
        print "No due payment coming soon."

if __name__ == "__main__":
    print "I am main function... ha ha ha"

    # Open for creating user (team members) accounts
    create_user_account()

    # Open for creating hotel accounts
    # create_hotel_account()

    # Open for dumping product catalog/ baseinventory
    # dump_product_catalog()

    # Open for making the desired excel invoice file
    # create_invoice_excel()

    # create_invoice_excel_dynamic()
    # alert_for_payment()
