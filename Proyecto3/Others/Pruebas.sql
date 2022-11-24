select * from sesionuser;
select p.sesiondate,p.sesionhour,p.timelength,exercisetype,p.description,p.workername,userweight,heartrate,caloriesacomplished from sesionuser
inner join (
    select sesioncode,sesionname,sesiondate,sesionhour,timelength,description,worker.workername
    from sesion
    inner join worker
    on worker.workerid = sesion.workerid
) as p
on p.sesioncode = sesionuser.sesioncode
where userid = 'alejandro';
select avg(userweight) from sesionuser where sesionuser.userid = 'alejandro';
select * from sesionuser;
select p.sesiondate,p.sesionhour,p.timelength,exercisetype,p.description,p.workername,userweight,heartrate,caloriesacomplished from sesionuser
inner join (
    select sesioncode,sesionname,sesiondate,sesionhour,timelength,description,worker.workername
    from sesion
    inner join worker
    on worker.workerid = sesion.workerid
) as p
on p.sesioncode = sesionuser.sesioncode
where userid = 'alejandro';
select current_date + interval '3 week'
-- Creacion de la vista de stats
create view stadium_stats as
select a.description, a.codigo_de_estadio,a.goles
from (
    select 'Estadio donde se marcan mas goles: ' as description,estadio.cod_estadio as codigo_de_estadio,estadio.capacidad, k.tot_goles as goles
    from estadio
    inner join 
    (
        select p.cod_estadio, sum(p.goles) as tot_goles
        from (    
            select codigo_juego,cod_estadio,marcador_visitante as goles
            from juego
            union all
            select codigo_juego, cod_estadio, marcador_casa
            from juego
        ) as p
        group by p.cod_estadio
    ) as k
    on estadio.cod_estadio = k.cod_estadio
    order by goles desc
    LIMIT 1
)as a
union all
select b.description, b.codigo_de_estadio,b.goles
from (
    select 'Estadio donde se marcan menos goles: ' as description,estadio.cod_estadio as codigo_de_estadio,estadio.capacidad, k.tot_goles as goles
    from estadio
    inner join 
    (
        select p.cod_estadio, sum(p.goles) as tot_goles
        from (    
            select codigo_juego,cod_estadio,marcador_visitante as goles
            from juego
            union all
            select codigo_juego, cod_estadio, marcador_casa
            from juego
        ) as p
        group by p.cod_estadio
    ) as k
    on estadio.cod_estadio = k.cod_estadio
    order by goles asc
    LIMIT 1
) as b
union all
select c.description, c.codigo_de_estadio,c.goles
from (
    select 'Estadio donde se la visita suele perder: ' as description,estadio.cod_estadio as codigo_de_estadio,estadio.capacidad, k.tot_goles as goles
    from estadio
    inner join 
    (
        select p.cod_estadio, sum(p.goles) as tot_goles
        from (    
            select codigo_juego,cod_estadio,marcador_visitante as goles
            from juego
            where marcador_visitante>marcador_casa
        ) as p
        group by p.cod_estadio
    ) as k
    on estadio.cod_estadio = k.cod_estadio
    order by goles asc
    LIMIT 1
) as c
union all
select d.description, d.codigo_de_estadio,d.goles
from (
    select 'Estadio donde se la casa suele perder: ' as description,estadio.cod_estadio as codigo_de_estadio,estadio.capacidad, k.tot_goles as goles
    from estadio
    inner join 
    (
        select p.cod_estadio, sum(p.goles) as tot_goles
        from (    
            select codigo_juego,cod_estadio,marcador_visitante as goles
            from juego
            where marcador_visitante<marcador_casa
        ) as p
        group by p.cod_estadio
    ) as k
    on estadio.cod_estadio = k.cod_estadio
    order by goles asc
    LIMIT 1
)as d

select * from sesionuser
select * from sesion
inner join (
    select count(sesionuser.userid), sesioncode from sesionuser
    group by sesioncode
) as p
on p.sesioncode = sesion.sesioncode

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
where sesion.sesionhour<'18:00:00' and sesion.sesionhour>'09:00:00' and sesion.sesiondate = '2022-11-23'
Limit 5


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
where sesion.sesionhour<'18:00:00' and sesion.sesionhour>'09:00:00' and sesion.sesiondate = '2022-11-23'
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

select * from sesion
create view top_10_most_instructors as
select workername, count(s.workerid) from worker inner join (select s.sesioncode, s.workerid, uc.userid from sesion as s inner join (select userid, sesioncode from sesionuser ) as uc on uc.sesioncode = s.sesioncode) as s on s.workerid=worker.workerid group by workername Limit 10;
