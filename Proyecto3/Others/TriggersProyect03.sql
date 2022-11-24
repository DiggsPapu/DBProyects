select * from sesion
        select sesion.sesionname,sesion.sesiondate,sesion.sesionhour,worker.workername from worker
        inner join sesion
        on worker.workerid = sesion.workerid
        inner join sesionuser
        on sesion.sesioncode = sesionuser.sesioncode
        where sesion.sesiondate<=current_date+interval '7 day'

-- TRIGGERS
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
if ((tg_op= 'UPDATE' or tg_op ='INSERT' or tg_op ='DELETE') and current_user = 'postgres') then
select actualweight into new.userweight from usuario
where usuario.userid = new.userid;
elsif (tg_op = 'INSERT'  and u_type = 'usuario') then
select actualweight into new.userweight from usuario
where usuario.userid = new.userid;
select category into new.exercisetype from excategory inner join sesion on sesion.categorycode = excategory.categorycode;
insert into bitacora (workerid,realized_action)
values (NULL,'user_assign_new_sesion');
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
if ((tg_op= 'UPDATE' or tg_op ='INSERT' or tg_op ='DELETE') and current_user = 'postgres') then
elsif ((tg_op = 'UPDATE' ) and u_type = 'usuario') then
insert into bitacora (workerid,realized_action)
values (null,'user_update_sesion_asignation');
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
if ((tg_op= 'UPDATE' or tg_op ='INSERT' or tg_op ='DELETE') and current_user = 'postgres') then
elsif (tg_op = 'UPDATE'and u_type = 'instructor') then
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
if ((tg_op= 'UPDATE' or tg_op ='INSERT' or tg_op ='DELETE') and current_user = 'postgres') then
elsif (tg_op = 'UPDATE'and u_type = 'instructor') then
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
if ((tg_op= 'UPDATE' or tg_op ='INSERT' or tg_op ='DELETE') and current_user = 'postgres') then
elsif (tg_op = 'UPDATE'and u_type = 'instructor') then
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
if ((tg_op= 'UPDATE' or tg_op ='INSERT' or tg_op ='DELETE') and current_user = 'postgres') then

elsif (tg_op = 'SELECT' and u_type = 'usuario') then
insert into bitacora(workerid,realized_action)
values (null,'user_search_sesion');
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
if ((tg_op= 'UPDATE' or tg_op ='INSERT' or tg_op ='DELETE') and current_user = 'postgres') then
elsif (tg_op = 'INSERT' and u_type = 'usuario') then
insert into bitacora(workerid,realized_action)
values (null,'user_create_user');
elsif (tg_op = 'UPDATE'and u_type = 'usuario') then
insert into bitacora (workerid,realized_action)
values (current_user,'user_update_user');
elsif (tg_op = 'INSERT' and u_type = 'admin_create_role') then
insert into bitacora(workerid,realized_action)
values (current_user,'admin_create_user');
elsif (tg_op = 'UPDATE'and u_type = 'admin_create_role') then
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
if ((tg_op ='UPDATE' or tg_op= 'INSERT' or tg_op ='DELETE') and current_user = 'postgres') then

elsif (tg_op = 'UPDATE'and u_type = 'usuario') then
insert into bitacora (workerid,realized_action)
values (null,'user_update_usercontract');
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
if ((tg_op= 'UPDATE' or tg_op= 'INSERT' or tg_op= 'DELETE') and current_user = 'postgres') then

elsif (tg_op = 'INSERT' and new.workertype='admin_create_role') then
insert into bitacora (workerid,realized_action)
values (current_user,'admin_create_admincreaterole');
elsif (tg_op = 'INSERT' and new.workertype='admin_full_admin') then
insert into bitacora (workerid,realized_action)
values (current_user,'admin_create_adminfulladmin');
elsif (tg_op = 'INSERT' and new.workertype='Instructor') then
insert into bitacora (workerid,realized_action)
values (current_user,'admin_create_instructor');
elsif (tg_op = 'UPDATE' and u_type = 'Instructor') then
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


drop trigger trigger_bitacora_usercontract on usercontract;
drop function bitacora_usercontract();


drop trigger trigger_new_contractuser on usercontract;
drop function new_contract_user();


drop trigger trigger_bitacora_usuario on usuario;
drop function bitacora_usuario();