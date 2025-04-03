# Práctica de Docker y PosgreSQL

## 0. Introducción

**Docker** es una plataforma que permite crear, desplegar y ejecutar aplicaciones en contenedores. Los contenedores son entornos ligeros y portátiles que permiten ejecutar aplicaciones de manera aislada del sistema operativo subyacente. Esto facilita la implementación y escalabilidad de aplicaciones en diferentes entornos.

**PostgreSQL** es un sistema de gestión de bases de datos relacional y objeto que permite almacenar y gestionar datos de manera eficiente. Es ampliamente utilizado en aplicaciones web y empresariales debido a su robustez y flexibilidad.

**Docker Compose** es una herramienta que permite definir y ejecutar aplicaciones compuestas por múltiples contenedores. Con Docker Compose, se puede definir la configuración de tus contenedores en un archivo YAML y luego iniciar y detener todos los contenedores con un solo comando.

**Docker** y **PostgreSQL** son herramientas muy útiles para el desarrollo y despliegue de aplicaciones. Docker permite crear entornos de desarrollo y producción consistentes, mientras que PostgreSQL proporciona una base de datos robusta y escalable para almacenar datos. Juntas, estas herramientas facilitan la creación y gestión de aplicaciones modernas.

**Python** es un lenguaje de programación de alto nivel que se utiliza ampliamente en el desarrollo web, la ciencia de datos y la inteligencia artificial. Es conocido por su simplicidad y legibilidad, lo que lo convierte en una excelente opción para principiantes y desarrolladores experimentados.


## 0.1. Objetivo

En esta práctica, se aprenderá a crear un contenedor de **PostgreSQL** usando **Docker** y **Docker Compose**. También se aprenderá a conectarse a la base de datos desde **Python** usando la librería **psycopg2** y a consultar datos de la base de datos.


## 1. Verificar que Docker y Docker Compose están instalados

Para verificar que Docker y Docker Compose están instalados, se pueden usar los siguientes comandos:

```bash
docker --version
```

Si se muestra un mensaje similar a este, significa que Docker está instalado correctamente:

```bash
Docker version 27.5.1-1, build 9f9e4058019a37304dc6572ffcbb409d529b59d8
```
Para verificar que Docker Compose está instalado, se puede usar el siguiente comando:

```bash
docker-compose --version
```
Si se muestra un mensaje similar a este, significa que Docker Compose está instalado correctamente:

```bash
Docker Compose version v2.34.0
```

## 2. Crear el Dockerfile

Crear un archivo llamado `Dockerfile`, este archivo contiene las instrucciones necesarias para crear un contenedor con postgresql, además llama a los archivos **init.sql** que creará la estructura básica de la base de datos, y el archivo **save_data.sql** que contiene datos de prueba. Copiar el siguiente contenido en el archivo:

```dockerfile
# Usa la imagen oficial de PostgreSQL
FROM postgres:latest

# Copia el script SQL al directorio de inicialización de PostgreSQL
COPY init.sql /docker-entrypoint-initdb.d/
COPY save_data.sql /docker-entrypoint-initdb.d/
# PostgreSQL ejecutará automáticamente los scripts en /docker-entrypoint-initdb.d/
```

## 3. Crear el archivo docker-compose.yml

Crear un archivo llamado `docker-compose.yml` en el directorio de trabajo y copiar el siguiente contenido:

```yaml
services:
  postgres:
    build: . #Construir contenedor usando Dockerfile presente en el directorio actual (.)
    container_name: ContDBpractMod3 # Nombre del contenedor
    ports:
      - "5432:5432" # Puerto para conectar desde tu máquina host al contenedor
    environment:
      POSTGRES_USER: Admin # Usuario de la base de datos
      POSTGRES_PASSWORD: p4ssw0rdDB # Contraseña del usuario
      POSTGRES_DB: credenciales # Nombre de la base de datos
    volumes:
      - postgres_data:/var/lib/postgresql/data # Espacio donde los datos se conservarán, al detener el contenedor.
volumes:
  postgres_data:
    driver: local
```

## 4. Crear el archivo de inicialización

Crear un archivo llamado `init.sql` en el mismo directorio y copiar el siguiente contenido:

```sql
-- Crear la tabla para almacenar datos de usuarios
CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(255) UNIQUE,
    telefono VARCHAR(15),
    fecha_nacimiento DATE
);

-- Crear la tabla para almacenar usuarios y contraseñas
CREATE TABLE credenciales (
    id_credencial SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario)
);
```

