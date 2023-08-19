from datetime import datetime
import pyodbc


server = 'COGNITO\SQLSERVER'
database = 'controlDeRegistro'
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

def obtener_datos(usuario):
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM datos_usuario WHERE idUsuario=? ", usuario)
        datos = cursor.fetchone()
        cursor.close()
        conn.close()

        return datos
    except pyodbc.Error as e:
        print("Error de conexión o ejecución:", e)


def insertar_registro(usuario):
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("EXEC SP_insertarRegistros @usuario=?", usuario)
        conn.commit()
        cursor.close()
        conn.close()

    except pyodbc.Error as e:
        print("Error de conexión o ejecución:", e)

def obtener_ultimo_registro(usuario):
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 1 fechaRegistro  FROM registros WHERE usuario = ? ORDER BY fechaRegistro DESC", usuario)
        last_record = cursor.fetchone()
        cursor.close()
        conn.close()

        datetimeObject = datetime.strptime(str(last_record.fechaRegistro), "%Y-%m-%d %H:%M:%S.%f")
        fecha_formato = datetimeObject.strftime("%Y-%m-%d %H:%M:%S")

        return fecha_formato
    except pyodbc.Error as e:
        print("Error de conexión o consulta:", e)


#ultimo_registro = obtener_ultimo_registro('asalazar')
#datetimeObject = datetime.strptime(str(ultimo_registro.fechaRegistro), "%Y-%m-%d %H:%M:%S.%f")
#fecha_formato = datetimeObject.strftime("%Y-%m-%d %H:%M:%S")
#print(fecha_formato)

#registro = datetime.strptime(obtener_ultimo_registro('asalazar'), "%Y-%m-%d %H:%M:%S")
#print(type(registro))
#print(type(obtener_ultimo_registro('asalazar')))
