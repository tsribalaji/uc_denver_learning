/* Page 19  - 1 */
CREATE TABLE Book(
Barcode VarChar2(10),
Title VarChar2(25),
BYear Number(4),
TypeName Varchar2(10),
CONSTRAINT Book_Barcode_pk PRIMARY KEY(Barcode));

/* Page 19  - 2 */
CREATE TABLE Booktype (Typename varchar2(9),LoanLength number(3));

/* Page 20  - 3 */
ALTER TABLE Booktype ADD CONSTRAINT booktype_typename_pk PRIMARY KEY(typename);

/* Page 20  - 4 */
ALTER TABLE Book ADD CONSTRAINT book_typename_fk FOREIGN KEY(typename) REFERENCES Booktype(typename);

/* Page 20  - 5 */
ALTER TABLE Book ADD CONSTRAINT book_Byear_ck CHECK(Byear<2000);

/* Page 20  - 6 */
ALTER TABLE Book ADD (CONSTRAINT book_typename_NN CHECK(typename IS NOT null), CONSTRAINT book_Byear_ck2 CHECK(Byear>1900));

/* Page 20  - 7 */
ALTER TABLE book ADD(NumOfPages number(3),Publisher  varchar2(30));

/* Page 22-24  - 8 */
ALTER TABLE book DROP(NumOfPages, Publisher);

/* Page 22-24  - 9 */
ALTER TABLE Booktype DROP CONSTRAINT booktype_typename_pk CASCADE;

/* Page 23  - 1 */
INSERT INTO Dept (deptno, dname, loc) VALUES(50, 'DEVELOPMENT', 'DETROIT');

/* Page 23  - 2 */
INSERT INTO dept(deptno, dname)VALUES(60, 'MIS');

/* Page 23  - 3 */
INSERT INTO ord(ordid, orderdate, custid, shipdate, total) VALUES(701, sysdate, '108', to_date(sysdate, 'dd-mon-yyyy')+7, 1000); 

/* Page 23  - 4 */
INSERT INTO ord(ordid, orderdate, custid, shipdate, total)VALUES(702, sysdate, 107, '15-JUL-2019', 1500);

/* Page 23  - 5 */
INSERT ALL INTO dept(deptno, dname) VALUES(70, 'HR') INTO dept (deptno, dname) VALUES(80, 'FINANCE')
SELECT * FROM dual;

/* Page 24  - 6 */
DELETE FROM Dept WHERE dname='DEVELOPMENT';

/* Page 24  - 7 */
DELETE FROM Dept;

/* Page 24  - 8 */
UPDATE emp SET deptno=20, ename='Mike' WHERE empno=7782;

/* Page 24  - 9 */
UPDATE emp SET deptno=20;

/* Page 25  - 1 */
Select ename From emp Where sal > (Select sal From emp Where empno=7566);

/* Page 25  - 5 */ 
select ename from emp where empno in (select mgr from emp where empno in (select repid from customer where lower(city)='cupertino'));

/* Page 25  - 6 */
select ename from emp where empno in (select mgr from emp where empno in (select repid from customer where lower(city)='burlingame'));

/* Page 25  - 9 */
select * from product where prodid in (select distinct prodid from item where ordid in (select ordid from ord where orderdate not between '01-Jan-2017' and '31-Jan-2017'));

/* Page 26  - 10 */
DELETE FROM emp WHERE deptno = (SELECT deptno FROM dept WHERE dname='SALES');

/* Page 26  - 11 */
UPDATE emp SET deptno = (SELECT deptno FROM emp WHERE empno=7788) WHERE job = (SELECT job FROM emp WHERE empno=7788);

/* Video 30  */
SELECT constraint_name, table_name, r_constraint_name FROM user_constraints where constraint_type = 'R';

SELECT constraint_name, table_name, search_condition FROM user_constraints where constraint_type = 'C';

  