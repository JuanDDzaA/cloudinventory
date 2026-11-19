import streamlit as st
from supabase import create_client

st.set_page_config(page_title="CloudInventory", page_icon="📦", layout="wide")
st.title("📦 CloudInventory")
st.caption("Inventario en la nube · Python · Streamlit · Supabase")

try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_ANON_KEY"]
except (KeyError, FileNotFoundError):
    st.error("Configura SUPABASE_URL y SUPABASE_ANON_KEY en .streamlit/secrets.toml")
    st.stop()

# Cliente separado por sesión: nunca compartir tokens de usuarios en caché global.
if "db" not in st.session_state:
    st.session_state.db = create_client(url, key)
db = st.session_state.db

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    tab1, tab2 = st.tabs(["Iniciar sesión", "Crear cuenta"])
    with tab1:
        with st.form("login"):
            email = st.text_input("Correo", key="login_email")
            password = st.text_input("Contraseña", type="password", key="login_password")
            submitted = st.form_submit_button("Entrar")
        if submitted:
            try:
                result = db.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = result.user.id
                db.table("access_logs").insert({"user_id": result.user.id, "event": "login"}).execute()
                st.rerun()
            except Exception:
                st.error("No se pudo iniciar sesión. Revisa tus credenciales y confirma el correo si es necesario.")
    with tab2:
        with st.form("register"):
            new_email = st.text_input("Correo", key="register_email")
            new_password = st.text_input("Contraseña (mínimo 6 caracteres)", type="password", key="register_password")
            registered = st.form_submit_button("Registrarme")
        if registered:
            try:
                db.auth.sign_up({"email": new_email, "password": new_password})
                st.success("Cuenta creada. Si Supabase requiere confirmar el correo, revisa tu bandeja antes de iniciar sesión.")
            except Exception as exc:
                st.error(f"Error al registrarse: {exc}")

                
    st.stop()

user_id = st.session_state.user
with st.sidebar:
    st.success("Sesión iniciada")
    if st.button("Cerrar sesión"):
        try:
            db.table("access_logs").insert({"user_id": user_id, "event": "logout"}).execute()
        except Exception:
            pass
        db.auth.sign_out()
        st.session_state.user = None
        st.rerun()

st.subheader("Agregar producto")
with st.form("new_product", clear_on_submit=True):
    name = st.text_input("Nombre del producto")
    quantity = st.number_input("Cantidad", min_value=0, step=1)
    price = st.number_input("Precio", min_value=0.0, step=100.0)
    add = st.form_submit_button("Guardar producto")
if add:
    if not name.strip():
        st.warning("Escribe un nombre.")
    else:
        try:
            db.table("products").insert({"user_id": user_id, "name": name.strip(), "quantity": int(quantity), "price": float(price)}).execute()
            st.success("Producto guardado")
        except Exception as exc:
            st.error(f"Error al guardar: {exc}")

st.subheader("Inventario")
try:
    products = db.table("products").select("id,name,quantity,price,created_at").eq("user_id", user_id).order("id", desc=True).execute().data
    if products:
        st.dataframe([{"ID": p["id"], "Producto": p["name"], "Cantidad": p["quantity"], "Precio": float(p["price"])} for p in products], use_container_width=True, hide_index=True)
        options = {f'{p["id"]} · {p["name"]}': p["id"] for p in products}
        selected = st.selectbox("Producto a eliminar", list(options))
        if st.button("Eliminar producto"):
            db.table("products").delete().eq("id", options[selected]).eq("user_id", user_id).execute()
            st.rerun()
    else:
        st.info("Aún no tienes productos. Agrega el primero.")
except Exception as exc:
    st.error(f"Error al cargar inventario: {exc}")

with st.expander("🔒 Historial de seguridad (accesos)"):
    try:
        logs = db.table("access_logs").select("event,created_at").eq("user_id", user_id).order("created_at", desc=True).limit(20).execute().data
        st.dataframe(logs, use_container_width=True, hide_index=True)
    except Exception as exc:
        st.error(f"Error al consultar registros: {exc}")
