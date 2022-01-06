/*Query 1A*/
Select custid, name From customer Where repid=7844;

/*Query 1B*/
Select custid, name from customer join emp on (customer.repid = emp.empno) where emp.ename ='TURNER';

/*Query 2A*/
select distinct  repid from customer where area=415;

/*Query 2B*/
select distinct ename from customer inner join emp on (repid=empno) where area=415;

/*Query 2C*/
Select distinct MGR from EMP join CUSTOMER on (emp.empno = customer.repid) where customer.area=415;

/*Query 3A*/
select ordid from ord where shipdate=orderdate or shipdate=orderdate+1 order by ordid;

/*Query 3B*/
select distinct prodid from ord, item where (shipdate=orderdate or shipdate=orderdate+1) and  ord.ordid=item.ordid order by prodid;

/*Query 3C*/
select distinct product.prodid, product.descrip from ord, item, product where ord.ordid=item.ordid and item.prodid=product.prodid and (shipdate=orderdate or shipdate=orderdate+1);

/*Query 4*/
select distinct emp.ename from emp
inner join customer on (emp.empno = customer.repid)
inner join ord on (customer.custid = ord.custid)
inner join item on (item.ordid = ord.ordid) 
inner join product on (item.prodid = product.prodid) where product.descrip like 'ACE TENNIS NET';

/*Query 5*/
select 'name' from customer where creditlimit >= 9000;
/*Query 6*/
select ordid, orderdate, shipdate from ord where ord.shipdate < ord.orderdate;
/*Query 7*/
select ename from emp where empno in (select repid from customer where customer.state = 'CA');

/*Query 23*/
select ename, count(custid) from customer, emp where customer.repid=emp.empno  group by repid, ename  having count(custid)>=3;

/*Query 24*/
select mgr, count(mgr) from emp group by mgr having count(mgr)>= 3;

/*Query 8*/
select ord.orderdate, ord.ordid, item.prodid, item.actualprice, price.stdprice, price.startdate, price.enddate 
from ord inner join item on ord.ordid = item.ordid  inner join price on item.prodid = price.prodid 
         where item.actualprice < price.stdprice;

/*Query 9*/
select orderdate, ord.ordid, item.prodid, item.actualprice, price.stdprice, price.startDate, price.EndDate
from ord inner join item on (ord.ordid = item.ordid)
         inner join price on (item.prodid = price.prodid)
where item.actualprice<price.stdprice and (ORD.ORDERDATE>PRICE.STARTDATE) and
      (ord.orderdate<price.EndDate or price.EndDate IS NULL);
      
/*Query 10*/
select count(ordid) from ord where custid=100;

/*Query 14*/
select custid, sum(total) from ord group by custid;

/*Query 15*/
select sum(total) from ord;

/*Query 18*/
select custid, sum(total) from ord where custid in (100, 106) group by custid;

/*Query 22*/
select repid, count(custid) from customer group by repid having count(custid)>=3;


/*Query 25*/
select sum(sal) from emp where mgr=7698;

/*Query 26*/
select emp.job, avg(emp.sal) from emp group by emp.job;

/*Query 27*/
select prodid, descrip from product where descrip like '%TENNIS%';

/*Query 28*/
Select custid, name from customer where substr(name, 1, 1)='J' and area=415;

/*Query 30*/
Select ename from emp where deptno in (10,20);

/*Query 34*/
Select customer.custid, customer.name from customer inner join emp on (customer.repid=emp.empno) where emp.ename='ALLEN';

/*Query 36*/
Select customer.custid, customer.name from customer 
    inner join Ord on (customer.custid=ord.custid)
    where To_char(orderDate, 'MonYYYY')='Feb2017';
    
/*Query 37*/
select ename, sal*12 ANNUAL_SAL, sal*1.05*12 CUSTOM_SAL from emp 
where lower(job) = 'salesman'or job = 'analyst';






