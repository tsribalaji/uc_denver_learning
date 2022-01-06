Drop table "OrderItem" cascade constraints;
Drop table "MenuItem" cascade constraints;
Drop table "OrderFeedback" cascade constraints;
Drop table "Order" cascade constraints;
Drop table "Payment" cascade constraints;
Drop table "DeliveryAgent" cascade constraints;
Drop table "PaymentType" cascade constraints;
Drop table "Restaurant" cascade constraints;
Drop table "OrderStatus" cascade constraints;
Drop table "Customer" cascade constraints;

Purge RecycleBin; 

CREATE TABLE "Customer" (
 CustID	NUMBER(10) NOT NULL,
 FName	  VARCHAR2(14),
 Lname	  VARCHAR2(14),
 Address  VARCHAR2(50),
 Phone	  VARCHAR2(14),
 email    VARCHAR2(50),
 CONSTRAINT CustID PRIMARY KEY (CustID));
 
 INSERT INTO	"Customer"	VALUES	(	1001,'Aaron','Smith','49 W Burgundy St, Aurora, CO 80129','1236547896','aaron.smit@gmail.com'	);
INSERT INTO	"Customer"	VALUES	(	1002,'Rainn','Wilson','455 Arbor Rd, Hillsbourough, MI 90345','(456) 987-1236','r.wilson@msn.com'	);
INSERT INTO	"Customer"	VALUES	(	1003,'Mike','Scott','4 S Parker Rd, Aurora, CO 80014','(789) 654-1222','mikey133@outlook.com'	);
INSERT INTO	"Customer"	VALUES	(	1004,'Wayne','Rooney','56 Parkour Ln, Farmington, MI, 67558','(342) 342-3423','rooney.w@gmail.com'	);
INSERT INTO	"Customer"	VALUES	(	1005,'Abigail','Paul','877, W Birch St, Wilcox, NJ 90876','(343) 424-3434','abi.p@gmail.com'	);
INSERT INTO	"Customer"	VALUES	(	1006,'Trishla','Perry','456, N Balfour Rd, Thornton, CO 87684','(234) 242-3423','trish.perry@gmail.com'	);


CREATE TABLE "PaymentType" ( TypeId  NUMBER(4) NOT NULL, Description  VARCHAR2(50),
 CONSTRAINT TypeId_PK PRIMARY KEY (TypeId));
 
INSERT INTO	"PaymentType"	VALUES	(	1,'Online Payment'	);
INSERT INTO	"PaymentType"	VALUES	(	2,'Credit Card'	);
INSERT INTO	"PaymentType"	VALUES	(	3,'Debit Card'	);
INSERT INTO	"PaymentType"	VALUES	(	4,'Payment Wallet'	);
INSERT INTO	"PaymentType"	VALUES	(	5,'Venmo'	);
INSERT INTO	"PaymentType"	VALUES	(	6,'Square'	);



CREATE TABLE "Restaurant" ( RID	NUMBER(5) NOT NULL, RPhone	  VARCHAR2(14), Raddress  VARCHAR2(50), Rlocation  VARCHAR2(50), RName  VARCHAR2(50),  CONSTRAINT RID PRIMARY KEY (RID));

INSERT INTO	"Restaurant"	VALUES	(	101,'4565155454','7412 S University Blvd, Centennial, CO 80122','S University Blvd','Udom Thai'	);
INSERT INTO	"Restaurant"	VALUES	(	102,'8040452666','1234 Main St. Pizzatown, MI 48501','Main St.','Little Caesars'	);
INSERT INTO	"Restaurant"	VALUES	(	103,'5225226336','9364 S Colorado Blvd Highlands Ranch, CO','S Colorado Blvd','QDOBA Mexican Eats'	);
INSERT INTO	"Restaurant"	VALUES	(	104,'2589632589','2563 S Arapahoe St, Centennial, CO 81922','S Arapahoe St','Swasthi Indian Gourmet'	);
INSERT INTO	"Restaurant"	VALUES	(	105,'4589632147','7142 E County Line Rd, Littleton, CO 80126','E County Line Rd','Egg Roll King'	);
INSERT INTO	"Restaurant"	VALUES	(	106,'5465464546','8545 S Quebec St, Highlands Ranch, CO 80130','S Quebec St','Lodo Bar Grill'	);


CREATE TABLE "MenuItem" (
 MID               NUMBER(3),
 Description                 VARCHAR2(50),
 UnitePrice                 NUMBER(9,2),
 RestuarantId                NUMBER(5),
 CONSTRAINT MID PRIMARY KEY (MID),
 CONSTRAINT RestuarantId_FK FOREIGN KEY (RestuarantId) REFERENCES "Restaurant" (RID)) ;
