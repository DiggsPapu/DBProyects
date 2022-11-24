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
    sesionhour time check(sesionhour<='22:59:59' and sesionhour>='05:00:00'),
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
    userweight float check(25<=userweight and 700>=userweight),
    primary key (userid,sesioncode)    
);
create table bitacora(
    action_id serial primary key,
    workerid varchar(30),
    realized_action varchar(100),
    execution_date date default (current_date::date),
    execution_hour time default (current_time(0)::time)
);
-- Super user

insert into worker (workerid,workerpassword,workername,direction,workertype)
values('postgres','Manager123','postgres','THE POSTGRES','Superuser');
-- Trigger to the bitacora insert sesion user
create or replace function bitacora_insert_sesionuser()
returns trigger as $trigger_bitacora_sesionuser$
declare u_type varchar(30);
declare weight float;
begin
select rolname into u_type from pg_catalog.pg_roles
inner join (
    select roleid from pg_auth_members 
    inner join (
        select oid from pg_catalog.pg_roles 
        where rolname = current_user
    ) as s
    on s.oid =pg_auth_members.member
)as b
on b.roleid = oid;
if (tg_op = 'INSERT'  and u_type = 'usuario') then
select actualweight into new.userweight from usuario
where usuario.userid = new.userid;
select category into new.exercisetype from excategory inner join sesion on sesion.categorycode = excategory.categorycode;
insert into bitacora (workerid,realized_action)
values (current_user,'user_assign_new_sesion');
elsif (tg_op = 'INSERT') then 
select actualweight into new.userweight from usuario
where usuario.userid = new.userid;
select category into new.exercisetype from excategory inner join sesion on sesion.categorycode = excategory.categorycode;
insert into bitacora(workerid,realized_action)
values (current_user,'admin_create_asignation');
end if;
return new;
end;
$trigger_bitacora_sesionuser$Language plpgsql;

create or replace trigger trigger_bitacora_insert_sesionuser
before insert on sesionuser
for each row execute procedure bitacora_insert_sesionuser();
-- Trigger to the bitacora delete sesionuser
create or replace function bitacora_sesionuser()
returns trigger as $trigger_bitacora_sesionuser$
declare u_type varchar(30);
declare weight float;
begin
select rolname into u_type from pg_catalog.pg_roles
inner join (
    select roleid from pg_auth_members 
    inner join (
        select oid from pg_catalog.pg_roles 
        where rolname = current_user
    ) as s
    on s.oid =pg_auth_members.member
)as b
on b.roleid = oid;
if ((tg_op = 'UPDATE' ) and u_type = 'usuario') then
insert into bitacora (workerid,realized_action)
values (current_user,'user_update_sesion_asignation');
elsif ((tg_op = 'INSERT' ) and u_type = 'usuario') then
insert into bitacora (workerid,realized_action)
values (current_user,'user_asignating');
elsif ((tg_op = 'DELETE' ) and u_type = 'usuario') then
insert into bitacora (workerid,realized_action)
values (current_user,'user_delete_sesion_asignation');
elsif (tg_op = 'UPDATE') then
insert into bitacora (workerid,realized_action)
values (current_user,'admin_update_asignation');
elsif (tg_op = 'DELETE' ) then
insert into bitacora (worker_id,realized_action)
values (current_user,'admin_delete_asignation');
end if;
return null;
end;
$trigger_bitacora_sesionuser$Language plpgsql;

