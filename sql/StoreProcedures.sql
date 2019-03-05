opencv js 
https://hub.packtpub.com/object-detection-using-image-features-javascript/

-- Creation of procedure --
DELIMITER //
CREATE PROCEDURE getAlprDataSP(
	OUT vehicle_img varchar(100),
	OUT ALPR_ID	varchar(200),
	OUT VEHICLE_NUM	varchar(100))

LANGUAGE SQL
DETERMINISTIC
SQL SECURITY DEFINER
COMMENT 'Sample SQL procedure returns alpr table data'

BEGIN 
SELECT VEHICLE_IMG, 
       ALPR_ID, 
       VEHICLE_NUM       
INTO   vehicle_img, 
       ALPR_ID, 
       VEHICLE_NUM       
FROM   TBL_ALPR;
END 

-- Procedure 2 --
DELIMITER //
CREATE PROCEDURE getAlprDataSP2()
LANGUAGE SQL
DETERMINISTIC
SQL SECURITY DEFINER
COMMENT 'Sample SQL procedure returns alpr table data'

BEGIN
	DECLARE vehicle_img varchar(100);
	DECLARE ALPR_ID	varchar(200);
	DECLARE VEHICLE_NUM	varchar(100); 
	SELECT VEHICLE_IMG, 
	       ALPR_ID, 
	       VEHICLE_NUM       
	INTO   vehicle_img, 
	       ALPR_ID, 
	       VEHICLE_NUM       
	FROM   TBL_ALPR;

	SELECT * FROM TBL_ALPR;
END 

-- Calling procedure --
CALL getAlprDataSP(@VEHICLE_IMG, @STARTDATETIME, @ALPR_ID, @VEHICLE_NUM);
SELECT @vehicle_img AS `VECHICLE IMG`, 
   @STARTDATETIME AS `START DATE TIME`, 
   @ALPR_ID AS `ALPR ID`, 
   @VEHICLE_NUM AS `VEHICLE NUMBER`;

CREATE
PROCEDURE getAlprData(
    OUT vehicle_img VARCHAR(100),
    OUT STARTDATETIME DATETIME,
    OUT ALPR_ID VARCHAR(200),
    OUT VEHICLE_NUM VARCHAR(100)
) LANGUAGE SQL DETERMINISTIC SQL SECURITY DEFINER COMMENT 'Sample SQL procedure returns alpr table data'
BEGIN
SELECT * FROM TBL_ALPR;
END

-- procedure 3 --
DELIMITER //
CREATE PROCEDURE getAlprDataSP3()
LANGUAGE SQL
DETERMINISTIC
SQL SECURITY DEFINER
COMMENT 'Sample SQL procedure returns alpr table data'
BEGIN 
SELECT VEHICLE_IMG AS `Vehicle Image`, 
       ALPR_ID AS `ALPR ID`, 
       VEHICLE_NUM AS `Vehicle Number`          
FROM   TBL_ALPR;
END 


-- DHFL Sample SP --
DELIMITER //
CREATE PROCEDURE get15GHnotUpdatedSP(
	IN bkr_id VARCHAR(20), 
	IN financial_year VARCHAR(20)
	)
LANGUAGE SQL
DETERMINISTIC
SQL SECURITY DEFINER
COMMENT 'Sample stored procedure to returns active deposits data'
BEGIN 
SELECT BKR_ID AS `Broker ID`, 
	   CSTID AS `Cust ID`,
	   CSTNAME AS `Customer Name`,
	   CITY AS `City`,
	   PIN AS `Pin`,
	   TTL_DEPST_HELD AS `Total Deposits Held`,
	   PAN AS `PAN`,
	   CST_MBL_NO AS `Customer Mobile Number`,
	   CST_TEL AS `Customer Tel`,
	   CST_MAIL AS `Customer Mail`
FROM   TBL_BKR_EXAMPLE
WHERE BKR_ID = bkr_id
AND YEAR = financial_year;
END

-- java code to call procedure --
package com.storedprocedure;

import java.sql.*;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ParameterMetaData;

public class StoredProcedure {

	public static void main(String args[]) throws Exception {
		
		
		Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/customers_orders","root","");
		
		String sql_process_order = "{call UpdateQtyCustomerBalance(?,?,?,?)}";
		CallableStatement cs = conn.prepareCall(sql_process_order);
		cs.setInt(1, 1);//product_id
		cs.setInt(2, 1); // customer-id
		cs.setInt(3, 1);// qty - product qunatity
		cs.setFloat(4,300); // amount
		
		int rows = cs.executeUpdate();
		System.out.println(rows + " rows have successfully been updated");
		
		
	    }
	
	
	
	}