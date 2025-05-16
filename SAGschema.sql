DROP TABLE IF EXISTS Make CASCADE;
DROP TABLE IF EXISTS Model CASCADE;
DROP TABLE IF EXISTS Salesperson CASCADE;
DROP TABLE IF EXISTS Customer CASCADE;
DROP TABLE IF EXISTS CarSales CASCADE;

CREATE TABLE Salesperson (
    UserName VARCHAR(10) PRIMARY KEY,
    Password VARCHAR(20) NOT NULL,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
	UNIQUE(FirstName, LastName)
);

INSERT INTO Salesperson VALUES 
('jdoe', 'Pass1234', 'John', 'Doe'),
('brown', 'Passwxyz', 'Bob', 'Brown'),
('ksmith1', 'Pass5566', 'Karen', 'Smith');

CREATE TABLE Customer (
    CustomerID VARCHAR(10) PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Mobile VARCHAR(20) NOT NULL
);

INSERT INTO Customer VALUES 
('c001', 'David', 'Wilson', '4455667788'),
('c899', 'Eva', 'Taylor', '5566778899'),
('c199',  'Frank', 'Anderson', '6677889900'),
('c910', 'Grace', 'Thomas', '7788990011'),
('c002',  'Stan', 'Martinez', '8899001122'),
('c233', 'Laura', 'Roberts', '9900112233'),
('c123', 'Charlie', 'Davis', '7712340011'),
('c321', 'Jane', 'Smith', '9988990011'),
('c211', 'Alice', 'Johnson', '7712222221');

CREATE TABLE Make (
    MakeCode VARCHAR(5) PRIMARY KEY,
    MakeName VARCHAR(20) UNIQUE NOT NULL
);

INSERT INTO Make VALUES ('MB', 'Mercedes Benz');
INSERT INTO Make VALUES ('TOY', 'Toyota');
INSERT INTO Make VALUES ('VW', 'Volkswagen');
INSERT INTO Make VALUES ('LEX', 'Lexus');
INSERT INTO Make VALUES ('LR', 'Land Rover');

CREATE TABLE Model (
    ModelCode VARCHAR(10) PRIMARY KEY,
    ModelName VARCHAR(20) UNIQUE NOT NULL,
    MakeCode VARCHAR(10) NOT NULL,  
    FOREIGN KEY (MakeCode) REFERENCES Make(MakeCode)
);

INSERT INTO Model (ModelCode, ModelName, MakeCode) VALUES
('aclass', 'A Class', 'MB'),
('cclass', 'C Class', 'MB'),
('eclass', 'E Class', 'MB'),
('camry', 'Camry', 'TOY'),
('corolla', 'Corolla', 'TOY'),
('rav4', 'RAV4', 'TOY'),
('defender', 'Defender', 'LR'),
('rangerover', 'Range Rover', 'LR'),
('discosport', 'Discovery Sport', 'LR'),
('golf', 'Golf', 'VW'),
('passat', 'Passat', 'VW'),
('troc', 'T Roc', 'VW'),
('ux', 'UX', 'LEX'),
('gx', 'GX', 'LEX'),
('nx', 'NX', 'LEX');

CREATE TABLE CarSales (
  CarSaleID SERIAL primary key,
  MakeCode VARCHAR(10) NOT NULL REFERENCES Make(MakeCode),
  ModelCode VARCHAR(10) NOT NULL REFERENCES Model(ModelCode),
  BuiltYear INTEGER NOT NULL CHECK (BuiltYear BETWEEN 1950 AND EXTRACT(YEAR FROM CURRENT_DATE)),
  Odometer INTEGER NOT NULL,
  Price Decimal(10,2) NOT NULL,
  IsSold Boolean NOT NULL,
  BuyerID VARCHAR(10) REFERENCES Customer,
  SalespersonID VARCHAR(10) REFERENCES Salesperson,
  SaleDate Date
);

