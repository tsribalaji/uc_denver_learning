/* Query 38 */
Select SYSDATE From Dual;

/* Query 39 */
Select (SysDate-HireDate)/7 From emp;

/* Query 40 */
Select 	empno, hiredate, Months_Between(SysDate, hiredate) Tenure, 
Add_Months(hiredate, 6) Review From emp Where Months_Between(SysDate, hiredate)<36;

/* Query 41*/
Select next_day(hiredate, 'MONDAY')
From emp
Where ename='KING';

/* Query 42*/
Select next_day('23-Nov-1992', 'Sunday')
from dual;

/* Query 43*/
Select next_day('23-Nov-1992', 'Sunday')+7
from dual;


/* Query 44*/
Select Last_day('01-Feb-2000')
from dual;

/* Query 45*/
Select to_char(sysdate, '"Today is" mm/dd/yyyy.') Today from dual;


/* Query 46*/
select to_char(sysdate, 'Month, ddth, yyyysp') from dual; 

/* Query 47*/
select to_char(sysdate, 'Month, ddth, year') from dual; 

/* Query 48*/
select to_char(sysdate, '"Today is " Day.') from dual;

/* Query 49*/
select ename, to_char(hiredate, 'Day, Mon. ddth, yyyy') from emp where lower(ename) = 'king';

/* Query 50*/
select to_char(to_date('Nov-23-1992','Mon-DD-yyyy'),'Day') from dual;


/* Query 51*/
Select ename, To_char(sal, '$99,999') From emp;


/* Query 53*/
select ename, to_char(hiredate, 'Day') from emp;

/* Query 54*/
select ename, to_char(hiredate, 'Day') from emp
where to_char(hiredate, 'DAY') like 'SATURDAY%' or to_char(hiredate, 'DAY') LIKE 'SUNDAY%';

/* Query 56*/
select ename
from emp
where to_char(hiredate, 'Mon') = 'Jan';

/* Query 57*/
Select loc
From dept inner join emp on (dept.deptno=emp.deptno)
Where ename='WARD';

/* Query 59*/
select name "Customer Name", ename "Rep Name"
from customer, emp
where customer.repid = emp.empno and lower(city)= 'cupertino';


/* Query 60*/
select name "Customer Name", mgr
from customer inner join emp on (customer.repid = emp.empno)
where lower(city)= 'cupertino';


/* Query 62*/
Select job, avg(sal)
From Emp
Group by job;


/* Query 64*/
select deptno, sum(sal) from emp group by deptno;


/* Query 65*/
select deptno, count(empno)
from emp
group by deptno;

/* Query 66*/
Select count(ename)
From emp;


/* Query 67*/
Select min(hiredate), max(hiredate)
From emp;


/* Query 68*/
select avg(sal), max(sal), min(sal), sum(sal) from emp;

/* Query 70*/
select count(empno) from emp where lower(job) in ('salesman', 'clerk');

/* Query 73*/
select job, avg(sal) from emp where lower(job) in ('salesman', 'clerk') group by job;

/* Query 75*/
select count(empno) "Num Hired" from emp where to_char(hiredate, 'Mon') ='Mar';

/* Query 74*/
select trim(to_char(hiredate, 'Day')), count(empno) "Num Emp"
from emp
group by trim(to_char(hiredate, 'Day'));


/* Query 76*/
Select deptno, job, avg(sal) From emp Group by deptno, job;

/* Query 77*/
Select deptno, max(sal) as MaxOfSal From emp
Group by deptno
Having max(sal)>6500;


/* Query 78*/
Select deptno, max(sal) as MaxOfSal
From emp
Group by deptno
Having min(sal)>3500;


/* Query 79*/
Select job, sum(sal) PAYROLL
From emp
Where job NOT LIKE 'SALES%'
Group by job
Having sum(sal)>16000
Order by Sum(sal);


/* Query 80*/
Select job, sum(sal) PAYROLL
From emp
Where hiredate<= '03-DEC-2001'
Group by job
Having sum(sal)>10000
Order by avg(sal);


/* Query 82*/
select job, count(empno)
from emp
group by job
having count(empno)>=4;

