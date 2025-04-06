"""Modulos para conectar con la base de datos y ocultar la contraseña al escribir."""

import logging
import getpass
import psycopg2


# Configuración de conexión a la base de datos en Docker definidos en docker-compose.yaml
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "credenciales"
DB_USER = "Admin"
DB_PASSWORD = "p4ssw0rdDB"


class Transacciones:
    """_summary_
    Clase que se conecta con un contenedor de Docker y Postgresql
    Returns:
        _type_: _description_
    """

    def __init__(self):
        pass

    def conectar_db(self):
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
            logger.debug("Error al conecta la BD: %s", e)
            print("Error al conectar con la BD")
            return None
        except Exception as e:
            if 'conn' in locals():
                conn.rollback()
            logger.debug("Error al conecta la BD %s", e)
            print("Error al conecta la BD")
            return None

    def agregar_usuario(self):
        """Agrega un nuevo usuario a la base de datos."""
        conn = self.conectar_db()
        if not conn:
            return

        try:
            cursor = conn.cursor()

            # Solicitar datos del nuevo usuario
            nombre = input("Ingrese el nombre del nuevo usuario: ")
            correo = input("Ingrese el correo electrónico del nuevo usuario: ")
            telefono = input("Ingrese el teléfono del nuevo usuario: ")
            fecha_nacimiento_str = input(
                "Ingrese la fecha de nacimiento del nuevo usuario (YYYY-MM-DD): "
            )
            user_name = input("Ingrese el nombre de usuario para la autenticación: ")
            user_password = getpass.getpass(
                "Ingrese la contraseña para la autenticación: "
            )

            # Verificar si el nombre de usuario ya existe
            cursor.execute(
                "SELECT username FROM autenticacion WHERE username = %s", (user_name,)
            )
            if cursor.fetchone():
                print("El nombre de usuario ya existe. Por favor, elija otro.")
                return

            # Insertar datos en la tabla usuarios
            query_usuarios = """
                INSERT INTO usuarios (nombre, correo, telefono, fecha_nacimiento)
                VALUES (%s, %s, %s, %s)
                RETURNING id_usuario;
            """
            cursor.execute(
                query_usuarios, (nombre, correo, telefono, fecha_nacimiento_str)
            )
            id_usuario = cursor.fetchone()[0]

            # Insertar datos en la tabla autenticacion
            query_autenticacion = """
                INSERT INTO autenticacion (id_usuario, username, password_hash)
                VALUES (%s, %s, %s);
            """
            cursor.execute(query_autenticacion, (id_usuario, user_name, user_password))

            conn.commit()
            print(f"Usuario '{nombre}' agregado exitosamente con ID: {id_usuario}.")

        except psycopg2.Error as e:
            conn.rollback()
            logger.debug("Error al agregar el usuario %s", e)
            print("Error al agregar el usuario")
        except Exception as e:
            conn.rollback()
            logger.debug("Error al agregar el usuario %s", e)
            print("Error al agregar el usuario")
        finally:
            cursor.close()
            conn.close()

    def iniciar_sesion(self):
        """Permite al usuario iniciar sesión y retorna True si es exitoso, False de lo contrario."""
        print("\nInicio de sesión en la base de datos")
        username = input("Ingrese su usuario: ")
        password = getpass.getpass("Ingrese su contraseña: ")
        conn = self.conectar_db()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            query = """
                SELECT u.id_usuario
                FROM autenticacion a
                JOIN usuarios u ON a.id_usuario = u.id_usuario
                WHERE a.username = %s AND a.password_hash = %s;
            """
            cursor.execute(query, (username, password))
            usuario = cursor.fetchone()
            if usuario:
                print("Inicio de sesión exitoso.")
                return True
            else:
                print("Usuario o contraseña incorrectos.")
                return False
        except psycopg2.Error as e:
            logger.debug("Error al iniciar sesión: %s", e)
            print("Error al iniciar sesión.")
            return False
        finally:
            cursor.close()
            conn.close()

    def buscar_usuario_por_nombre(self):
        """Busca usuarios por nombre en la base de datos."""
        conn = self.conectar_db()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            nombre_buscar = input("Ingrese el nombre del usuario a buscar: ")
            query = """
                SELECT id_usuario, nombre, correo, telefono, fecha_nacimiento
                FROM usuarios
                WHERE nombre LIKE %s;
            """
            cursor.execute(query, ('%' + nombre_buscar + '%',))
            resultados = cursor.fetchall()
            if resultados:
                print("\nUsuarios encontrados:")
                for usuario in resultados:
                    print(f"ID: {usuario[0]}")
                    print(f"Nombre: {usuario[1]}")
                    print(f"Correo: {usuario[2]}")
                    print(f"Teléfono: {usuario[3]}")
                    print(f"Fecha de Nacimiento: {usuario[4]}")
                    print("-" * 20)
            else:
                print("No se encontraron usuarios con ese nombre.")
        except psycopg2.Error as e:
            logger.debug("Error al buscar usuario por nombre: %s", e)
            print("Error al buscar usuario.")
        finally:
            cursor.close()
            conn.close()

    def listar_todos_los_usuarios(self):
        """Lista todos los usuarios en la base de datos."""
        conn = self.conectar_db()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            query = """
                SELECT id_usuario, nombre, correo, telefono, fecha_nacimiento
                FROM usuarios;
            """
            cursor.execute(query)
            usuarios = cursor.fetchall()
            if usuarios:
                print("\nLista de todos los usuarios:")
                for usuario in usuarios:
                    print(f"ID: {usuario[0]}")
                    print(f"Nombre: {usuario[1]}")
                    print(f"Correo: {usuario[2]}")
                    print(f"Teléfono: {usuario[3]}")
                    print(f"Fecha de Nacimiento: {usuario[4]}")
                    print("-" * 20)
            else:
                print("No hay usuarios registrados en la base de datos.")
        except psycopg2.Error as e:
            logger.debug("Error al listar usuarios: %s", e)
            print("Error al listar usuarios.")
        finally:
            cursor.close()
            conn.close()

    def borrar_usuario(self):
        """Borra un usuario de la base de datos."""
        conn = self.conectar_db()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            id_usuario_borrar = input("Ingrese el ID del usuario que desea borrar: ")

            # Primero, borrar de la tabla de autenticación
            query_autenticacion = "DELETE FROM autenticacion WHERE id_usuario = %s;"
            cursor.execute(query_autenticacion, (id_usuario_borrar,))

            # Luego, borrar de la tabla de usuarios
            query_usuarios = "DELETE FROM usuarios WHERE id_usuario = %s;"
            cursor.execute(query_usuarios, (id_usuario_borrar,))

            conn.commit()
            if cursor.rowcount > 0:
                print(f"Usuario con ID {id_usuario_borrar} borrado exitosamente.")
            else:
                print(f"No se encontró ningún usuario con ID {id_usuario_borrar}.")

        except psycopg2.Error as e:
            conn.rollback()
            logger.debug("Error al borrar usuario: %s", e)
            print("Error al borrar usuario.")
        finally:
            cursor.close()
            conn.close()

    def actualizar_datos_usuario(self):
        """Actualiza los datos de un usuario existente."""
        conn = self.conectar_db()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            id_usuario_actualizar = input("Ingrese el ID del usuario que desea actualizar: ")

            # Verificar si el usuario existe
            cursor.execute("SELECT nombre FROM usuarios WHERE id_usuario = %s", (id_usuario_actualizar,))
            usuario_existe = cursor.fetchone()
            if not usuario_existe:
                print(f"No se encontró ningún usuario con ID {id_usuario_actualizar}.")
                return

            print("\nIngrese los nuevos datos del usuario (deje en blanco para no modificar):")
            nuevo_nombre = input(f"Nuevo nombre ({usuario_existe[0]}): ")
            nuevo_correo = input("Nuevo correo electrónico: ")
            nuevo_telefono = input("Nuevo teléfono: ")
            nueva_fecha_nacimiento = input("Nueva fecha de nacimiento (YYYY-MM-DD): ")

            updates = []
            if nuevo_nombre:
                updates.append(("nombre", nuevo_nombre))
            if nuevo_correo:
                updates.append(("correo", nuevo_correo))
            if nuevo_telefono:
                updates.append(("telefono", nuevo_telefono))
            if nueva_fecha_nacimiento:
                updates.append(("fecha_nacimiento", nueva_fecha_nacimiento))

            if not updates:
                print("No se proporcionaron datos para actualizar.")
                return

            set_clauses = ", ".join([f"{campo} = %s" for campo, _ in updates])
            values = [valor for _, valor in updates]
            values.append(id_usuario_actualizar)

            query = f"""
                UPDATE usuarios
                SET {set_clauses}
                WHERE id_usuario = %s;
            """
            cursor.execute(query, values)
            conn.commit()
            if cursor.rowcount > 0:
                print(f"Datos del usuario con ID {id_usuario_actualizar} actualizados exitosamente.")
            else:
                print("Error al actualizar los datos del usuario.")

        except psycopg2.Error as e:
            conn.rollback()
            logger.debug("Error al actualizar datos del usuario: %s", e)
            print("Error al actualizar datos del usuario.")
        finally:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename="app.log", encoding="utf-8", level=logging.DEBUG)
    transacciones = Transacciones()
    logged_in = False # Al iniciar el programa no se ha iniciado sesion

    while not logged_in:
        print("\n--- Menú de Inicio ---")
        print("1. Iniciar sesión")
        print("2. Salir")

        opcion_inicio = input("Seleccione una opción: ")

        if opcion_inicio == "1":
            logged_in = transacciones.iniciar_sesion()
        elif opcion_inicio == "2":
            print("Saliendo del programa.")
            exit()
        else:
            print("Opción inválida. Por favor, intente de nuevo.")

    while logged_in:
        print("\n--- Menú Principal ---")
        print("1. Buscar usuario por nombre")
        print("2. Listar todos los usuarios")
        print("3. Agregar usuario")
        print("4. Borrar usuario")
        print("5. Actualizar datos de usuario")
        print("6. Cerrar sesión")
        print("7. Salir")

        opcion_menu = input("Seleccione una opción: ")

        if opcion_menu == "1":
            transacciones.buscar_usuario_por_nombre()
        elif opcion_menu == "2":
            transacciones.listar_todos_los_usuarios()
        elif opcion_menu == "3":
            transacciones.agregar_usuario()
        elif opcion_menu == "4":
            transacciones.borrar_usuario()
        elif opcion_menu == "5":
            transacciones.actualizar_datos_usuario()
        elif opcion_menu == "6":
            logged_in = False
            print("Sesión cerrada.")
        elif opcion_menu == "7":
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida. Por favor, intente de nuevo.")