INSERT INTO CarSales (
    MakeCode, ModelCode, BuiltYear, Odometer, Price, IsSold,
    BuyerID, SalespersonID, SaleDate
) VALUES
('MB', 'cclass', 2020, 64210, 72000.00, TRUE, 'c001', 'jdoe', TO_DATE('01/03/2024', 'DD/MM/YYYY')),
('MB', 'eclass', 2019, 31210, 89000.00, FALSE, NULL, NULL, NULL),
('TOY', 'camry', 2021, 98200, 37200.00, TRUE, 'c123', 'brown', TO_DATE('07/12/2023', 'DD/MM/YYYY')),
('TOY', 'corolla', 2022, 65000, 35000.00, TRUE, 'c910', 'jdoe', TO_DATE('21/09/2024', 'DD/MM/YYYY')),
('LR', 'defender', 2018, 115000, 97000.00, FALSE, NULL, NULL, NULL),
('VW', 'golf', 2023, 22000, 33000.00, TRUE, 'c233', 'jdoe', TO_DATE('06/11/2023', 'DD/MM/YYYY')),
('LEX', 'nx', 2020, 67000, 79000.00, TRUE, 'c321', 'brown', TO_DATE('01/01/2025', 'DD/MM/YYYY')),
('LR', 'discosport', 2021, 43080, 85000.00, TRUE, 'c211', 'ksmith1', TO_DATE('27/01/2021', 'DD/MM/YYYY')),
('TOY', 'rav4', 2019, 92900, 48000.00, FALSE, NULL, NULL, NULL),
('MB', 'aclass', 2022, 47000, 57000.00, TRUE, 'c199', 'jdoe', TO_DATE('01/03/2025', 'DD/MM/YYYY')),
('LEX', 'ux', 2023, 23000, 70000.00, TRUE, 'c899', 'brown', TO_DATE('01/01/2023', 'DD/MM/YYYY')),
('VW', 'passat', 2020, 63720, 42000.00, FALSE, NULL, NULL, NULL),
('MB', 'eclass', 2021, 12000, 155000.00, TRUE, 'c002', 'ksmith1', TO_DATE('01/10/2024', 'DD/MM/YYYY')),
('LR', 'rangerover', 2017, 60000, 128000.00, FALSE, NULL, NULL, NULL),
('TOY', 'camry', 2025, 10, 49995.00, FALSE, NULL, NULL, NULL),
('LR', 'discosport', 2022, 53000, 89900.00, FALSE, NULL, NULL, NULL),
('MB', 'cclass', 2023, 55000, 82100.00, FALSE, NULL, NULL, NULL),
('MB', 'aclass', 2025, 5, 78000.00, FALSE, NULL, NULL, NULL),
('MB', 'aclass', 2015, 8912, 12000.00, TRUE, 'c199', 'jdoe', TO_DATE('11/03/2020', 'DD/MM/YYYY')),
('TOY', 'camry', 2024, 21000, 42000.00, FALSE, NULL, NULL, NULL),
('LEX', 'gx', 2025, 6, 128085.00, FALSE, NULL, NULL, NULL),
('MB', 'eclass', 2019, 99220, 105000.00, FALSE, NULL, NULL, NULL),
('VW', 'golf', 2023, 53849, 43000.00, FALSE, NULL, NULL, NULL),
('MB', 'cclass', 2022, 89200, 62000.00, FALSE, NULL, NULL, NULL);

CREATE VIEW CarSalesFormatted AS
SELECT
	CarSaleID,
	ma.MakeName,
	mo.ModelName,
	BuiltYear,
	Odometer,
	Price,
	IsSold,
	SaleDate,
	TO_CHAR(SaleDate, 'DD-MM-YYYY') AS SaleDate_dis,
	c.FirstName || ' ' || c.LastName AS BuyerName,
	sp.FirstName || ' ' || sp.LastName AS Salesperson
FROM CarSales cs 
LEFT JOIN MAKE ma ON cs.MakeCode = ma.MakeCode
LEFT JOIN MODEL mo ON cs.ModelCode = mo.ModelCode
LEFT JOIN Customer c ON cs.BuyerID = c.CustomerID
LEFT JOIN Salesperson sp ON cs.SalespersonID = sp.UserName;

CREATE VIEW AvailableUnits AS
SELECT 
    MakeCode,
    ModelCode,
    count(*) AS AvailableUnit
FROM CarSales
WHERE IsSold = FALSE
GROUP BY MakeCode, ModelCode;


CREATE VIEW SoldUnits AS 
SELECT 
    MakeCode,
    ModelCode,
    count(*) AS SoldUnit,
	sum(Price) AS totalSales,
	TO_CHAR(max(SaleDate), 'DD-MM-YYYY') AS LastPurchase
FROM CarSales
WHERE IsSold = TRUE
GROUP BY MakeCode, ModelCode;