INSERT INTO	"MenuItem"	VALUES	(	1,'Veggie Wrap',10.49,105	);
INSERT INTO	"MenuItem"	VALUES	(	2,'Chicken King Roll',12.69,105	);
INSERT INTO	"MenuItem"	VALUES	(	3,'Chicken Biriyani',9.29,104	);
INSERT INTO	"MenuItem"	VALUES	(	4,'Paneer Tikka Masala',9.99,104	);
INSERT INTO	"MenuItem"	VALUES	(	5,'Mac n Cheese',5.99,106	);
INSERT INTO	"MenuItem"	VALUES	(	6,'Yellow Curry Noodles',12.99,101	);
INSERT INTO	"MenuItem"	VALUES	(	7,'Margherita Pizza 11in',14.99,102	);
INSERT INTO	"MenuItem"	VALUES	(	8,'Pizza Pastries - 4pc',11.99,102	);
INSERT INTO	"MenuItem"	VALUES	(	9,'Pad Thai - Veg',10.99,101	);
INSERT INTO	"MenuItem"	VALUES	(	10,'Burrito - Beef',12.99,103	);
INSERT INTO	"MenuItem"	VALUES	(	11,'Rice bowl - Veg',9.79,103	);
INSERT INTO	"MenuItem"	VALUES	(	12,'Portobello Mushroom Sandwich',15.99,106	);


CREATE TABLE "DeliveryAgent" (
	AgentId	VARCHAR2(4),
	Aname	VARCHAR2(50),
	Vehicle#	VARCHAR2(10),
	Aphone VARCHAR2(15),
	CONSTRAINT AgentId PRIMARY KEY (AgentId));
 
INSERT INTO	"DeliveryAgent"	VALUES	(	'A10','Michael','BN456','(125) 448-8877'	);
INSERT INTO	"DeliveryAgent"	VALUES	(	'A11','Sam','ER456','(233) 569-8763'	);
INSERT INTO	"DeliveryAgent"	VALUES	(	'A12','Rio','RIO1234','(458) 623-6589'	);
INSERT INTO	"DeliveryAgent"	VALUES	(	'A13','Paris','AS8921','(847) 896-5321'	);
INSERT INTO	"DeliveryAgent"	VALUES	(	'A14','Parker','HJ1234','(896) 336-9877'	);


CREATE TABLE "OrderStatus" (
	StatusId            VARCHAR2(4) NOT NULL,
	Description         VARCHAR2(50),
 CONSTRAINT StatusId_PK PRIMARY KEY (StatusId));

INSERT INTO	"OrderStatus"	VALUES	(	'S1','Waiting for order confirmation'	);
INSERT INTO	"OrderStatus"	VALUES	(	'S2','Confirmed'	);
INSERT INTO	"OrderStatus"	VALUES	(	'S3','Preparing Order'	);
INSERT INTO	"OrderStatus"	VALUES	(	'S4','Waiting For delivery agent '	);
INSERT INTO	"OrderStatus"	VALUES	(	'S5','On the way to pick up'	);
INSERT INTO	"OrderStatus"	VALUES	(	'S6','Picked Up '	);
INSERT INTO	"OrderStatus"	VALUES	(	'S7','Delivered'	);


CREATE TABLE "Payment" (
	PID            VARCHAR2(4) NOT NULL,
	Status            VARCHAR2(50) NOT NULL,
	PDate DATE,
	TypeId NUMBER(4) NOT NULL,
 CONSTRAINT PID PRIMARY KEY (PID),
 CONSTRAINT TypeId_FK FOREIGN KEY (TypeId) REFERENCES "PaymentType"  (TypeId));

INSERT INTO	"Payment"	VALUES	(	'P1','Pending',TO_DATE('12/16/2020', 'mm/dd/yyyy'),1	);
INSERT INTO	"Payment"	VALUES	(	'P2','Success',TO_DATE('12/17/2020', 'mm/dd/yyyy'),2	);
INSERT INTO	"Payment"	VALUES	(	'P3','Failed', TO_DATE('01/13/2021', 'mm/dd/yyyy'),6	);
INSERT INTO	"Payment"	VALUES	(	'P4','Payment processing',TO_DATE('1/17/2021', 'mm/dd/yyyy'),3	);
INSERT INTO	"Payment"	VALUES	(	'P5','Pending',TO_DATE('2/17/2021', 'mm/dd/yyyy'),3	);
INSERT INTO	"Payment"	VALUES	(	'P6','Pending',TO_DATE('2/27/2021', 'mm/dd/yyyy'),2	);
INSERT INTO	"Payment"	VALUES	(	'P7','Success',TO_DATE('3/7/2021', 'mm/dd/yyyy'),5	);
INSERT INTO	"Payment"	VALUES	(	'P8','Payment processing',TO_DATE('3/10/2021', 'mm/dd/yyyy'),1	);
INSERT INTO	"Payment"	VALUES	(	'P9','Success',TO_DATE('3/11/2021', 'mm/dd/yyyy'),1	);
INSERT INTO	"Payment"	VALUES	(	'P10','Success',TO_DATE('3/12/2021', 'mm/dd/yyyy'),3	);
INSERT INTO	"Payment"	VALUES	(	'P11','Success',TO_DATE('3/13/2021', 'mm/dd/yyyy'),4	);
INSERT INTO	"Payment"	VALUES	(	'P12','Failed',TO_DATE('3/13/2021', 'mm/dd/yyyy'),5	);



