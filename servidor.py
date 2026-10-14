"""
PFO2 - Sistema de Gestión de Tareas con API y Base de Datos
Servidor Flask + SQLite con autenticación segura.
"""

from flask import Flask, request, jsonify, render_template_string
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# ============================================================
# CONFIGURACIÓN INICIAL
# ============================================================
app = Flask(__name__)
DB_NAME = "tareas.db"

# HTML de bienvenida para GET /tareas
HTML_BIENVENIDA = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Gestión de Tareas</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
        h1 { color: #2c3e50; }
        p { color: #555; }
    </style>
</head>
<body>
    <h1>¡Bienvenido al Sistema de Gestión de Tareas!</h1>
    <p>Has accedido correctamente a la API. Desde aquí podrás administrar tus tareas diarias.</p>
</body>
</html>
"""

# ============================================================
# FUNCIONES DE BASE DE DATOS
# ============================================================
def get_db():
    """Establece y devuelve la conexión a SQLite."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Para acceder a columnas por nombre
    return conn

def init_db():
    """Crea la tabla 'usuarios' si no existe."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                contraseña TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
        print("✓ Base de datos inicializada correctamente.")
    except sqlite3.Error as e:
        print(f"✗ Error al inicializar la base de datos: {e}")
        raise

# ============================================================
# ENDPOINTS
# ============================================================
@app.route('/registro', methods=['POST'])
def registro():
    """
    Endpoint: POST /registro
    Recibe: {"usuario": "nombre", "contraseña": "1234"}
    Almacena el usuario con la contraseña hasheada.
    """
    data = request.get_json()
    
    # Validación de datos
    if not data or 'usuario' not in data or 'contraseña' not in data:
        return jsonify({"error": "Debe enviar 'usuario' y 'contraseña'"}), 400
    
    usuario = data['usuario']
    contraseña_plano = data['contraseña']
    
    # Hashear la contraseña (¡NUNCA en texto plano!)
    hashed_pw = generate_password_hash(contraseña_plano)
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)',
            (usuario, hashed_pw)
        )
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    """
    Endpoint: POST /login
    Recibe: {"usuario": "nombre", "contraseña": "1234"}
    Verifica las credenciales.
    """
    data = request.get_json()
    
    if not data or 'usuario' not in data or 'contraseña' not in data:
        return jsonify({"error": "Debe enviar 'usuario' y 'contraseña'"}), 400
    
    usuario = data['usuario']
    contraseña_plano = data['contraseña']
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE usuario = ?', (usuario,))
    user = cursor.fetchone()
    conn.close()
    
    # Verificar el hash
    if user and check_password_hash(user['contraseña'], contraseña_plano):
        return jsonify({
            "mensaje": "Inicio de sesión exitoso",
            "usuario": usuario
        }), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

@app.route('/tareas', methods=['GET'])
def tareas():
    """
    Endpoint: GET /tareas
    Muestra un HTML de bienvenida al usuario.
    """
    return render_template_string(HTML_BIENVENIDA)

# ============================================================
# BLOQUE PRINCIPAL
# ============================================================
if __name__ == '__main__':
    init_db()  # Prepara la base de datos al iniciar
    print("🚀 Servidor Flask corriendo en http://localhost:5000")
    app.run(debug=True, port=5000)