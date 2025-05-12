#!/usr/bin/env python3
import psycopg2

#####################################################
##  Database Connection
#####################################################

def openConnection():
    # connection parameters - ENTER YOUR LOGIN AND PASSWORD HERE

    userid = "y25s1c9120_mzha0323"
    passwd = "zmj20020619"
    myHost = "awsprddbs4836.shared.sydney.edu.au"
    
    # Create a connection to the database
    conn = None
    try:
        # Parses the config file and connects using the connect string
        conn = psycopg2.connect(database=userid,
                                    user=userid,
                                    password=passwd,
                                    host=myHost)

    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)
    
    # return the connection to use
    return conn

def executeQuery(query):
    # Open a connection to the database
    conn = openConnection()
    if not conn: 
        print("Failed to connect to the database.")
        return {"code": 500, "message": "Failed to connect to the database.", "data": None}
    try:
        # Create a cursor object
        cursor = conn.cursor()

        # Execute the query
        cursor.execute(query)

        # Fetch all results
        results = cursor.fetchall()
        return {"code": 200, "message": "Query executed successfully.", "data": results}
    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)
        if conn:
            conn.rollback()
        return {"code": 500, "message": sqle.pgerror, "data": None}


'''
Validate salesperson based on username and password
'''
def checkLogin(login, password):

    return ['jdoe', 'John', 'Doe']


"""
    Retrieves the summary of car sales.

    This method fetches the summary of car sales from the database and returns it 
    as a collection of summary objects. Each summary contains key information 
    about a particular car sale.

    :return: A list of car sale summaries.
"""
def getCarSalesSummary():
    return

"""
    Finds car sales based on the provided search string.

    This method searches the database for car sales that match the provided search 
    string. See assignment description for search specification

    :param search_string: The search string to use for finding car sales in the database.
    :return: A list of car sales matching the search string.
"""



def findCarSales(searchString):
    #A = F"select .. where == {searchString}"
    query = f"""
    SELECT * FROM CarSalesFormatted 
    WHERE (MakeName ILIKE '%{searchString}%' 
           OR ModelName ILIKE '%{searchString}%' 
           OR BuyerID ILIKE '%{searchString}%' 
           OR SalespersonID ILIKE '%{searchString}%')
    AND (IsSold = FALSE OR SaleDate > CURRENT_DATE - INTERVAL '3 years')
    ORDER BY IsSold DESC, SaleDate ASC, MakeName, ModelName
    """
    return executeQuery(query)

"""
    Adds a new car sale to the database.

    This method accepts a CarSale object, which contains all the necessary details 
    for a new car sale. It inserts the data into the database and returns a confirmation 
    of the operation.

    :param car_sale: The CarSale object to be added to the database.
    :return: A boolean indicating if the operation was successful or not.
"""



def addCarSale(make, model, builtYear, odometer, price):
    
    if odometer <= 0 or price <= 0:
        return False
    
    query_check_make = f"SELECT * FROM Make WHERE MakeName = '{make}'"
    make_result = executeQuery(query_check_make)
    if not make_result:
        return False
    
    query_check_make = f"""
    SELECT * FROM Model 
    WHERE ModelName = '{model}' 
    AND MakeCode = (SELECT MakeCode FROM Make WHERE MakeName = '{make}')
    """
    model_result = executeQuery(query_check_make)
    if not model_result:
        return False
    
    query_insert = f"""
    INSERT INTO CarSales (MakeCode, ModelCode, BuiltYear, Odometer, Price, IsSold)
    VALUES ('{make}', '{model}', {builtYear}, {odometer}, {price}, FALSE)
    """
    executeQuery(query_insert)
    return True

"""
    Updates an existing car sale in the database.

    This method updates the details of a specific car sale in the database, ensuring
    that all fields of the CarSale object are modified correctly. It assumes that 
    the car sale to be updated already exists.

    :param car_sale: The CarSale object containing updated details for the car sale.
    :return: A boolean indicating whether the update was successful or not.
"""



def updateCarSale(carsaleid, customer, salesperosn, saledate):
    return

if __name__ == "__main__":
    print(executeQuery("SELECT * FROM CarSalesFormatted"))