## 5. Crear el archivo de con datos de prueba

Crear un archivo llamado `save_data.sql` en el mismo directorio y copiar el siguiente contenido:

```sql
-- Insertar datos en la tabla usuarios
INSERT INTO usuarios (nombre, correo, telefono, fecha_nacimiento)
VALUES
('Juan Pérez', 'juan.perez1@example.com', '1234567890', '1985-01-15');

-- Insertar datos en la tabla credenciales
INSERT INTO credenciales (id_usuario, username, password_hash)
VALUES
(1, 'juan.perez1', 'hash_juan_perez');
```


## 6. Crear el contendor de PostgreSQL

Primero se crea el contendor de **PostgreSQL** con el siguiente comando:

```bash
docker-compose up -d
```


Esto creará el contenedor y lo ejecutará en segundo plano. Se peude verificar que el contenedor se está ejecutando correctamente con el siguiente comando:

```bash
docker ps
```

Esto mostrará una lista de los contenedores en ejecución. Se debería  ver algo como esto:

```bash
CONTAINER ID   IMAGE                      COMMAND                  CREATED        STATUS         PORTS                                       NAMES
45e3a2e30e00   dbconfiguration-postgres   "docker-entrypoint.s…"   20 hours ago   Up 4 seconds   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   ContDBpractMod3
```

Esto indica que el contenedor se está ejecutando correctamente.


## 7. Conectar con el contenedor

Una vez creado el contenedor, se puede conectar a él usando el siguiente comando:

```bash
docker exec -it ContDBpractMod3 bash
```

Esto abrirá una terminal dentro del contenedor. Desde aquí, se pueden ejecutar comandos de PostgreSQL.

```bash
root@45e3a2e30e00:/# 
```

## 8. Conectar a la base de datos

Para conectarte a la base de datos **credenciales** como el usuario **Admin**, se puede usar el siguiente comando:

```bash
psql -U Admin -d credenciales
```

Esto abrirá una consola de PostgreSQL donde es posible ejecutar comandos SQL.

```bash
root@45e3a2e30e00:/# psql -U Admin -d credenciales
psql (17.4 (Debian 17.4-1.pgdg120+2))
Type "help" for help.

credenciales=# 
```

## 9. Consultar la base de datos

Prara consultar la base de datos, se usan los siguientes comandos SQL:

```sql
SELECT * FROM usuarios;
```
Esto mostrará todos los registros de la tabla **usuarios**.

```sql
credenciales=# SELECT * FROM usuarios;
 id_usuario |     nombre      |            correo             |  telefono  | fecha_nacimiento
------------+-----------------+-------------------------------+------------+------------------
          1 | Juan Pérez      | juan.perez1@example.com       | 1234567890 | 1985-01-15
          2 | Ana Gómez       | ana.gomez2@example.com        | 1234567891 | 1990-03-22
          3 | Luis Martínez   | luis.martinez3@example.com    | 1234567892 | 1988-07-10
          4 | María López     | maria.lopez4@example.com      | 1234567893 | 1992-11-05
          5 | Carlos Ruiz     | carlos.ruiz5@example.com      | 1234567894 | 1980-06-25
          6 | Sofía Castro    | sofia.castro6@example.com     | 1234567895 | 1995-02-18
          7 | David Ramírez   | david.ramirez7@example.com    | 1234567896 | 1983-09-09
          8 | Elena Ortega    | elena.ortega8@example.com     | 1234567897 | 1991-05-03
          9 | Miguel Torres   | miguel.torres9@example.com    | 1234567898 | 1993-12-14
         10 | Laura Sánchez   | laura.sanchez10@example.com   | 1234567899 | 1987-08-01
         11 | Pedro Morales   | pedro.morales11@example.com   | 1234567800 | 1986-04-17
         12 | Clara Hernández | clara.hernandez12@example.com | 1234567801 | 1994-06-30
         13 | Jorge Rojas     | jorge.rojas13@example.com     | 1234567802 | 1981-03-25
         14 | Valeria Peña    | valeria.pena14@example.com    | 1234567803 | 1992-01-09
         15 | Andrés Romero   | andres.romero15@example.com   | 1234567804 | 1989-10-12
         16 | Camila Paredes  | camila.paredes16@example.com  | 1234567805 | 1997-11-19
         17 | Ricardo Vargas  | ricardo.vargas17@example.com  | 1234567806 | 1984-07-23
         18 | Daniela Flores  | daniela.flores18@example.com  | 1234567807 | 1996-03-01
         19 | Héctor Serrano  | hector.serrano19@example.com  | 1234567808 | 1982-02-11
         20 | Patricia Vega   | patricia.vega20@example.com   | 1234567809 | 1990-09-05
(20 rows)

credenciales=#
```

