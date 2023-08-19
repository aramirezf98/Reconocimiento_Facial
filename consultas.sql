Select * from registros order by fechaRegistro desc


select * from datos_usuario

select * from datos_usuario du, registros r where du.idUsuario = r.usuario

Select convert(varchar, fechaRegistro, 13) from registros order by fechaRegistro desc

delete from registros where usuario = 'aramirez'