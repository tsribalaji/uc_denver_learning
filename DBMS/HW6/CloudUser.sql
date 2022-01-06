/* Problem 1*/
select to_char(SysDate+65, 'Day, mm/dd/yyyy') from dual;

/* Problem 2*/
select ename, to_char(hiredate, 'Day, Mon, ddth, yyyy')  from emp where to_char(hiredate, 'Mon') = 'Apr';

/* Problem 3*/
select ordId, orderdate from ord where to_char(orderdate, 'Mon, yyyy') in ('Jan, 2017', 'Feb, 2017');

/* Problem 4*/
select ord.custid, customer.name, ord.ordid, ord.orderdate from ord inner join customer on ord.custid = customer.custid where orderdate = shipdate;

/* Problem 5*/
select distinct product.prodid, product.descrip from ord inner join item on ord.ordid = item.ordid inner join product on product.prodid = item.prodid where to_char(ord.orderdate, 'yyyy') = '2017' and product.descrip like '%GUIDE TO TENNIS%';

/* Problem 6*/
select emp.ename from emp inner join customer on empno = repid where address like '574%';

/* Problem 7*/
select to_char(orderdate, 'yyyy'), count(prodid) month from ord inner join item on item.ordid = ord.ordid  group by to_char(orderdate, 'yyyy');

/* Problem 8*/
select product.prodid, sum(item.qty) SoldCount from product inner join item on item.prodid = product.prodid group by product.prodid HAVING product.prodid in (100870, 100860, 100861);

/* Problem 9*/
select sum(item.qty) SoldCount from product inner join item on item.prodid = product.prodid where product.prodid in (100870, 100860, 100861);

/* Problem 10*/
select avg(item.actualprice) avg_sale_price from product inner join item on item.prodid = product.prodid where product.descrip like '%ACE%';

/* Problem 5*/
select prodid, sum(Qty) from item where actualprice > 2.5 group by prodid having sum(qty) >=1000

/* Problem 5*/


/* Problem 5*/