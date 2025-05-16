#!/usr/bin/env python3
import psycopg2

#####################################################
##  Database Connection
#####################################################

# ZMJ EDIT ON 2025_5_16
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


'''
Validate salesperson based on username and password
'''
def checkLogin(login, password):
    conn = openConnection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT UserName, FirstName, LastName FROM SalesPerson WHERE LOWER(UserName) = LOWER(%s) AND Password = %s",(login, password))
        res = cursor.fetchall()
        return res[0] if res != [] else None
    except psycopg2.Error as sqle:
        print(psycopg2.Error)
        return None
    


"""
    Retrieves the summary of car sales.

    This method fetches the summary of car sales from the database and returns it 
    as a collection of summary objects. Each summary contains key information 
    about a particular car sale.

    :return: A list of car sale summaries.
"""
def getCarSalesSummary():
    try:
        conn = openConnection()
        if not conn:
            return []
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM CarSalesSummary ORDER BY MakeName, ModelName ASC")
        data = cursor.fetchall()

        if not data:
            return []

        result = []
        for row in data:
            result.append({
                'make': row[0],
                'model': row[1],
                'availableUnits': row[2] or 0,
                'soldUnits': row[3] or 0,
                'soldTotalPrices': row[4] or 0,
                'lastPurchaseAt': row[5] or ''
            })

        return result
    except psycopg2.Error as e:
        print("Database error:", e)
        return []
    finally:
        if conn:
            conn.close()

"""
    Finds car sales based on the provided search string.

    This method searches the database for car sales that match the provided search 
    string. See assignment description for search specification

    :param search_string: The search string to use for finding car sales in the database.
    :return: A list of car sales matching the search string.
"""



def findCarSales(searchString):
    query = """
        SELECT 
            CarSaleID,
            MakeName,
            ModelName,
            BuiltYear,
            Odometer,
            Price,
            IsSold,
            SaleDate_dis,
            BuyerName,
            Salesperson
        FROM CarSalesFormatted
        WHERE (
            MakeName ILIKE '%%' || %s || '%%' 
            OR ModelName ILIKE '%%' || %s || '%%' 
            OR BuyerName ILIKE '%%' || %s || '%%' 
            OR Salesperson ILIKE '%%' || %s || '%%'
        )
        AND (IsSold = FALSE OR SaleDate > CURRENT_DATE - INTERVAL '3 years')
        ORDER BY IsSold DESC, SaleDate ASC, MakeName, ModelName
    """
    params = (searchString, searchString, searchString, searchString)

    try:
        conn = openConnection()
        if not conn:
            return []
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

        return [
            {
                'carsale_id': row[0],
                'make': row[1] or '',
                'model': row[2] or '',
                'builtYear': row[3] if row[3] is not None else 0,
                'odometer': row[4] if row[4] is not None else 0,
                'price': row[5] if row[5] is not None else 0,
                'isSold': row[6],
                'sale_date': row[7] or '',
                'buyer': row[8] or '',
                'salesperson': row[9] or ''
            }
            for row in rows
        ]
    except psycopg2.Error as e:
        print("Database error:", e)
        return []
    finally:
        if conn:
            conn.close()



"""
    Adds a new car sale to the database.

    This method accepts a CarSale object, which contains all the necessary details 
    for a new car sale. It inserts the data into the database and returns a confirmation 
    of the operation.

    :param car_sale: The CarSale object to be added to the database.
    :return: A boolean indicating if the operation was successful or not.
"""



def addCarSale(make, model, builtYear, odometer, price):
    query_insert = "SELECT add_car_sale(%s, %s, %s, %s, %s);"
    params = (make, model, builtYear, odometer, price)

    try:
        conn = openConnection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute(query_insert, params)
        result = cursor.fetchone()
        print(result)
        conn.commit()
        return True if result and result[0] == True else False
    except psycopg2.Error as e:
        print("Database error:", e)
        return False
    finally:
        if conn:
            conn.close()

"""
    Updates an existing car sale in the database.

    This method updates the details of a specific car sale in the database, ensuring
    that all fields of the CarSale object are modified correctly. It assumes that 
    the car sale to be updated already exists.

    :param car_sale: The CarSale object containing updated details for the car sale.
    :return: A boolean indicating whether the update was successful or not.
"""


def updateCarSale(carsaleid, customer, salesperson, saledate):
    query_update = "SELECT update_car_sale(%s, %s, %s, %s);"
    params = (carsaleid, customer, salesperson, saledate)
    try:
        conn = openConnection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute(query_update, params)
        result = cursor.fetchone()
        conn.commit()
        print(result)
        return True if result and result[0] == True else False
    except psycopg2.Error as e:
        print("Database error:", e)
        return False
    finally:
        if conn:
            conn.close()
