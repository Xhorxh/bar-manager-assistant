"""import PrettyPrinter module"""
from pprint import pprint
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('bar_sales')


def input_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 8 numbers separated
    by commmas. The loop will repeatedly request data, until it is valid.
    """
    while True:
        print('Please enter sales data from the last market day.')
        print('Data should be eight (8) numbers, separated by commas.')
        print('Example: 10,20,30,40,50,60,70,80\n')
        data_str = input('Enter your data here: ')
        sales_data = data_str.split(',')
        if validate_data(sales_data):
            print('Data is valid')
            break
    return sales_data


def input_order_data():
    """
    Get order figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 8 numbers separated
    by commmas. The loop will repeatedly request data, until it is valid.
    """
    while True:
        print('Please enter last order data.')
        print('Data should be eight (8) numbers, separated by commas.')
        print('Example: 10,20,30,40,50,60,70,80\n')
        data_str = input('Enter your data here: ')
        order_data = data_str.split(',')
        if validate_data(order_data):
            print('Data is valid')
            break
    return order_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 8 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 8:
            raise ValueError(
                f'Exactly 8 values required, you provided {len(values)}'
            )
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')
        return False
    return True


def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided.
    """
    print('Updating sales worksheet...\n')
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)


def update_order_worksheet(orders):
    """
    Update order worksheet, add new row with the list data provided.
    """
    print('Updating order worksheet...\n')
    order_worksheet = SHEET.worksheet('order')
    order_worksheet.append_row(orders)


def calculate_stock_after_orders():
    """
    Calculates Stock after inputing orders
    """
    order = SHEET.worksheet('order').get_all_values()
    last_order = order[-1]
    last_order = [int(i) for i in last_order]
    stock = SHEET.worksheet('stock').get_all_values()
    new_stock = stock[-1]
    new_stock = [float(i) for i in new_stock]
    ordered_stock = [sum(i) for i in zip(last_order, new_stock)]
    return ordered_stock


def update_stock_worksheet(ordered_stock):
    """
    This function will delete the existing row form the stock worksheet
    and append the updated row
    """
    print('Updating stock worksheet...\n')
    stock_worksheet = SHEET.worksheet('stock')
    stock_worksheet.delete_rows(2)
    stock_worksheet.append_row(ordered_stock)


def convert_units():
    """
    Takes the last market day sales and converts the sales units in stock
    and order units
    """
    sales = SHEET.worksheet('sales').get_all_values()
    last_sales = sales[-1]
    last_sales = [int(i) for i in last_sales]
    converter = [0.008, 0.266, 0.266, 0.04, 0.04, 0.04, 0.04, 0.04]
    converter = [float(i) for i in converter]
    converted_sales = [i1 * i2 for i1, i2 in zip(last_sales, converter)]
    return converted_sales


def calculate_stock_after_sales():
    """
    Calculates remained stocks after the last market day
    """
    stock = SHEET.worksheet('stock').get_all_values()
    new_stock = stock[-1]
    converted_sales = convert_units()
    new_stock = [float(i) for i in new_stock]
    sold_stocks = [i1 - i2 for i1, i2 in zip(new_stock, converted_sales)]
    return sold_stocks


def update_stocks_worksheet(saled_stock):
    """
    This function will delete the existing row form the stock worksheet
    and append the updated row
    """
    print('Updating stock worksheet...\n')
    stock_worksheet = SHEET.worksheet('stock')
    stock_worksheet.delete_rows(2)
    stock_worksheet.append_row(saled_stock)


def show_stock_worksheet():
    """
    Shows the stock worksheet in the terminal
    """
    print('Showing the Stock worksheet...')
    stock = SHEET.worksheet('stock').get_all_values()
    print(stock)


def show_order_worksheet():
    """
    Shows the order worksheet in the terminal
    """
    print('Showing the Order worksheet...')
    order = SHEET.worksheet('order').get_all_values()
    pprint(order)


def show_sales_worksheet():
    """
    Shows the sales worksheet in the terminal
    """
    print('Showing the Sales worksheet...')
    sales = SHEET.worksheet('sales').get_all_values()
    pprint(sales)


def leave_application():
    """
    Exit the program and displays a thanks message
    """
    print('Thanks for using Bar-Manager assistant')


def selection_one():
    """
    Calls the functions for the first option from the menu
    """
    data = input_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    saled_stock = calculate_stock_after_sales()
    update_stocks_worksheet(saled_stock)
    print('If you would like to do something else choose from the list below:')
    menu()


def selection_two():
    """
    Calls the functions for the second option from the menu
    """
    orders = input_order_data()
    order_data = [int(num) for num in orders]
    update_order_worksheet(order_data)
    ordered_stock = calculate_stock_after_orders()
    update_stock_worksheet(ordered_stock)
    print('If you would like to do something else choose from the list below:')
    menu()


def selection_three():
    """
     Calls the functions for the third option from the menu
    """
    show_stock_worksheet()
    print('If you would like to do something else choose from the list below:')
    menu()


def selection_four():
    """
    Calls the functions for the fourth option from the menu
    """
    show_order_worksheet()
    print('If you would like to do something else choose from the list below:')
    menu()


def selection_five():
    """
    Calls the functions for the fifth option from the menu
    """
    show_sales_worksheet()
    print('If you would like to do something else choose from the list below:')
    menu()


def selection_zero():
    """
    Calls the functions for the last option from the menu
    """
    leave_application()
    print('------------------------------------------------')


def menu():
    """
    Gives the posibility to the user to choose what option to use
    """
    while True:
        try:
            print('1. Input the last market day sales')
            print('2. Input last orders')
            print('3. See the Stock worksheet')
            print('4. See the Order worksheet')
            print('5. See the Sale worksheet')
            print('0. Exit\n')
            selection = int(input('Enter a number from the list above:'))
            if selection == 1:
                selection_one()
                break
            elif selection == 2:
                selection_two()
                break
            elif selection == 3:
                selection_three()
                break
            elif selection == 4:
                selection_four()
                break
            elif selection == 5:
                selection_five()
                break
            elif selection == 0:
                selection_zero()
                break
            else:
                if selection != [0, 1, 2, 3, 4, 5]:
                    raise ValueError('Invalid entry. Enter a number form 0-5')
        except ValueError:
            print('Invalid entry. Enter a number form 0 to 5')
        continue


print('Welcome to Bar-Manager assistant\n')
print('------------------------------------------------')
menu()
