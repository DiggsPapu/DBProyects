create table Usuario(
    userID varchar(30) primary key,
    password varchar(30),
    name varchar(30),
    birthdate date,
    height float,
    actualweight float,
    direction varchar(100)
)5
update worker set workerpassword = 'Manager123' where workerid = 1
delete from usuario where userid = 'Riuk'

create table UserContract(
    ContractCode int primary key,
    UserID varchar(30) references Usuario(userid) on delete cascade,
    subscriptionType varchar(30),
    lastDate date,
    smartwatchreturn boolean,
    activeContract boolean,
    paymentmethod varchar(6),
    cardnumber varchar(16),
    initdate date
)
drop table usercontract
select * from usercontract
create table userprogress(
    progresscode int primary key,
    userid varchar(30) references Usuario(userid) on delete cascade,
    weekweight float,
    weekcalories float
)
select * from usuario
select * from usercontract
drop table userprogress
select count(contractcode) from usercontract
select * from userProgress
drop table usuario
drop table usercontract
drop table userprogress
delete from usuario where userid = 'DieggsPapu'
insert into usuario(
    userid,password,
        name,birthdate,
        height,actualweight,
        direction
)
select * from worker
values('DieggsPapu','Manager123','Diego','2002-01-20',1.60,50,'First avenue')
create table Worker(
    WorkerID int primary key,
    WorkerPassword varchar(30),
    workername varchar(30),
    direction varchar(100),
    WorkerType varchar(5)
)
update worker set workerpassword = 'Manager123' where workerid = 1
drop table worker
select * from worker
select * from worker where workerid = 1 and workerpassword = 'RaulAlbiol01' and workertype = 'Instr'
insert into worker(workerid,workerpassword,workername,direction,workertype)
values(0,'Manager123','Diego Andres Alonzo Medinilla','First av','Admin')
insert into worker(workerid,workerpassword,workername,direction,workertype)
values(1,'RaulAlbiol01','Raul Albiol','First av','Instr')
drop table sesion
create table sesion(
    sesioncode int primary key,
    sesionname varchar(30),
    sesiondate date,
    sesionhour time,
    timelength time,
    sesionstatus varchar(4), --     quit, done, wait
    description varchar(100),
    workerid int references worker(workerid) on delete cascade,
    categorycode int references excategory(categorycode) on delete cascade
)
insert into sesion(
    sesioncode,sesionname,sesiondate,sesionhour,timelength,sesionstatus,description,workerid,categorycode
)
values(1,'Calisthenics 2','2022-8-09','11:00:00','00:59:00','wait','Work with body', 1,1)
select * from sesion
create table sesionuser(
    userid varchar(30) references usuario(userid) on delete cascade,
    sesioncode int references sesion(sesioncode) on delete cascade,
    caloriesacomplished float,
    heartrate int,
    exercisetype varchar(30),
    userweight float,
    primary key (userid,sesioncode)    
);
drop table sesionuser
create table excategory (
    categorycode int primary key,
    category varchar(30)
)
select * from excategory
-- Check if user name is already taken
create function validation_UserName()
returns trigger as $$
declare repetidos int;
begin
select count(userid) into repetidos 
from usuario where userid = new.userid;
if (repetidos>0) then
raise exception 'The username is already taken'
using errcode = '20808';
end if;
return new;
end;
$$Language plpgsql;

create trigger trigger_validUsername
before insert
on usuario
for each row execute procedure validation_UserName()

drop function validation_UserName()
drop trigger trigger_validUsername on usuario

-- Table InstructorContract
create table instructorcontract(
    contractinstructorcode int primary key,
    workerid int references worker(workerid) on delete cascade,
    contractlength int,
    activecontract boolean,
    weight float,
    height float
)
select * from instructorcontract
select * from excategory
create table sesion(
    sesioncode int primary key,
    sesionname varchar(30),
    sesiondate date,
    sesionhour hour,
    sesionstatus varchar(4),
    description varchar(100),
    workerid int references worker(workerid) on delete cascade,
    categorycode int references category(categorycode) on delete cascade
)
insert into sesion(sesioncode,sesiondate,sesionhour,sesionstatus,description,workerid,categorycode)
values(5,'2022-07-09',)
delete from sesionuser where userid = 'DieggsPapu' and sesioncode = '4'
select * from sesion
select * from sesionuser
select * from sesion inner join (select * from sesionuser where userid = 'DieggsPapu') as us on us.sesioncode = sesion.sesioncode 
select * from sesionuser inner join (select sesioncode,sesiondate, sesionhour,sesionstatus from sesion where sesion.sesiondate <= '2022-10-18' and sesion.sesiondate >= '2022-07-07') as s on s.sesioncode = sesionuser.sesioncode where sesionuser.userid = 'DieggsPapu'
select * from sesionuser inner join (select sesioncode, sesiondate, sesionhour from sesion where sesion.sesionstatus = 'done') as s on s.sesioncode = sesionuser.sesioncode where sesionuser.userid ='DieggsPapu'
select count(sesionuser.userid), sesionuser.sesioncode from sesionuser group by sesionuser.sesioncode order by count(sesionuser.userid) desc limit 10 
select * from sesion inner join (select count(sesionuser.userid), sesionuser.sesioncode from sesionuser group by sesionuser.sesioncode order by count(sesionuser.userid) desc limit 10 ) as us on us.sesioncode = sesion.sesioncode
select count(sesion.sesioncode), c.category from sesion inner join (select category, categorycode from excategory) as c on c.categorycode = sesion.categorycode group by c.category, sesion.categorycode
select count (uc.userid), c.category from sesionuser as uc inner join (select sesioncode, categorycode from sesion) as s on s.sesioncode = uc.sesioncode inner join (select category, categorycode from excategory) as c on c.categorycode = s.categorycode group by c.category, s.categorycode
 select (select count (uc.userid), c.category from sesionuser) as uc inner join (select sesioncode, categorycode from sesion) as s on s.sesioncode = uc.sesioncode inner join (select category, categorycode from excategory) as c on c.categorycode = s.categorycode group by c.category, s.categorycode
 select workername, count(s.workerid) from worker inner join (select s.sesioncode, s.workerid, uc.userid from sesion as s inner join (select userid, sesioncode from sesionuser ) as uc on uc.sesioncode = s.sesioncode) as s on s.workerid=worker.workerid group by workername Limit 5
 
 select count(uc.userid), s.sesionhour from sesion as s inner join (select userid, sesioncode from sesionuser) as uc on uc.sesioncode = s.sesioncode where s.sesiondate = '2022-10-18' group by s.sesionhour order by count(uc.userid) desc Limit 1
 select subscriptiontype, count(subscriptiontype) from usercontract where initdate>='2022-06-18' and subscriptiontype = 'Diamond' group by subscriptiontype 
 select count(sesion.sesioncode), c.category from sesion inner join (select category, categorycode from excategory) as c on c.categorycode = sesion.categorycode where sesion.sesiondate >='2022-01-07' and sesion.sesiondate<='2022-10-18' group by c.category, sesion.categorycode
 select * from sesionuser
 select * from usuario
 select * from sesion
 select * from worker