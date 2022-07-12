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
    """
    while True:

        print("Please enter sales data from the last market day.")
        print("Data should be eight (8) numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60,70,80\n")

        data_str = input("Enter your data here: ")

        sales_data = data_str.split(',')
        
        if validate_data(sales_data):
            print('Data successfully updated')
            break
    return sales_data    


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
                f"Exactly 8 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True    


data = input_sales_data()