CREATE VIEW CarSalesSummary AS
SELECT
    mk.MakeName,
    mo.ModelName,
    au.AvailableUnit,
    su.SoldUnit,
    su.totalSales AS TotalSales,
    su.LastPurchase
FROM 
    Model mo
    JOIN Make mk ON mo.MakeCode = mk.MakeCode
    LEFT JOIN AvailableUnits au ON mo.ModelCode = au.ModelCode AND mo.MakeCode = au.MakeCode
    LEFT JOIN SoldUnits su ON mo.ModelCode = su.ModelCode AND mo.MakeCode = su.MakeCode;


DROP FUNCTION if EXISTS check_new_car CASCADE;

CREATE FUNCTION check_new_car() RETURNS trigger AS $$
BEGIN
	IF NEW.odometer < 0 THEN
		RAISE EXCEPTION 'Odometer cannot be negative!';
	END IF;
	
	IF NEW.PRICE < 0 THEN
		RAISE EXCEPTION 'Price cannot be negative!';
	END IF;
	
	RETURN NEW;
	
END; $$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS insert_car_trigger ON CarSales;
CREATE TRIGGER insert_car_trigger BEFORE INSERT ON CarSales
FOR EACH ROW EXECUTE FUNCTION check_new_car();

DROP FUNCTION IF EXISTS update_car CASCADE;
CREATE FUNCTION update_car() RETURNS trigger AS $$ 
BEGIN
	IF NEW.SALEDATE IS NULL OR NEW.SALEDATE > CURRENT_DATE THEN 
		RAISE EXCEPTION 'SaleDate ERROR!';
	END IF;
	
	IF NEW.BuyerID IS NULL OR NOT EXISTS(
		SELECT 1 FROM Customer WHERE CustomerID = NEW.BuyerID
	) THEN
	RAISE EXCEPTION 'Buyer NOT EXISTS!';
	END IF;

	IF NEW.SalespersonID IS NULL OR NOT EXISTS(
		SELECT 1 FROM Salesperson WHERE UserName = NEW.SalespersonID
	) THEN
	RAISE EXCEPTION 'Salesperson NOT EXISTS!';
	END IF;
	
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;


DROP TRIGGER IF EXISTS T_update_car ON CarSales; 
CREATE TRIGGER T_update_car BEFORE UPDATE ON CarSales
FOR EACH ROW 
EXECUTE FUNCTION update_car();

CREATE OR REPLACE FUNCTION add_car_sale(
    make_name TEXT,
    model_name TEXT,
    built_year INTEGER,
    odometer INTEGER,
    price NUMERIC
)
RETURNS BOOLEAN AS $$
DECLARE
    make_code VARCHAR(10);
    model_code VARCHAR(10);
BEGIN
    SELECT MakeCode INTO make_code
    FROM Make
    WHERE LOWER(MakeName) = LOWER(make_name);

    IF make_code IS NULL THEN
        RETURN FALSE;
    END IF;

    SELECT ModelCode INTO model_code
    FROM Model
    WHERE LOWER(ModelName) = LOWER(model_name)
      AND MakeCode = make_code;

    IF model_code IS NULL THEN
        RETURN FALSE;
    END IF;

    INSERT INTO CarSales (MakeCode, ModelCode, BuiltYear, Odometer, Price, IsSold)
    VALUES (make_code, model_code, built_year, odometer, price, FALSE);

    RETURN TRUE;
EXCEPTION
    WHEN OTHERS THEN
        RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS update_car_sale;

CREATE FUNCTION update_car_sale(
    n_carsaleid INTEGER,
    n_customer TEXT,
    n_salesperson TEXT,
    n_saledate DATE
)
RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE CarSales
    SET 
        BuyerID = (SELECT CustomerID FROM Customer WHERE LOWER(CustomerID) = LOWER(n_customer)),
        SalespersonID = (SELECT UserName FROM Salesperson WHERE LOWER(UserName) = LOWER(n_salesperson)),
        SaleDate = n_saledate,
        IsSold = TRUE
    WHERE  CarSaleID = n_carsaleid;

    IF FOUND THEN
        RETURN True;
    ELSE
        RETURN False;
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        RETURN FALSE;
END;
$$;

SELECT update_car_sale(18, 'c001', 'jdoe', '2024-05-01');
SELECT * FROM CarSales WHERE carsaleid = 18