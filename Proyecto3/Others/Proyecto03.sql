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
    ContractCode int,
    UserID varchar(30) references Usuario(userid) on delete cascade,
    subscriptionType varchar(30)check (subscriptiontype='DIAMOND' or subscriptiontype = 'GOLD'),
    lastDate date default((current_date+ interval'1 year')::date),
    smartwatchreturn boolean default false,
    activeContract boolean default true,
    paymentmethod varchar(6),
    cardnumber varchar(16),
    initdate date default(current_date::date),
    primary key (contractcode,userid)
);
-- select ((current_date+ interval'1 year')::date)
create table Worker(
    WorkerID varchar(30),
    WorkerPassword varchar(30),
    workername varchar(30),
    direction varchar(100),
    WorkerType varchar(30),
    primary key (workerid)
);
create table instructorcontract(
    contractinstructorcode int,
    workerid varchar(30) references worker(workerid) on delete cascade,
    contractlength int default(30),
    activecontract boolean default(true),
    weight float check (25<=weight and 700>=weight),
    height float check(0.5<=height and 3.0>=height),
    primary key (contractinstructorcode,workerid)
);

create table excategory (
    categorycode int primary key,
    category varchar(30)
);
create table sesion(
    sesioncode int primary key,
    sesionname varchar(30),
    sesiondate date check(sesiondate>=current_date),
    sesionhour time check(sesionhour<='10:59:59' and sesionhour>='00:00:00'),
    timelength time check(timelength<='01:00:00' and timelength>='00:00:00'),
    sesionstatus varchar(4) check(sesionstatus='QUIT' or sesionstatus='DONE' or sesionstatus='WAIT'), --     quit, done, wait
    description varchar(100),
    workerid varchar(30) references worker(workerid) on delete cascade,
    categorycode int references excategory(categorycode) on delete cascade
);
create table sesionuser(
    userid varchar(30) references usuario(userid) on delete cascade,
    sesioncode int references sesion(sesioncode) on delete cascade,
    caloriesacomplished float default 0.0,
    heartrate int check(480<=heartrate and heartrate>=26),
    exercisetype varchar(30),
    userweight float check(0.5<=userweight and 3.0>=userweight),
    primary key (userid,sesioncode)    
);
create table bitacora(
    action_id int primary key,
    workerid varchar(30) references worker(workerid) on delete cascade,
    realized_action varchar(30),
    execution_date date default (current_date::date),
    execution_hour time default (current_time(0)::time)
);
-- DROP TABLES
drop table bitacora;
drop table sesionuser;
drop table sesion;
drop table excategory;
drop table instructorcontract;
drop table worker;
drop table usercontract;
drop table usuario;
-- SELECT TABLES
select * from usuario;
select * from usercontract;
select * from worker;
select * from instructorcontract;
select * from excategory;
select * from sesion;
select * from sesionuser;
select * from bitacora;
-- DELETE TABLES
delete from usuario;
delete from usercontract;
delete from worker;
delete from instructorcontract;
delete from excategory;
delete from sesion;
delete from bitacora;
-- CREATE ROLES
-- Show all the db names
SELECT datname FROM pg_database;
-- Show all the roles
select * from pg_roles
SELECT * FROM information_schema.table_privileges
-- Admin level full admin gets all permissions
create role full_admin;
grant all privileges on database proyect to full_admin;
revoke all privileges on database proyect from full_admin
drop role full_admin

create user dieggspapu with password 'Manager123';--los nombres de usuario quedan en minusculas, las contrasenias no
grant full_admin to dieggspapu;
drop role admin_level1
drop user uoi

-- Admin create users
create role admin_create_role createrole  createrole createdb login
grant rolcreaterole privileges on database proyect to admin_create_role
drop role admin_create_role 
create role andres with password 'Manager123' createrole login
grant admin_create_role to andres
drop role andres
-- Admin level 3
create role admin_level3;
grant select on asignation, curse, student to admin_level3;
grant insert on asignation to admin_level3;
revoke select on asignation, curse, student to admin_level3;
revoke insert on asignation to admin_level3;
create user Ulises2 with password 'Ulises2';
grant admin_level3 to Ulises2;
grant insert on student to admin_level3;
drop role admin_level3
drop user ulises2
-- Reporteroy admin
create role admin_reportery;
grant select,insert,delete on bitacora to admin_reportery;

-- TRIGGERS
-- Trigger to generate the bitacora usuario
create or replace function bitacora_usuario()
returns trigger as $trigger_bitacora_usuario$
declare bitacora_id int;
declare id_worker varchar(30);
begin
select count(action_id)+1 into bitacora_id from bitacora;
select current_user into id_worker;
if (tg_op = 'INSERT' and current_user = 'postgres') then
select null into id_worker;
insert into bitacora(action_id,workerid,realized_action)
values (bitacora_id,id_worker,'user_create_user');
elsif (tg_op = 'UPDATE'and current_user = 'postgres') then
select null into id_worker;
insert into bitacora (action_id,workerid,realized_action)
values (bitacora_id,id_worker,'user_update_user');
elsif (tg_op = 'INSERT') then
insert into bitacora(action_id,workerid,realized_action)
values (bitacora_id,id_worker,'admin_create_user');
elsif (tg_op = 'UPDATE') then
insert into bitacora (action_id,workerid,realized_action)
values (bitacora_id,id_worker,'admin_update_user');
elsif (tg_op = 'DELETE') then
insert into bitacora (action_id,workerid,realized_action)
values (bitacora_id,id_worker,'admin_update_user');
end if;
return null;
end;
$trigger_bitacora_usuario$Language plpgsql;

