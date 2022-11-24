-- CREATE TABLES
create table Usuario(
    userID varchar(30) primary key,
    password varchar(30),
    name varchar(30),
    birthdate date check (birthdate>='1940-01-01'),
    height float check (0.5<=height and 3.0>=height),
    actualweight float check (25<=actualweight and 700>=actualweight),
    direction varchar(100)
);
create table UserContract(
    ContractCode serial,
    UserID varchar(30) references Usuario(userid) on delete cascade,
    subscriptionType varchar(30)check (subscriptiontype='DIAMOND' or subscriptiontype = 'GOLD'),
    lastDate date default((current_date+ interval'1 year')::date),
    smartwatchreturn boolean default false,
    activeContract boolean default true,
    paymentmethod varchar(6) check(paymentmethod = 'DEBIT' or paymentmethod = 'CREDIT'),
    cardnumber varchar(16),
    initdate date default(current_date::date),
    primary key (contractcode)
);
create table Worker(
    WorkerID varchar(30),
    WorkerPassword varchar(30),
    workername varchar(30),
    direction varchar(100),
    WorkerType varchar(30),
    primary key (workerid)
);
create table instructorcontract(
    contractinstructorcode serial,
    workerid varchar(30) references worker(workerid) on delete cascade,
    weight float check (25<=weight and 700>=weight),
    height float check(0.5<=height and 3.0>=height),
    primary key (contractinstructorcode,workerid)
);

create table excategory (
    categorycode serial primary key,
    category varchar(30)
);
create table sesion(
    sesioncode serial primary key,
    sesionname varchar(30),
    sesiondate date check(sesiondate>=current_date),
    sesionhour time check(sesionhour<='22:59:59' and sesionhour>='00:00:00'),
    timelength time check(timelength<='01:00:00' and timelength>='00:00:00'),
    sesionstatus varchar(4) check(sesionstatus='QUIT' or sesionstatus='DONE' or sesionstatus='WAIT'), --     quit, done, wait
    description varchar(100),
    workerid varchar(30) references worker(workerid) on delete cascade,
    categorycode int references excategory(categorycode) on delete cascade
);
select * from 
insert into sesionuser()

select * from sesion
left join sesionuser
on sesion.sesioncode = sesionuser.sesioncode
where sesionuser.userid = 'dieggspapu' 
and sesionuser.sesioncode = null

select * from sesion 
where not exists

select * from sesion 
left join 
sesionuser
on sesionuser.sesioncode = sesion.sesioncode
where sesionuser.sesioncode = null

select * from sesionuser
left join
sesion
on sesion.sesioncode = sesionuser.sesioncode
where sesion.sesioncode = null

select * from sesion
where sesion.sesiondate = '2022-11-23'
except all 
select sesion.sesioncode,sesion.sesionname,sesion.sesiondate,sesion.sesionhour,sesion.timelength,sesion.sesionstatus,sesion.description,sesion.workerid,sesion.categorycode from sesion
inner join sesionuser 
on sesionuser.sesioncode = sesion.sesioncode
where userid = 'dieggspapu';

where sesioncode not in (
select sesioncode from sesion
inner join sesionuser 
on sesionuser.sesioncode = sesion.sesioncode
where userid = 'dieggspapu' ) as p


create table sesionuser(
    userid varchar(30) references usuario(userid) on delete cascade,
    sesioncode int references sesion(sesioncode) on delete cascade,
    caloriesacomplished float default 0.0,
    heartrate int check(480<=heartrate and heartrate>=26) default 70,
    exercisetype varchar(30),
    userweight float check(25<=userweight and 700>=userweight),
    primary key (userid,sesioncode)    
);
create table bitacora(
    action_id serial primary key,
    workerid varchar(30),
    realized_action varchar(30),
    execution_date date default (current_date::date),
    execution_hour time default (current_time(0)::time)
);
-- DROP TABLES
drop view top_10_alltimesesions_user;
drop view profileupdate;
drop view top_5_sesions_user;
drop view top_10_most_instructors;
drop view subscriptiontype_lastsixmonth_amount;
drop table bitacora;
drop table sesionuser;
drop table sesion;
drop table excategory;
drop table instructorcontract;
drop table worker;
drop table usercontract;
drop table usuario;
select now()+interval '2 min'
-- SELECT TABLES
select * from usuario;
select * from usercontract;
select * from worker;
select * from instructorcontract;
select * from excategory;
select * from sesion;
select * from sesionuser;
select * from bitacora;
grant all privileges on usuario to dieggspapu
grant all privileges on bitacora to dieggspapu
select * from sesion where sesioncode = 1
select * from sesion 
left outer join (
    select sesioncode from sesionuser 
        where sesionuser.sesioncode 
not in (select sesionuser.sesioncode from sesionuser 
        where sesionuser.userid = 'dieggspapu')) as b 
on b.sesioncode = sesion.sesioncode
where sesiondate = '2022-11-23'
select * from sesionuser where usercode = 'dieggspapu'
-- DELETE TABLES
delete from usuario;
delete from usercontract;
delete from worker;
delete from instructorcontract;
delete from excategory;
delete from sesion;
delete from bitacora;

select localtimestamp(0)

select * from usercontract
inner join (select max(contractcode) from usercontract where userid = 'dixie') as p
on p.max = usercontract.contractcode

select * from instructorcontract
inner join (select max(contractinstructorcode) from instructorcontract where workerid = 'raulalbiol') as p
on p.max = instructorcontract.contractinstructorcode

select current_date+interval'12 month'
create user andres password 'Manager123' createrole;
grant admin_create_role to andres;
drop user andres;

insert into usuario(userid,password,name,birthdate,height,actualweight,direction)
values('dieggspapu','Manager123','Diego Alonzo','2002-01-20',1.90,50,'Primera calle');
insert into usercontract(userid,subscriptiontype,paymentmethod,cardnumber)
values('dieggspapu','DIAMOND','CREDIT','123456789');
-- select ((current_date+ interval'1 year')::date)