create or replace trigger trigger_bitacora_sesionuser
after update or delete on sesionuser
for each row execute procedure bitacora_sesionuser();
-- Trigger to generate the bitacora for category update,delete
create or replace function bitacora_category()
returns trigger as $trigger_bitacora_category$
declare u_type varchar(30);
begin
select rolname into u_type from pg_catalog.pg_roles
inner join (
    select roleid from pg_auth_members 
    inner join (
        select oid from pg_catalog.pg_roles 
        where rolname = current_user
    ) as s
    on s.oid =pg_auth_members.member
)as b
on b.roleid = oid;
if (tg_op = 'UPDATE'and u_type = 'instructor') then
insert into bitacora (workerid,realized_action)
values (current_user,'instructor_update_category');
elsif (tg_op = 'SELECT'and u_type = 'usuario') then
insert into bitacora (workerid,realized_action)
values (current_user,'instructor_search_category');
elsif (tg_op = 'INSERT'and u_type = 'instructor') then
insert into bitacora (workerid,realized_action)
values (current_user,'instructor_create_category');
elsif (tg_op = 'DELETE'and u_type = 'instructor') then
insert into bitacora (workerid,realized_action)
values (current_user,'instructor_delete_category');
elsif (tg_op = 'UPDATE'and u_type = 'instructor') then
insert into bitacora (workerid,realized_action)
values (current_user,'instructor_update_instructorcontract');
elsif (tg_op = 'INSERT') then
insert into bitacora(workerid,realized_action)
values (current_user,'admin_create_category');
elsif (tg_op = 'UPDATE') then
insert into bitacora (workerid,realized_action)
values (current_user,'admin_update_category');
elsif (tg_op = 'DELETE' ) then
insert into bitacora (worker_id,realized_action)
values (current_user,'admin_delete_category');
end if;
return new;
end;
$trigger_bitacora_category$Language plpgsql;

create or replace trigger trigger_bitacora_category
after insert or update or delete on excategory
for each row execute procedure bitacora_category();
-- Trigger to generate the bitacora for category update,delete
create or replace function bitacora_insert_category()
returns trigger as $trigger_bitacora_category$
declare u_type varchar(30);
begin
select rolname into u_type from pg_catalog.pg_roles
inner join (
    select roleid from pg_auth_members 
    inner join (
        select oid from pg_catalog.pg_roles 
        where rolname = current_user
    ) as s
    on s.oid =pg_auth_members.member
)as b
on b.roleid = oid;
if (tg_op = 'UPDATE'and u_type = 'instructor') then
insert into bitacora (workerid,realized_action)
values (current_user,'instructor_update_category');
elsif (tg_op = 'SELECT'and u_type = 'usuario') then
insert into bitacora (workerid,realized_action)
values (current_user,'instructor_search_category');
elsif (tg_op = 'INSERT'and u_type = 'instructor') then
insert into bitacora (workerid,realized_action)
values (current_user,'instructor_create_category');
elsif (tg_op = 'DELETE'and u_type = 'instructor') then
insert into bitacora (workerid,realized_action)
values (current_user,'instructor_delete_category');
elsif (tg_op = 'UPDATE'and u_type = 'instructor') then
insert into bitacora (workerid,realized_action)
values (current_user,'instructor_update_category');
elsif (tg_op = 'INSERT') then
insert into bitacora(workerid,realized_action)
values (current_user,'admin_create_category');
elsif (tg_op = 'UPDATE') then
insert into bitacora (workerid,realized_action)
values (current_user,'admin_update_category');
elsif (tg_op = 'DELETE' ) then
insert into bitacora (worker_id,realized_action)
values (current_user,'admin_delete_category');
end if;
return new;
end;
$trigger_bitacora_category$Language plpgsql;

create or replace trigger trigger_bitacora_category
after insert or update or delete on excategory
for each row execute procedure bitacora_category();
-- Trigger to generate the bitacora for instructorcontract
create or replace function bitacora_instructorcontract()
returns trigger as $trigger_bitacora_sesion$
declare u_type varchar(30);
begin
select rolname into u_type from pg_catalog.pg_roles
inner join (
    select roleid from pg_auth_members 
    inner join (
        select oid from pg_catalog.pg_roles 
        where rolname = current_user
    ) as s
    on s.oid =pg_auth_members.member
)as b
on b.roleid = oid;
if (tg_op = 'UPDATE'and u_type = 'instructor') then
insert into bitacora (workerid,realized_action)
values (current_user,'instructor_update_instructorcontract');
elsif (tg_op = 'INSERT' and u_type = 'instructor') then
insert into bitacora(workerid,realized_action)
values (current_user,'instructor_create_renewal_instructorcontract');
elsif (tg_op = 'INSERT') then
insert into bitacora(workerid,realized_action)
values (current_user,'admin_create_instructorcontract');
elsif (tg_op = 'UPDATE') then
insert into bitacora (workerid,realized_action)
values (current_user,'admin_update_instructorcontract');
elsif (tg_op = 'DELETE' ) then
insert into bitacora (worker_id,realized_action)
values (current_user,'admin_delete_instructorcontract');
end if;

return new;
end;
$trigger_bitacora_sesion$Language plpgsql;