create or replace trigger trigger_bitacora_usuario
after insert or update or delete on usuario
for each row execute procedure bitacora_usuario();

drop trigger trigger_bitacora_usuario on usuario;
drop function bitacora_usuario();
-- Create trigger bitacora user contract
create or replace function bitacora_usercontract()
returns trigger as $trigger_bitacora_usercontract$
declare bitacora_id int;
declare id_worker varchar(30);
begin
select count(action_id)+1 into bitacora_id from bitacora;
select current_user into id_worker;
if (tg_op = 'INSERT') then
insert into bitacora(action_id,workerid,realized_action)
values (bitacora_id,id_worker,'admin_create_usernewcontract');
elsif (tg_op = 'UPDATE') then
insert into bitacora (action_id,workerid,realized_action)
values (bitacora_id,id_worker,'admin_update_usercontract');
elsif (tg_op = 'DELETE') then
insert into bitacora (action_id,workerid,realized_action)
values (bitacora_id,id_worker,'admin_delete_usercontract');
end if;
return null;
end;
$trigger_bitacora_usercontract$Language plpgsql;

create or replace trigger trigger_bitacora_usercontract
after insert or update or delete on usercontract
for each row execute procedure bitacora_usercontract();

drop trigger trigger_bitacora_usercontract on usercontract;
drop function bitacora_usercontract();
-- Create trigger bitacora worker
create or replace function bitacora_worker()
returns trigger as $trigger_bitacora_worker$
declare bitacora_id int;
declare id_worker varchar(30);
begin
select count(action_id)+1 into bitacora_id from bitacora;
select current_user into id_worker;
if (tg_op = 'INSERT' and new.workertype='admin_create_role') then
insert into bitacora(action_id,workerid,realized_action)
values (bitacora_id,id_worker,'admin_create_admincreaterole');
elsif (tg_op = 'INSERT' and new.workertype='admin_full_admin') then
insert into bitacora(action_id,workerid,realized_action)
values (bitacora_id,id_worker,'admin_create_adminfulladmin');
elsif (tg_op = 'UPDATE') then
insert into bitacora (action_id,workerid,realized_action)
values (bitacora_id,id_worker,'admin_update_worker');
elsif (tg_op = 'DELETE') then
insert into bitacora (action_id,workerid,realized_action)
values (bitacora_id,id_worker,'admin_delete_worker');
end if;
return null;
end;
$trigger_bitacora_usercontract$Language plpgsql;

create or replace trigger trigger_bitacora_worker
after insert or update or delete on worker
for each row execute procedure bitacora_worker();

drop trigger trigger_bitacora_usercontract on usercontract;
drop function bitacora_usercontract();
-- Trigger to generate a new contract id for user
create or replace function new_contract_user()
returns trigger as $$
begin 
select count(contractcode) into new.contractcode;
select upper(new.subscriptiontype) into new.subscriptiontype;
if (new.subscriptiontype = 'DIAMOND') then
select true into new.smartwatchreturn;
end if;
return new;
end;
$$Language plpgsql;

create or replace trigger trigger_new_contractuser
before insert
on usercontract
for each row execute procedure new_contract_user();

drop trigger trigger_new_contractuser;
drop function new_contract_user();

-- Trigger to generate a new contract id for instructor
create or replace function new_contract_instructor()
returns trigger as $$
begin
select count(contractcode)+1 into new.contractinstructorcode;
return new;
end;
$$ Language plpgsql;

create or replace trigger trigger_new_instructorcontract
before insert
on instructorcontract
for each row execute procedure new_contract_instructor();

drop trigger trigger_new_instructorcontract on instructorcontract;
drop function new_contract_instructor();
-- Trigger to validate a username
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
-- Pruebas
insert into usuario(userid,password,name,birthdate,height,actualweight,direction)
values('dieguito3','manager123','diego alonzo','2002-01-20',1.60,50,'Primera calle 12-51 sector b1 ciudad san cristobal zona 8 de mixco');
update usuario set userid = 'dieguito' where userid = 'dieguito3';
insert into worker (workerid,workerpassword,workername,direction,workertype)
values('postgres','Manager123','DieggsPapu','Primera calle 12-51 sector b1 ciudad san cristobal zona 8 de mixco','full_admin');
insert into usercontract(contractcode,userid,subscriptiontype,lastdate,smartwatchreturn,activecontract,paymentmethod,cardnumber,initdate)
values (1,'dieguito','diamond','2023-11-17',true,true,)
insert into instructorcontract(contractinstructorcode,workerid,contractlength,activecontract,weight,height)
