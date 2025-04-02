# Practica de Docker y PosgreSQL


## 1. Crear el contendor de PostgreSQL

Primero se crea el contendor de PostgreSQL con el siguiente comando:

```bash
docker-compose up -d
```

## Conectar con el contenedor

Una vez creado el contenedor, puedes conectarte a él usando el siguiente comando:

```bash
docker exec -it ContDBpractMod3 bash
```

## Conectar a la base de datos

Para conectarte a la base de datos **credenciales** como el usuario **Admin**, puedes usar el siguiente comando:

```bash
psql -U Admin -d credenciales
```

## Consultar la base de datos

Prara consultar la base de datos, puedes usar los siguientes comandos SQL:

```sql
SELECT * FROM usuarios;
```

```sql
SELECT * FROM credenciales;
```

