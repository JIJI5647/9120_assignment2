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

        if query.strip().lower().startswith("select"):
            results = cursor.fetchall()
        else:
            results = cursor.rowcount
            if results == 0 :
                return {"code": 500, "message": "No effect on database", "data": None}
            conn.commit()
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
    res = executeQuery(f"SELECT UserName, FirstName, LastName FROM SalesPerson WHERE UserName = '{login}' AND Password = '{password}'")
    return res["data"][0] if res["code"] == 200 else None


"""
    Retrieves the summary of car sales.

    This method fetches the summary of car sales from the database and returns it 
    as a collection of summary objects. Each summary contains key information 
    about a particular car sale.

    :return: A list of car sale summaries.
"""
def getCarSalesSummary():
    res = executeQuery("SELECT * FROM CarSalesSummary ORDER BY MakeName, ModelName ASC")
    if res["code"] != 200:
        print("Error fetching car sales summary:", res["message"])
        return []
    return [
    {
        'make': row[0],
        'model': row[1],
        'availableUnits': row[2] or 0,
        'soldUnits': row[3] or 0,
        'soldTotalPrices' : row[4] or 0,
        'lastPurchaseAt': row[5] or '',
    }
    for row in res["data"]
    ]

"""
    Finds car sales based on the provided search string.

    This method searches the database for car sales that match the provided search 
    string. See assignment description for search specification

    :param search_string: The search string to use for finding car sales in the database.
    :return: A list of car sales matching the search string.
"""



def findCarSales(searchString):
    query = f"""
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
            MakeName ILIKE '%{searchString}%' 
            OR ModelName ILIKE '%{searchString}%' 
            OR BuyerName ILIKE '%{searchString}%' 
            OR Salesperson ILIKE '%{searchString}%'
        )
        AND (IsSold = FALSE OR SaleDate > CURRENT_DATE - INTERVAL '3 years')
        ORDER BY IsSold DESC, SaleDate ASC, MakeName, ModelName
        """
    res = executeQuery(query)
    print(res)
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
    for row in res["data"]
    ]




"""
    Adds a new car sale to the database.

    This method accepts a CarSale object, which contains all the necessary details 
    for a new car sale. It inserts the data into the database and returns a confirmation 
    of the operation.

    :param car_sale: The CarSale object to be added to the database.
    :return: A boolean indicating if the operation was successful or not.
"""



def addCarSale(make, model, builtYear, odometer, price):
    
    if int(odometer) < 0 or int(price) <= 0 :
        return False
    
    query_insert = f"""
    INSERT INTO CarSales (MakeCode, ModelCode, BuiltYear, Odometer, Price, IsSold)
    VALUES ('{make}', '{model}', {builtYear}, {odometer}, {price}, FALSE)
    """

    result = executeQuery(query_insert)
    print(result)
    return True if result["code"] == 200 else False

"""
    Updates an existing car sale in the database.

    This method updates the details of a specific car sale in the database, ensuring
    that all fields of the CarSale object are modified correctly. It assumes that 
    the car sale to be updated already exists.

    :param car_sale: The CarSale object containing updated details for the car sale.
    :return: A boolean indicating whether the update was successful or not.
"""

def updateCarSale(carsaleid, customer, salesperson, saledate):
        # open the database and make a connection
    conn = openConnection()
    if not conn:
        print("Error: Database connection failed.")
        return False
    try:
        with conn.cursor() as cursor:
            # Verify whether the CustomerID exists in the Customer table
            cursor.execute("SELECT 1 FROM Customer WHERE CustomerID = %s", (customer,))
            if cursor.fetchone() is None:
                print("Error: Invalid Customer ID.")
                return 

            # Verify whether the Salesperson Username exists in the Salesperson table, with case-insensitive
            cursor.execute("SELECT 1 FROM Salesperson WHERE LOWER(UserName) = LOWER(%s)", (salesperson,))
            if cursor.fetchone() is None:
                print("Error: Invalid Salesperson Username.")
                return "Invalid Salesperson Username"

            # Update the sale record
            cursor.execute("""
                UPDATE CarSales
                SET BuyerID = %s,
                    SalespersonID = (SELECT UserName FROM Salesperson WHERE LOWER(UserName) = LOWER(%s)),
                    SaleDate = %s,
                    IsSold = TRUE
                WHERE CarSaleID = %s
            """, (customer, salesperson, saledate, carsaleid))

            # Commit the transaction to ensure changes have been saved
            conn.commit()
            print("Update successful.")
            return True
    except psycopg2.Error as e:
        # Rollback the transaction on error to prevent data inconsistency
        conn.rollback()
        print("Database error:", e.pgerror)
        return False
    finally:
        # Always close the connection, regardless of errors
        conn.close()

if __name__ == "__main__":
    print(executeQuery("SELECT * FROM CarSalesFormatted"))