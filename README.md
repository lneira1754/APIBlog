# APIBlog - MiniBlog API

API REST construida con Flask para gestionar un mini blog con roles (admin, moderator, user), autenticación JWT y administración de posts, categorías, comentarios y usuarios.

## Requisitos previos
- Python 3.11 o superior
- MySQL 8 (u otra instancia compatible con `mysql+pymysql`)
- `pip` y `virtualenv`
- (Opcional) `curl` o una herramienta tipo Postman para probar endpoints

## Instalación
1. Clona el repositorio y entra en la carpeta `APIBlog`.
2. Crea y activa un entorno virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # Windows: .venv\\Scripts\\activate
   ```
3. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Configura las variables de entorno. Puedes copiar `.env` (o crear uno nuevo) con al menos:
   ```ini
   DATABASE_URL=mysql+pymysql://root:tu_password@localhost/miniblog_flask
   SECRET_KEY=clave-flask
   JWT_SECRET_KEY=clave-jwt
   ```
   Ajusta credenciales y nombre de base según tu entorno.

## Base de datos
1. Crea la base de datos en MySQL:
   ```sql
   CREATE DATABASE miniblog_flask CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
2. Poblala de una de estas formas:
   - **Migrations**: `flask --app app db upgrade`
   - **Dump**: importa `miniblog_flask.sql` con `mysql -u root -p miniblog_flask < miniblog_flask.sql`
3. (Opcional) Genera usuarios de prueba ejecutando:
   ```bash
   flask --app app shell <<'PY'
   from crear_usuarios_prueba import create_test_users
   create_test_users()
   PY
   ```
   o simplemente `python crear_usuarios_prueba.py` con el entorno virtual activo.

## Cómo ejecutar el proyecto
1. Activa el entorno virtual y asegúrate de tener el `.env` cargado (usa `export $(cat .env | xargs)` en Linux/macOS si lo necesitas).
2. Arranca la app:
   ```bash
   flask --app app run --debug
   ```
   También puedes ejecutar `python app.py` si prefieres evitar la CLI de Flask.
3. El API quedará disponible en `http://localhost:5000`. El front-end autorizado por CORS es `http://localhost:3000`.

## Endpoints principales
Los endpoints se registran bajo el prefijo `/api`. A continuación, un resumen informal (consultá los módulos en `views/` para más detalle).

### Salud
| Método | Ruta | Descripción | Auth |
| --- | --- | --- | --- |
| GET | `/api/health` | Chequeo rápido de la API | Pública |

### Autenticación
| Mét. | Ruta | Descripción | Auth |
| --- | --- | --- | --- |
| POST | `/api/register` | Registro de usuario (`username`, `email`, `password`) | Pública |
| POST | `/api/login` | Devuelve `access_token`, rol y expiración | Pública |
| GET | `/api/profile` | Perfil del usuario autenticado | JWT |

### Posts
| Mét. | Ruta | Descripción | Auth / Rol |
| --- | --- | --- | --- |
| GET | `/api/posts` | Lista posts publicados | Pública |
| POST | `/api/posts` | Crea post (campos `title`, `content`, `categories[]`) | JWT (autor)
| GET | `/api/posts/<id>` | Obtiene post; si no está publicado exige permisos | Pública/JWT
| PUT | `/api/posts/<id>` | Actualiza post propio | JWT + autor
| DELETE | `/api/posts/<id>` | Soft delete (autor o admin) | JWT + autor/admin
| GET | `/api/my-posts` | Posts del usuario autenticado | JWT

### Comentarios
| Mét. | Ruta | Descripción | Auth / Rol |
| --- | --- | --- | --- |
| GET | `/api/posts/<post_id>/comments` | Lista comentarios del post | Pública |
| POST | idem | Crea comentario | JWT |
| DELETE | `/api/comments/<comment_id>` | Autor o admin lo elimina; moderador lo oculta | JWT + rol/autor |

### Categorías
| Mét. | Ruta | Descripción | Auth / Rol |
| --- | --- | --- | --- |
| GET | `/api/categories` | Lista categorías | Pública |
| POST | `/api/categories` | Crea nueva categoría | JWT + admin/moderator |
| GET | `/api/categories/<id>` | Detalle de categoría | Pública |
| PUT | `/api/categories/<id>` | Edita categoría | JWT + admin/moderator |
| DELETE | `/api/categories/<id>` | Elimina categoría sin posts | JWT + admin |

### Usuarios / Administración
| Mét. | Ruta | Descripción | Auth / Rol |
| --- | --- | --- | --- |
| GET | `/api/users` | Lista todos los usuarios | JWT + admin |
| GET | `/api/users/<id>` | Perfil por id (dueño o admin) | JWT + dueño/admin |
| PUT | `/api/users/<id>/role` | Cambia rol (`user`, `moderator`, `admin`) | JWT + admin |
| PUT | `/api/users/<id>/status` | Activa/desactiva usuario | JWT + admin |

### Estadísticas
| Mét. | Ruta | Descripción | Auth / Rol |
| --- | --- | --- | --- |
| GET | `/api/stats` | Métricas generales; admins ven datos detallados | JWT + admin/moderator |

> Tip: hay ejemplos de `curl` en `endpoints_Pruebas.txt` si querés copiar/pegar.

## Credenciales de prueba
Si ejecutaste `crear_usuarios_prueba.py`, tendrás:

| Rol | Email | Usuario | Password | Notas |
| --- | --- | --- | --- | --- |
| admin | `admin@example.com` | `admin` | `admin123` | Acceso total, cambios de rol/estado y eliminación definitiva |
| moderator | `moderator@example.com` | `moderator1` | `mod123` | Puede crear categorías, ver stats básicas y ocultar comentarios |
| user | `user1@example.com` | `user1` | `user123` | Puede crear posts propios y comentar |

Cada token JWT dura 24 h (`JWT_ACCESS_TOKEN_EXPIRES = 86400`). Guarda el `access_token` que devuelve `/api/login` para llamar a los endpoints protegidos usando `Authorization: Bearer <token>`.

## Notas útiles
- Los blueprints viven en `views/` y la lógica en `services/` y `repositories/`.
- `decorators/roles.py` contiene los helpers para verificar roles en cada endpoint.
- Si cambiás `DATABASE_URL`, recordá actualizar `alembic.ini` si usás migraciones.