Para consultar la tabla **credenciales**, se usa el siguiente comando SQL:

```sql
SELECT * FROM credenciales;
```

Esto mostrará todos los registros de la tabla **credenciales**.

```sql
credenciales=# SELECT * FROM credenciales;
 id_credencial | id_usuario |     username      |    password_hash
---------------+------------+-------------------+----------------------
             1 |          1 | juan.perez1       | hash_juan_perez
             2 |          2 | ana.gomez2        | hash_ana_gomez
             3 |          3 | luis.martinez3    | hash_luis_martinez
             4 |          4 | maria.lopez4      | hash_maria_lopez
             5 |          5 | carlos.ruiz5      | hash_carlos_ruiz
             6 |          6 | sofia.castro6     | hash_sofia_castro
             7 |          7 | david.ramirez7    | hash_david_ramirez
             8 |          8 | elena.ortega8     | hash_elena_ortega
             9 |          9 | miguel.torres9    | hash_miguel_torres
            10 |         10 | laura.sanchez10   | hash_laura_sanchez
            11 |         11 | pedro.morales11   | hash_pedro_morales
            12 |         12 | clara.hernandez12 | hash_clara_hernandez
            13 |         13 | jorge.rojas13     | hash_jorge_rojas
            14 |         14 | valeria.pena14    | hash_valeria_pena
            15 |         15 | andres.romero15   | hash_andres_romero
            16 |         16 | camila.paredes16  | hash_camila_paredes
            17 |         17 | ricardo.vargas17  | hash_ricardo_vargas
            18 |         18 | daniela.flores18  | hash_daniela_flores
            19 |         19 | hector.serrano19  | hash_hector_serrano
            20 |         20 | patricia.vega20   | hash_patricia_vega
(20 rows)

credenciales=#
```

Para salir de la consola de PostgreSQL, se usa el siguiente comando:

```sql
exit
```

Para salir de la terminal del contenedor, se usa el siguiente comando:

```bash
exit
```


## 10. Crear un virtualenv para instalar las librerías necesarias

Crear un virtualenv, este permitira instalar las liberías **psycopg2** necesarias para conectarse con la base de datos.

Se puede usar el siguiente comando para su creación:

```bash
python3 -m venv .venv
```
## 9. Activar el virtualenv

Para activar el virtualenv, se usa el siguiente comando:

```bash
source .venv/bin/activate
```
## 10. Instalar las librerías necesarias

Una vez que el virtualenv está activado, se pueden instalar las librerías necesarias. En este caso, la librería necesaria es **psycopg2**, que es un adaptador de PostgreSQL para Python. Esta librería permite interactuar con bases de datos PostgreSQL desde Python.

Para instalar las librerías necesarias, se usa el siguiente comando:

```bash
pip install psycopg2
```

## 11. Crear el archivo de conexión a la base de datos

Crear un archivo llamado `acceso.py` y copiar el siguiente contenido:

```python
"""Modulos para conectar con la base de datos y ocultar la contraseña al escribir."""

import getpass
import psycopg2

# Configuración de conexión a la base de datos en Docker definidos en docker-compose.yaml
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "credenciales"
DB_USER = "Admin"
DB_PASSWORD = "p4ssw0rdDB"


def conectar_db():
    """Conecta a la base de datos PostgreSQL y retorna la conexión."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error al conectar con la BD: {e}")
        return None


def obtener_datos_usuario(user_name, user_password):
    """
    Consulta la base de datos para obtener los datos de un usuario a
    partir de sus credenciales.
    """
    conn = conectar_db()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        # Verificar si el suario y contraseña existen en la tabla credenciales
        query = """
            SELECT u.id_usuario, u.nombre, u.correo, u.telefono, u.fecha_nacimiento
            FROM credenciales c
            JOIN usuarios u ON c.id_usuario = u.id_usuario
            WHERE c.username = %s AND c.password_hash = %s;
        """
        cursor.execute(query, (user_name, user_password))
        usuario = cursor.fetchone()
        if usuario:
            print("\nDatos del usuario encontrado:")
            print(f"ID: {usuario[0]}")
            print(f"Nombre: {usuario[1]}")
            print(f"Correo: {usuario[2]}")
            print(f"Teléfono: {usuario[3]}")
            print(f"Fecha de Nacimiento: {usuario[4]}")
        else:
            print("\nUsuario o contraseña incorrectos.")

        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error al consultar la base de datos: {e}")


if __name__ == "__main__":
    print("Inicio de sesión en la base de datos")

    # Solicitar credenciales al usuario
    username = input("Ingrese su usuario: ")
    password = getpass.getpass(
        "Ingrese su contraseña: "
    )  # No muestra la contraseña al escribir

    # Consultar la base de datos
    obtener_datos_usuario(username, password)
```
## 12. Ejecutar el archivo de conexión a la base de datos