create or replace trigger trigger_bitacora_instructorcontract
after insert or update or delete on instructorcontract
for each row execute procedure bitacora_instructorcontract();
-- Trigger to generate the bitacora sesion
create or replace function bitacora_sesion()
returns trigger as $trigger_bitacora_sesion$
declare u_type varchar(30);
begin
select rolname into u_type from pg_catalog.pg_roles
inner join (
    select roleid from pg_auth_members 
    inner join (
        select oid from pg_catalog.pg_roles 
        where rolname = current_user
    ) as s
    on s.oid =pg_auth_members.member
)as b
on b.roleid = oid;
if (tg_op = 'SELECT' and u_type = 'usuario') then
insert into bitacora(workerid,realized_action)
values (current_user,'user_search_sesion');
elsif (tg_op = 'UPDATE'and u_type = 'instructor') then
insert into bitacora (workerid,realized_action)
values (current_user,'instructor_update_sesion');
elsif (tg_op = 'INSERT' and u_type = 'instructor') then
insert into bitacora(workerid,realized_action)
values (current_user,'instructor_create_sesion');
elsif (tg_op = 'DELETE'and u_type = 'instructor') then
insert into bitacora (workerid,realized_action)
values (current_user,'instructor_delete_sesion');
elsif (tg_op = 'INSERT') then
insert into bitacora(workerid,realized_action)
values (current_user,'admin_create_sesion');
elsif (tg_op = 'UPDATE') then
insert into bitacora (workerid,realized_action)
values (current_user,'admin_update_sesion');
elsif (tg_op = 'DELETE' ) then
insert into bitacora (worker_id,realized_action)
values (current_user,'admin_delete_sesion');
end if;
return new;
end;
$trigger_bitacora_sesion$Language plpgsql;

create or replace trigger trigger_bitacora_sesion
after insert or update or delete on sesion
for each row execute procedure bitacora_sesion();
-- Create trigger bitacora usuario
create or replace function bitacora_usuario()
returns trigger as $trigger_bitacora_usuario$
declare u_type varchar(30);
begin
select rolname into u_type from pg_catalog.pg_roles
inner join (
    select roleid from pg_auth_members 
    inner join (
        select oid from pg_catalog.pg_roles 
        where rolname = current_user
    ) as s
    on s.oid =pg_auth_members.member
)as b
on b.roleid = oid;
if (tg_op = 'INSERT' and u_type = 'usuario') then
insert into bitacora(workerid,realized_action)
values (current_user,'user_create_user');
elsif (tg_op = 'UPDATE'and u_type = 'usuario') then
insert into bitacora (workerid,realized_action)
values (current_user,'user_update_user');
elsif (tg_op = 'INSERT' and (u_type = 'admin_create_role' or current_user = 'postgres')) then
insert into bitacora(workerid,realized_action)
values (current_user,'admin_create_user');
elsif (tg_op = 'UPDATE'and (u_type = 'admin_create_role' or current_user = 'postgres')) then
insert into bitacora (workerid,realized_action)
values (current_user,'admin_update_user');
elsif (tg_op = 'INSERT') then
insert into bitacora(workerid,realized_action)
values (current_user,'admin_create_user');
elsif (tg_op = 'UPDATE') then
insert into bitacora (workerid,realized_action)
values (current_user,'admin_update_user');
elsif (tg_op = 'DELETE' ) then
insert into bitacora (worker_id,realized_action)
values (current_user,'admin_delete_user');
end if;
return new;
end;
$trigger_bitacora_usuario$Language plpgsql;

create or replace trigger trigger_bitacora_usuario
after insert or update or delete on usuario
for each row execute procedure bitacora_usuario();

-- Create trigger bitacora user contract

create or replace function bitacora_usercontract()
returns trigger as $trigger_bitacora_usercontract$
declare u_type varchar(30);
begin
select rolname into u_type from pg_catalog.pg_roles
inner join (
    select roleid from pg_auth_members 
    inner join (
        select oid from pg_catalog.pg_roles 
        where rolname = current_user
    ) as s
    on s.oid =pg_auth_members.member
)as b
on b.roleid = oid;
if (tg_op = 'UPDATE'and u_type = 'usuario') then
insert into bitacora (workerid,realized_action)
values (current_user,'user_update_usercontract');
elsif (tg_op = 'INSERT' and (u_type = 'admin_create_role'or u_type =  'postgres')) then
insert into bitacora(workerid,realized_action)
values (current_user,'admin_create_usercontract');
elsif (tg_op = 'UPDATE' and (u_type = 'admin_create_role' or u_type =  'postgres')) then
insert into bitacora (workerid,realized_action)
values (current_user,'admin_update_usercontract');
elsif (tg_op = 'DELETE' ) then
insert into bitacora (worker_id,realized_action)
values (current_user,'admin_delete_usercontract');
end if;
return null;
end;
$trigger_bitacora_usercontract$Language plpgsql;

