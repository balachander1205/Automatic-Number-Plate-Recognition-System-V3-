CREATE TABLE TBL_ALPR(
    ID INT NOT NULL AUTO_INCREMENT,
    VEHICLE_IMG VARCHAR(100),
    ALPR_IMG VARCHAR(100),
    QRCODE_IMG VARCHAR(100),
    STARTDATETIME DATETIME,
    ENDDATATIME DATETIME,
    PARKING_HOURS FLOAT,
    TOTAL_COST FLOAT,
    ALPR_ID VARCHAR(200),
    VEHICLE_NUM VARCHAR(100),
    EXTRA_COL2 VARCHAR(100),
    EXTRA_COL3 VARCHAR(100),
    PRIMARY KEY(ID)
)

CREATE TABLE TBL_VEH_HOTLIST(
    ID INT NOT NULL AUTO_INCREMENT,
    VEHICLE_IMG VARCHAR(100),
    ALPR_IMG VARCHAR(100),
    STARTDATETIME DATETIME,
    ENDDATATIME DATETIME,
    ALPR_ID VARCHAR(200),
    VEHICLE_NUM VARCHAR(100),
    EXTRA_COL2 VARCHAR(100),
    EXTRA_COL3 VARCHAR(100),
    PRIMARY KEY(ID)
)

INSERT INTO `tbl_veh_hotlist`(
        `ID`,
        `VEHICLE_IMG`,
        `ALPR_IMG`,
        `STARTDATETIME`,
        `ENDDATATIME`,
        `ALPR_ID`,
        `VEHICLE_NUM`,
        `EXTRA_COL2`,
        `EXTRA_COL3`
    )
VALUES(0,'/static/NumberPlates/2018-03-14/numplates/NumberPlates/1a69840a-1d73-4f46-ab9a-a922c0d71f64.png',
    '/static/NumberPlates/2018-03-14/numplates/NumberPlates/1a69840a-1d73-4f46-ab9a-a922c0d71f64.png',
    '2018-03-19 04:14:00',
    '2018-03-19 04:14:00',
    '2018kahdiuasuid8198daasdsds',
    'AP09CP8795',
    '','')

INSERT INTO `TBL_ALPR`(
    `ID`,
    `VEHICLE_IMG`,
    `ALPR_IMG`,
    `QRCODE_IMG`,
    `STARTDATETIME`,
    `ENDDATATIME`,
    `PARKING_HOURS`,
    `TOTAL_COST`,
    `ALPR_ID`,
    `VEHICLE_NUM`,
    `EXTRA_COL2`,
    `EXTRA_COL3`
)
VALUES(
    NULL,
    '/static/NumberPlates/2018-03-14/numplates/NumberPlates/1a69840a-1d73-4f46-ab9a-a922c0d71f64.png',
    '/static/NumberPlates/2018-03-14/numplates/NumberPlates/1a69840a-1d73-4f46-ab9a-a922c0d71f64.png',
    '/static/NumberPlates/2018-03-14/numplates/NumberPlates/1a69840a-1d73-4f46-ab9a-a922c0d71f64.png',
    '2018-03-19 04:14:00',
    '2018-03-19 07:18:00',
    '25',
    '50',
    '12200-12220-112239-',
    NULL,
    NULL,
    NULL
);
-- Select query to get row between dates
SELECT
    `VEHICLE_IMG`,
    `ALPR_IMG`,
    `QRCODE_IMG`,
    `STARTDATETIME`,
    `ENDDATATIME`,
    `PARKING_HOURS`,
    `TOTAL_COST`,
    `ALPR_ID`
FROM
    TBL_ALPR
WHERE
    DATE(`STARTDATETIME`) >= '2018-03-20' AND DATE(`STARTDATETIME`) <= '2018-03-24'