Para ejecutar el archivo de conexión a la base de datos, se usa el siguiente comando:

```bash
python3 acceso.py
```

Esto ejecutará el script y pedirá que ingresar un nombre de usuario y contraseña. Si las credenciales son correctas, mostrará los datos del usuario.

```bash
Inicio de sesión en la base de datos
Ingrese su usuario: juan.perez1
Ingrese su contraseña:

Datos del usuario encontrado:
ID: 1
Nombre: Juan Pérez
Correo: juan.perez1@example.com
Teléfono: 1234567890
Fecha de Nacimiento: 1985-01-15
```
Si las credenciales son incorrectas, mostrará un mensaje de error.

```bash
Inicio de sesión en la base de datos
Ingrese su usuario: juan.perez1
Ingrese su contraseña:

Usuario o contraseña incorrectos.
```

Si el contenedor de PostgreSQL no está en ejecución, mostrará un mensaje de error.

```bash
Inicio de sesión en la base de datos
Ingrese su usuario: juan.perez1
Ingrese su contraseña:
Error al conectar con la BD: could not connect to server: Connection refused
        Is the server running on host "localhost" (::1) and accepting
        TCP/IP connections on port 5432?
could not connect to server: Connection refused
        Is the server running on host "localhost" (127.0.0.1) and accepting
        TCP/IP connections on port 5432?
```
Esto indica que el contenedor de PostgreSQL no está en ejecución o que la configuración de conexión es incorrecta.


## 12. Crear un archivo de requerimientos

Crear un archivo llamado `requirements.txt` y copiar el siguiente contenido:

```bash
pip freeze > requirements.txt
```

Esto permitirá instalar las librerías necesarias en el futuro.


## 13. Instalar las librerías necesarias desde el archivo de requerimientos

Para instalar las librerías necesarias desde el archivo de requerimientos, se puede usar el siguiente comando:

```bash
pip install -r requirements.txt
```

Esto instalará todas las librerías listadas en el archivo `requirements.txt`.

## 13. Detener el contenedor

Para detener el contenedor, se usa el siguiente comando:

```bash
docker-compose down
```

Esto detendrá y eliminará el contenedor de PostgreSQL. Se puede verificar que el contenedor se ha detenido correctamente con el siguiente comando:

```bash
docker ps
```
Esto no mostrará el contenedor de PostgreSQL, lo que indica que se ha detenido correctamente.

```bash
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

Esto indica que el contenedor se ha detenido correctamente.

##  14. Conclusiones

1. En esta práctica, he aprendido a crear un contenedor de PostgreSQL usando Docker y Docker Compose.
2. También he aprendido a conectarme a la base de datos desde Python usando la librería **psycopg2** y a consultar datos de la base de datos.
3. Además, he aprendido a crear un archivo de requerimientos para instalar las librerías necesarias en el futuro.
4. También he aprendido a detener y eliminar el contenedor de PostgreSQL.
5. Esta práctica es útil para aprender a trabajar con bases de datos en un entorno de desarrollo y producción.

## 15. Recursos adicionales

- [Documentación de Docker](https://docs.docker.com/)
- [Documentación de Docker Compose](https://docs.docker.com/compose/)
- [Documentación de psycopg2](https://www.psycopg.org/docs/)
- [Documentación de PostgreSQL](https://www.postgresql.org/docs/)
- [Documentación de Python](https://docs.python.org/3/)
- [Documentación de SQL](https://www.w3schools.com/sql/)
