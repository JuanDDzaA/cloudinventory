# CloudInventory
Sistema de inventario en la nube desarrollado con Streamlit y Supabase PostgreSQL.

## Instalación
1. Crea un proyecto en https://supabase.com y ejecuta `schema.sql` en SQL Editor.
2. En Supabase > Project Settings > API (o Connect), copia Project URL y la clave pública **anon/publishable**. Nunca uses `service_role` ni `secret`.
3. Copia `.streamlit/secrets.toml.example` a `.streamlit/secrets.toml` y completa las credenciales.
4. En la terminal: `py -m pip install -r requirements.txt` y `py -m streamlit run app.py`.
5. Crea una cuenta. Si está activada la confirmación de correo en Supabase Auth, confirma el correo antes de entrar.
6. Sube los archivos a GitHub (sin `secrets.toml`). En https://share.streamlit.io despliega el repositorio y configura las mismas variables en Advanced settings > Secrets.

## Seguridad
Autenticación por Supabase Auth; contraseñas administradas por Supabase; políticas RLS para aislar los productos y accesos de cada usuario; secretos fuera de GitHub.

## Requisitos de la rúbrica
- Internet y nube: despliegue en Streamlit Community Cloud.
- Seguridad: autenticación y registro de inicio/cierre de sesión.
- Base de datos: Supabase PostgreSQL.
- Funcionamiento: registro, listado y eliminación de productos.
