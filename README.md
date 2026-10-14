# PFO2 - Sistema de Gestión de Tareas con API y Base de Datos

Sistema que implementa una API REST con Flask, autenticación segura con contraseñas hasheadas y persistencia de datos en SQLite.

## 🚀 Instrucciones para ejecutar el proyecto

### 1. Requisitos previos
- Python 3.8 o superior


### 2. Instalación de dependencias
python -m pip install flask requests


### 3. Ejecutar el servidor
python servidor.py

El servidor quedará disponible en: `http://localhost:5000`

### 4. Probar la API
1. Crear una petición POST a `http://localhost:5000/registro` con body JSON.
2. Crear una petición POST a `http://localhost:5000/login` con body JSON.
3. Crear una petición GET a `http://localhost:5000/tareas`.

#### Opción A: Usando el cliente en consola

python cliente.py 

seguir la instruciones por pantalla.


#### ¿Por qué hashear contraseñas?
Hashear contraseñas es una medida de seguridad fundamental. Si un atacante logra acceso a la base de datos (por ejemplo, mediante una inyección SQL o una filtración), solo verá cadenas de texto irreconocibles (los hashes) en lugar de las contraseñas reales.
A diferencia del cifrado, el hash es una función unidireccional; es computacionalmente inviable revertirlo para obtener el texto original. Además, al usar librerías como werkzeug, se aplica "salt" (sal), lo que protege contra ataques de diccionario y tablas arcoíris.

#### Ventajas de usar SQLite en este proyecto
Cero configuración (Serverless): No requiere instalar ni configurar un servidor de base de datos externo (como MySQL o PostgreSQL). Toda la base de datos es simplemente un archivo local (database.db).
Ligero y Portátil: Es ideal para aplicaciones de tamaño pequeño a mediano, prototipos o entornos de desarrollo, ya que consume mínimos recursos.
Persistencia sencilla: Facilita el respaldo y la migración, ya que solo es necesario copiar el archivo .db para tener toda la información.

