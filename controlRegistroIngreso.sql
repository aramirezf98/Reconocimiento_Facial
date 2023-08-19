-- Crear la base de datos si no existe
IF NOT EXISTS (SELECT name FROM dbo.sysdatabases WHERE name = 'controDeRegistro')
BEGIN
    CREATE DATABASE controlDeRegistro;
    PRINT 'Base de datos "controDeRegistro" creada correctamente.';
END
ELSE
BEGIN
    PRINT 'La base de datos "controDeRegistro" ya existe.';
END
GO

-- Usar la base de datos "controDeRegistro"
USE controlDeRegistro;
GO

-- Crear la tabla "registros" si no existe
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'registros')
BEGIN
    CREATE TABLE registros (
        usuario VARCHAR(100),
        fechaRegistro datetime
    );
    PRINT 'Tabla "registros" creada correctamente.';
END
ELSE
BEGIN
    PRINT 'La tabla "registros" ya existe.';
END
GO

alter PROCEDURE SP_insertarRegistros
	@usuario VARCHAR(100)
AS
BEGIN
	SET NOCOUNT ON;

	-- Insertar el registro con la fecha y hora actual
	INSERT INTO registros (usuario, fechaRegistro)
	VALUES (@usuario, GETDATE());
END;


-- Crear la tabla "datos_usuario" si no existe
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'datos_usuario')
BEGIN
    CREATE TABLE datos_usuario (
        idUsuario varchar(20) primary key, 
		nombre varchar(45), 
		cedula varchar(10) unique, 
		typo varchar(15),
    );
END

-- Insertar Datos
Insert Into datos_usuario(idUsuario, nombre, cedula, typo) 
values ('asalazar', 'Andrea Salazar', '0956239584', 'Estudiante') 

Insert Into datos_usuario(idUsuario, nombre, cedula, typo) 
values ('aramirez', 'Andres Ramirez', '0986325695', 'Estudiante') 

Insert Into datos_usuario(idUsuario, nombre, cedula, typo) 
values ('achacon', 'Ana Chacon', '0963527415', 'Docente')

Insert Into datos_usuario(idUsuario, nombre, cedula, typo) 
values ('abedon', 'Alex Bedon', '0932123564', 'Estudiante') 


select * from datos_usuario

insert into registros(usuario, fechaRegistro) values ('aramirez', GETDATE())