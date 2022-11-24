-- CREATE ROLES
-- Show all the db names
SELECT datname FROM pg_database;
-- Show all the roles
SELECT * FROM information_schema. table_privileges where grantee = 'admin_create_role';
UPDATE information_schema. table_privileges SET is_grantable='YES' where grantee = 'admin_create_role';

select * from pg_roles;
grant all privileges on sesionuser to dieggspapu
select * from pg_roles;
select * from pg_catalog.pg_user;
select * from 
grant all privileges on usuario to andres with grant option
select * from information_schema.table_privileges where grantor != 'postgres'
SELECT grantee, table_name,privilege_type FROM information_schema.table_privileges
where grantee = 'usuario' or grantee = 'admin_create_role' or grantee = 'dieggspapu'
group by grantee,table_name,privilege_type;
select session_user;
select current_user;
create user dieggspapu password 'Manager123';
grant usuario to dieggspapu;
select * from pg_auth_members;
select * from pg_catalog.pg_roles;
-- Rolname
select rolname from pg_catalog.pg_roles
inner join (
    select roleid from pg_auth_members 
    inner join (
        select oid from pg_catalog.pg_roles 
        where rolname = 'dieggspapu'
    ) as s
    on s.oid =pg_auth_members.member
)as b
on b.roleid = oid
select * from pg_catalog.pg_user catalog
-- Usuario, the users get the permissions to update their user, create values in sesionuser, consult in sesion, category,worker
create role usuario login inherit;
grant insert on usuario to usuario;
grant update on usuario to usuario;
grant insert on usercontract to usuario;
grant select on usercontract to usuario;
grant update on usercontract to usuario;
grant select on sesion to usuario;
grant insert on sesionuser to usuario;
grant delete on sesionuser to usuario;
grant select on excategory to usuario;
grant select on worker to usuario;
grant all privileges on all sequences in schema public to usuario;
-- Instructor admin, the instructors get the permissions to create their own sesions, also update their info.
create role instructor login inherit;
grant update on worker to instructor;
grant update,insert,delete on sesion to instructor;
grant update, insert, delete on excategory to instructor;
grant insert,select on bitacora to instructor;
grant all privileges on all sequences in schema public to instructor;
-- Admin create users
create role admin_create_role createrole login inherit;
grant insert,select on worker to admin_create_role;
grant insert on instructorcontract to admin_create_role;
grant insert on sesionuser to admin_create_role;
grant insert,select on usuario to admin_create_role;
grant insert,select on usercontract to admin_create_role;
grant insert,select on bitacora to admin_create_role;
grant all privileges on all sequences in schema public to admin_create_role;
-- Reportery admin
create role admin_reportery login inherit;
grant select,insert,delete on bitacora to admin_reportery;
grant all privileges on all sequences in schema public to admin_reportery;
-- Drop roles
revoke all privileges on usuario from usuario;
revoke all privileges on sesionuser from usuario;
revoke all privileges on sesion from usuario;
revoke all privileges on usercontract from usuario;
revoke all privileges on excategory from usuario;
revoke all privileges on worker from usuario;
revoke all privileges on bitacora from usuario;
revoke all privileges on all sequences in schema public from usuario;
drop role usuario;
revoke all privileges on worker from instructor;
revoke all privileges on sesion from instructor;
revoke all privileges on excategory from instructor;
revoke all privileges on bitacora from instructor;
revoke all privileges on all sequences in schema public from instructor;
drop role instructor;
revoke all privileges on worker from admin_create_role;
revoke all privileges on instructorcontract from admin_create_role;
revoke all privileges on sesionuser from admin_create_role;
revoke all privileges on usuario from admin_create_role;
revoke all privileges on bitacora from admin_create_role;
revoke all privileges on all sequences in schema public from admin_create_role;
drop role admin_create_role;
revoke all privileges on bitacora from admin_reportery;
revoke all privileges on bitacora from admin_reportery;
revoke all privileges on all sequences in schema public from admin_reportery;
drop role admin_reportery;
-- Example
create user andres password 'Manager123' createrole login;
grant admin_create_role to andres;
grant insert,select on usuario to andres;
grant update on usuario to andres;
grant insert on sesionuser to andres;
grant select on sesion to andres;
grant select on excategory to andres;
grant select on worker to andres;
grant all privileges on bitacora to andres;
grant insert on usercontract to andres;
grant usage, select on all sequences in schema public to andres;
insert into worker(workerid,workerpassword,workername,direction,workertype)
values('andres','Manager123','Andres Medinilla','First av','admin_create_role');
revoke all privileges on usuario from andres;
revoke all privileges on sesionuser from andres;
revoke all privileges on worker from andres;
revoke all privileges on bitacora from andres;
revoke all privileges on excategory from andres;
revoke all privileges on sesion from andres;
revoke all privileges on usercontract from andres;
revoke all privileges on function bitacora_usuario() from andres;
revoke all privileges on all sequences in schema public from andres;
drop user andres;

revoke all privileges on worker from raulalbiol;
revoke all privileges on sesion from raulalbiol;
revoke all privileges on excategory from raulalbiol;
revoke all privileges on instructorcontract from raulalbiol;
revoke all privileges on bitacora from raulalbiol;
revoke all privileges on all sequences in schema public from raulalbiol;
drop user raulalbiol;