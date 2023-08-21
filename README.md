# Reconocimiento_Facial
Proyecto de Reconocimiento facial para el control de ingreso a una institución

Este es un proyecto con la finalidad de proporcionar un registro de ingreso, valiando la identidad del usuario si se encuentra o no en la base de datos.
se usaron dos bases de datos, Firebase para las imagenes y sql para los datos y el registro de las personas.

Main.py 
es el archivo principal 

EncodeGenerator.py
es el archivo que genera el archivo encode.p donde se guardan todos los rostros en el archivo. Antes de ejecutar este codigo debes tenerla base de datos de firebase
y tener activo el "Storage" donde se van a guardar las imagenes que tengas de los usuarios en la direccion de tu carpeta.

prueba.py 
es donde tenemos la conexion a la base de datos y las funciones donde realizaremos las consultas a la base de datos sql.