create or replace trigger trigger_bitacora_usercontract
after insert or update or delete on usercontract
for each row execute procedure bitacora_usercontract();
-- Create trigger bitacora worker
create or replace function bitacora_worker()
returns trigger as $trigger_bitacora_worker$
declare u_type varchar(30);
begin
select rolname into u_type from pg_catalog.pg_roles
inner join (
    select roleid from pg_auth_members 
    inner join (
        select oid from pg_catalog.pg_roles 
        where rolname = current_user
    ) as s
    on s.oid =pg_auth_members.member
)as b
on b.roleid = oid;
if (tg_op = 'INSERT' and new.workertype='admin_create_role') then
insert into bitacora (workerid,realized_action)
values (current_user,'admin_create_admincreaterole');
elsif (tg_op = 'INSERT' and new.workertype='admin_full_admin') then
insert into bitacora (workerid,realized_action)
values (current_user,'admin_create_adminfulladmin');
elsif (tg_op = 'INSERT' and new.workertype='Instructor') then
insert into bitacora (workerid,realized_action)
values (current_user,'admin_create_instructor');
elsif (tg_op = 'UPDATE' and u_type = 'instructor') then
insert into bitacora (workerid,realized_action)
values (current_user,'instructor_update_instructor');
elsif (tg_op = 'UPDATE') then
insert into bitacora (workerid,realized_action)
values (current_user,'admin_update_worker');
elsif (tg_op = 'DELETE') then
insert into bitacora (workerid,realized_action)
values (current_user,'admin_delete_worker');
end if;
return null;
end;
$trigger_bitacora_worker$Language plpgsql;

create or replace trigger trigger_bitacora_worker
after insert or update or delete on worker
for each row execute procedure bitacora_worker();
-- Trigger to generate a set if user has to return the smartwatch
create or replace function new_contract_user()
returns trigger as $$
begin 
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
-- Usuario, the users get the permissions to update their user, create values in sesionuser, consult in sesion, category,worker

create role usuario;
GRANT usuario TO postgres WITH ADMIN OPTION;
grant all privileges on usuario to usuario;
grant insert,select,update on usercontract to usuario;
grant select on sesion to usuario;
grant all privileges on sesionuser to usuario;
grant select on excategory to usuario;
grant select on worker to usuario;
grant all privileges on bitacora to usuario;
grant all privileges on all sequences in schema public to usuario;
-- Instructor admin, the instructors get the permissions to create their own sesions, also update their info.
create role instructor login inherit;

GRANT instructor TO postgres WITH ADMIN OPTION;
grant update,select on worker to instructor;
grant update,insert,select on instructorcontract to instructor;
grant update,insert,select on sesion to instructor;
grant update, insert, select,delete on excategory to instructor;
grant insert,select on bitacora to instructor;
grant all privileges on all sequences in schema public to instructor;
grant update,select on worker to instructor;
grant update,insert,select,delete on sesion to instructor;
grant update, insert,select, delete on excategory to instructor;
grant insert,select, update on instructorcontract to instructor;
grant insert,select on bitacora to instructor;
grant all privileges on all sequences in schema public to instructor;

-- Admin create users
create role admin_create_role createrole login;
GRANT admin_create_role TO postgres WITH ADMIN OPTION;
grant insert,select on worker to admin_create_role;
grant insert on instructorcontract to admin_create_role;
grant insert on sesionuser to admin_create_role;
grant insert,select on usuario to admin_create_role;
grant insert,select on usercontract to admin_create_role;
grant insert,select on bitacora to admin_create_role;
grant all privileges on all sequences in schema public to admin_create_role;
-- Reportery admin
create role admin_reportery login inherit;
GRANT admin_reportery TO postgres WITH ADMIN OPTION;
grant select,insert,delete on bitacora to admin_reportery;
grant all privileges on all sequences in schema public to admin_reportery;
create user raulalbiol password 'RaulAlbiol' valid until '2022-11-25 06:00:00' login;
grant instructor to raulalbiol;