CREATE TABLE "Order" (
	OrderId	NUMBER(5),
	ODate DATE,
	TotalAmount	NUMBER(9,2),
	CustId	NUMBER(10),
	RID	NUMBER(5),
	PID	VARCHAR2(4),
	AgentId	VARCHAR2(4),
	CONSTRAINT OrderId_PK PRIMARY KEY (OrderId),
	CONSTRAINT CustId_FK FOREIGN KEY (CustId) REFERENCES "Customer"  (CustID),
	CONSTRAINT RID_FK FOREIGN KEY (RID) REFERENCES "Restaurant"  (RID),
	CONSTRAINT PID_FK FOREIGN KEY (PID) REFERENCES "Payment"  (PID),
	CONSTRAINT AgentId_FK FOREIGN KEY (AgentId) REFERENCES "DeliveryAgent"  (AgentId));
 
INSERT INTO	"Order"	VALUES	(	10001,TO_DATE('12/13/2020', 'mm/dd/yyyy'),59.05,1001,105,'P1','A10'	);
INSERT INTO	"Order"	VALUES	(	10002,TO_DATE('12/23/2020', 'mm/dd/yyyy'),74.94,1003,102,'P2','A11'	);
INSERT INTO	"Order"	VALUES	(	10003,TO_DATE('01/01/2021', 'mm/dd/yyyy'),  130.79,1004,105,'P4','A11'	);
INSERT INTO	"Order"	VALUES	(	10004,TO_DATE('02/13/2021', 'mm/dd/yyyy'), 133.67,1005,103,'P3','A12'	);
INSERT INTO	"Order"	VALUES	(	10005,TO_DATE('02/23/2021', 'mm/dd/yyyy'), 28.57,1005,104,'P5','A13'	);
INSERT INTO	"Order"	VALUES	(	10006,TO_DATE('03/13/2021', 'mm/dd/yyyy'), 5.99,1001,103,'P6','A14'	);
INSERT INTO	"Order"	VALUES	(	10007,TO_DATE('03/13/2021', 'mm/dd/yyyy'), 6.99,1006,103,'P7','A12'	);



CREATE TABLE "OrderItem" (
	MID	NUMBER(3),
	OrderId	NUMBER(5),
	CurrentPrice	NUMBER(9,2),
	Qty NUMBER(5),
	CONSTRAINT PK  PRIMARY KEY (OrderId, MID),
	CONSTRAINT OrderId_FK FOREIGN KEY (OrderId) REFERENCES "Order"  (OrderId),
	CONSTRAINT MID_FK FOREIGN KEY (MID) REFERENCES "MenuItem"  (MID));
	
	
INSERT INTO	"OrderItem"	VALUES	(	1,10001,20.98,2	);
INSERT INTO	"OrderItem"	VALUES	(	1,10003,41.96,4	);
INSERT INTO	"OrderItem"	VALUES	(	2,10001,38.07,3	);
INSERT INTO	"OrderItem"	VALUES	(	2,10003,88.83,7	);
INSERT INTO	"OrderItem"	VALUES	(	3,10005,18.58,2	);
INSERT INTO	"OrderItem"	VALUES	(	4,10005,9.99,1	);
INSERT INTO	"OrderItem"	VALUES	(	7,10002,14.99,1	);
INSERT INTO	"OrderItem"	VALUES	(	8,10002,59.95,5	);
INSERT INTO	"OrderItem"	VALUES	(	10,10004,25.98,2	);
INSERT INTO	"OrderItem"	VALUES	(	10,10006,5.99,1	);
INSERT INTO	"OrderItem"	VALUES	(	10,10007,6.99,1	);
INSERT INTO	"OrderItem"	VALUES	(	11,10004,107.69,19	);




CREATE TABLE "OrderFeedback" (
	FID	VARCHAR2(4),
	Feedback VARCHAR2(250),
	Rating NUMBER(1),	
	OrderId	NUMBER(5),
	CONSTRAINT FID_PK  PRIMARY KEY (FID),
	CONSTRAINT Feedback_OrderId_FK FOREIGN KEY (OrderId) REFERENCES "Order"  (OrderId));
	
INSERT INTO	"OrderFeedback"	VALUES	(	'F1','Good food',5,10001	);
INSERT INTO	"OrderFeedback"	VALUES	(	'F2','Crispy and hot',4,10002	);
INSERT INTO	"OrderFeedback"	VALUES	(	'F3','Very spicy',3,10003	);
INSERT INTO	"OrderFeedback"	VALUES	(	'F4','Food tastes like old stock',2,10004	);
INSERT INTO	"OrderFeedback"	VALUES	(	'F5','Wrong food delivered',1,10005	);
INSERT INTO	"OrderFeedback"	VALUES	(	'F6','Amazing food ',6,10006	);


commit; --commit so all inserted data are saved.