insert into worker(workerid,workerpassword,workername,direction,workertype)
values('raulalbiol','RaulAlbiol','Raul Albiol','Raul av','Instructor');
insert into instructorcontract(workerid,weight,height)
values('raulalbiol',80,1.80);

-- Create views
create index on sesion(sesionhour,sesiondate);
create index on sesion(sesionhour);
create index on sesion(sesiondate);
create view top_5_sesions_user as
select sesionname,sesiondate,sesionhour,timelength,sesionstatus,description,j.count as amount_people from sesion
inner join (
    select workername,c.count,c.sesioncode from worker
    inner join (
        select * from sesion
        inner join (
            select count(sesionuser.userid), sesioncode as l from sesionuser
            group by sesioncode
        ) as p
        on p.l = sesion.sesioncode
    ) as c
    on c.workerid = worker.workerid
)as j
on j.sesioncode = sesion.sesioncode
where sesion.sesionhour<'18:00:00.000000-06:00' and sesion.sesionhour>'09:00:00.000000-06:00' and sesion.sesiondate < current_date
Limit 5;
create view top_10_alltimesesions_user as
select sesionname,sesiondate,sesionhour,timelength,sesionstatus,description,j.count as amount_people from sesion
inner join (
    select workername,c.count,c.sesioncode from worker
    inner join (
        select * from sesion
        inner join (
            select count(sesionuser.userid), sesioncode as l from sesionuser
            group by sesioncode
        ) as p
        on p.l = sesion.sesioncode
    ) as c
    on c.workerid = worker.workerid
)as j
on j.sesioncode = sesion.sesioncode
Limit 10;
select * from top_10_alltimesesions_user;

create or replace view top_10_most_instructors as
select workername, count(s.workerid) from worker 
inner join (
    select s.sesioncode, s.workerid, uc.userid 
    from sesion as s 
    inner join (
        select userid, sesioncode from sesionuser 
    ) as uc 
    on uc.sesioncode = s.sesioncode
) as s on s.workerid=worker.workerid 
group by workername Limit 10;
create index on sesion(sesioncode,workerid);

create index on usercontract(subscriptiontype);
create or replace view subscriptiontype_lastsixmonth_amount as
select usercontract.subscriptiontype, count(subscriptiontype) 
from usercontract 
where (initdate>=current_date-interval'6 month')
group by usercontract.subscriptiontype
order by subscriptiontype desc;
select * from subscriptiontype_lastsixmonth_amount;
create index on bitacora(workerid)
create or replace view profileupdate as 
(select 'Description: User updated profile', workerid, count(realized_action) from bitacora
where realized_action = 'user_update_user'
group by workerid
limit 5)
union all
(select 'Description: Instructor updated profile', workerid, count(realized_action) from bitacora
where realized_action = 'instructor_update_instructor'
group by workerid
limit 5)
union all 
(select 'Description: Admin updated profile', workerid,count(realized_action) from bitacora
where realized_action = 'admin_update_worker'
group by workerid
limit 5);

select * from sesion
select * from sesionuser

create view users_withoutlast3week_exercise as
(select * from sesionuser
inner join sesion
on sesion.sesioncode = sesionuser.sesioncode
where sesion.sesiondate>=current_date - interval '3 week')
except all
(select * from sesionuser
inner join sesion
on sesion.sesioncode = sesionuser.sesioncode
where sesionuser.caloriesacomplished >0);

create index on usuario(name);
create view users_withoutlast3week_exercise as
select usuario.name,count(sesion.sesioncode) as faltas from usuario
inner join sesionuser
on sesionuser.userid = usuario.userid
inner join sesion
on sesion.sesioncode = sesionuser.sesioncode
where sesion.sesiondate>=current_date - interval '3 week' and sesion.sesiondate<current_date
group by usuario.name
except all
select usuario.name,count(sesion.sesioncode) as faltas from usuario
inner join sesionuser
on sesionuser.userid = usuario.userid
inner join sesion
on sesion.sesioncode = sesionuser.sesioncode
where sesionuser.caloriesacomplished >0
group by usuario.name;
select * from users_withoutlast3week_exercise;