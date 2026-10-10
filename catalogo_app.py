import streamlit as st
import pandas as pd
import urllib.parse
import glob

# Configuración de página
st.set_page_config(page_title="Catálogo Fábrica Taira", layout="wide", initial_sidebar_state="collapsed")

# Estilos CSS personalizados para imitar el PDF
st.markdown('''
<style>
    /* Fondo general */
    .stApp {
        background-color: #FDF1B8; /* Color crema amarillento del PDF */
    }
    
    /* Títulos principales */
    h1 {
        color: #E62429; /* Rojo de Taira */
        text-align: center;
        font-family: 'Arial Black', sans-serif;
        text-transform: uppercase;
        font-weight: 900;
        margin-bottom: 0px;
        padding-bottom: 0px;
        font-size: 3rem !important;
    }
    
    /* Subtítulos */
    h3 {
        color: #E62429;
        font-weight: bold;
    }
    
    /* Textos informativos del encabezado */
    .info-header {
        text-align: center;
        color: #333333;
        font-size: 1.1rem;
        font-weight: bold;
        margin-top: 5px;
    }
    .info-promo {
        text-align: center;
        color: #E62429;
        font-size: 1.2rem;
        font-weight: bold;
        background-color: white;
        padding: 10px;
        border-radius: 10px;
        border: 2px solid #E62429;
        margin-bottom: 20px;
    }
    
    /* Tarjetas de productos */
    .product-card {
        background-color: white;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border: 1px solid #ffcccc;
    }
    
    /* Precio destacado */
    .price-tag {
        color: #E62429;
        font-size: 1.4rem;
        font-weight: bold;
    }
    
    /* Título de sección (ej. COLLARES) */
    .section-title {
        color: #FFB6C1; /* Rosa pastel con borde rojo */
        text-shadow: -1px -1px 0 #E62429, 1px -1px 0 #E62429, -1px 1px 0 #E62429, 1px 1px 0 #E62429;
        font-size: 3rem;
        font-weight: 900;
        text-align: center;
        text-transform: uppercase;
        margin: 30px 0 20px 0;
        letter-spacing: 2px;
    }
    
    /* Botón WhatsApp */
    .whatsapp-btn {
        background-color: #25D366;
        color: white !important;
        padding: 15px;
        text-align: center;
        border-radius: 8px;
        font-size: 18px;
        font-weight: bold;
        text-decoration: none;
        display: block;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .whatsapp-btn:hover {
        background-color: #128C7E;
    }
</style>
''', unsafe_allow_html=True)

# Encabezado estilo PDF
st.markdown("<h1>TAIRA</h1>", unsafe_allow_html=True)
st.markdown("<div class='info-header'>FÁBRICA Y DISTRIBUIDORA<br>Calidad y originalidad<br>CATÁLOGO VETERINARIAS/PET-SHOP</div>", unsafe_allow_html=True)
st.markdown("<div class='info-header' style='font-size:0.9rem;'>Los precios están sujetos a modificaciones</div>", unsafe_allow_html=True)
st.markdown("<div class='info-promo'>Envíos gratis A TODO EL PAÍS a partir de $500.000<br>Envíos gratis AL INTERIOR DE MISIONES a partir de $150.000</div>", unsafe_allow_html=True)


@st.cache_data
def cargar_datos():
    archivos = glob.glob("*.xlsx")
    for archivo in archivos:
        try:
            df = pd.read_excel(archivo)
            
            # Buscar cuál es la columna de "producto" (ignorando mayúsculas)
            col_prod = next((c for c in df.columns if 'producto' in str(c).lower()), None)
            if col_prod:
                df = df.dropna(subset=[col_prod])
            return df
        except Exception:
            continue
            
    st.error("No se encontró el archivo Excel en GitHub.")
    return pd.DataFrame()

df = cargar_datos()

if 'carrito' not in st.session_state:
    st.session_state.carrito = {}

st.divider()

if not df.empty:
    # Detectar las columnas de tu Excel basándonos en tu captura con guiones bajos
    col_prod = next((c for c in df.columns if 'producto' in str(c).lower()), None)
    col_precio = next((c for c in df.columns if 'unidad' in str(c).lower()), None)
    col_desc = next((c for c in df.columns if 'descrip' in str(c).lower()), None)
    col_largo = next((c for c in df.columns if 'largo' in str(c).lower()), None)
    col_promo = next((c for c in df.columns if 'promo' in str(c).lower()), None)
    col_img = next((c for c in df.columns if 'imag' in str(c).lower() or 'foto' in str(c).lower() or 'url' in str(c).lower()), None)
    
    # Layout en cuadrícula (3 columnas) para que se vea más como un catálogo
    cols = st.columns(3)
    col_idx = 0
    
    for index, row in df.iterrows():
        with cols[col_idx]:
            # Contenedor estilo tarjeta blanca
            st.markdown("<div class='product-card'>", unsafe_allow_html=True)
            
            # Imagen
            tiene_foto = False
            if col_img and pd.notna(row[col_img]):
                url = str(row[col_img]).strip()
                if url.startswith('http'):
                    st.image(url, use_container_width=True)
                    tiene_foto = True
            if not tiene_foto:
                # Imagen genérica de relleno para mantener el formato
                st.info("📷 Imagen no disponible")
            
            # Nombre del producto
            if col_prod and pd.notna(row[col_prod]):
                producto_nombre = str(row[col_prod])
            else:
                producto_nombre = f'Producto {index}'
            
            st.markdown(f"<h3>{producto_nombre}</h3>", unsafe_allow_html=True)
            
            # Unir las descripciones y extras
            detalles = []
            if col_desc and pd.notna(row[col_desc]):
                val_desc = str(row[col_desc]).strip()
                if val_desc and val_desc != 'nan':
                    detalles.append(val_desc)
                    
            if col_largo and pd.notna(row[col_largo]):
                val_largo = str(row[col_largo]).strip()
                if val_largo and val_largo != 'nan':
                    detalles.append(f"Largo: {val_largo}")
                    
            if col_promo and pd.notna(row[col_promo]):
                val_promo = str(row[col_promo]).strip()
                if val_promo and val_promo != 'nan':
                    st.markdown(f"<div style='background-color: yellow; padding: 5px; font-weight: bold; text-align: center; border: 1px solid red; margin-bottom: 5px;'>PROMO: {val_promo}</div>", unsafe_allow_html=True)
                        
            if detalles:
                st.write(" | ".join(detalles))
            
            # Limpiar y mostrar el precio
            precio = 0.0
            if col_precio and pd.notna(row[col_precio]):
                try:
                    precio_str = str(row[col_precio]).replace('$', '').replace(',', '').strip()
                    precio = float(precio_str)
                except:
                    precio = 0.0
                    
            st.markdown(f"<div class='price-tag'>$ {precio:,.2f}</div>", unsafe_allow_html=True)
            
            # Control de cantidad
            cantidad = st.number_input(
                f"Cantidad", 
                min_value=0, 
                max_value=100, 
                step=1, 
                key=f"cant_{index}",
                label_visibility="collapsed"
            )
            
            if cantidad > 0:
                st.session_state.carrito[producto_nombre] = {
                    'cantidad': cantidad,
                    'precio': precio,
                    'subtotal': cantidad * precio
                }
            elif producto_nombre in st.session_state.carrito:
                del st.session_state.carrito[producto_nombre]
                
            st.markdown("</div>", unsafe_allow_html=True)
            
        # Avanzar a la siguiente columna
        col_idx += 1
        if col_idx > 2:
            col_idx = 0

st.divider()
st.header("🛒 Resumen del Pedido")

if not st.session_state.carrito:
    st.info("Tu carrito está vacío. Sumá cantidades arriba para ver el total.")
else:
    subtotal_productos = sum(item['subtotal'] for item in st.session_state.carrito.values())
    
    st.write("### Opciones de Envío (Ingresá tu CP para ver si aplicás a Envío Gratis)")
    cp = st.text_input("Código Postal (Ej: 3352):", placeholder="3352")
    
    costo_envio = 0
    texto_envio = ""
    
    # Lógica de envío basada en el PDF y el CP local
    if subtotal_productos >= 500000:
        costo_envio = 0
        texto_envio = "¡Envío GRATIS a TODO EL PAÍS! (Superaste los $500.000)"
    elif subtotal_productos >= 150000 and cp and (cp.strip().startswith('33') or cp.strip() == '3352'):
         costo_envio = 0
         texto_envio = "¡Envío GRATIS Misiones/Local! (Superaste los $150.000)"
    elif cp and cp.strip() == "3352":
        costo_envio = 0
        texto_envio = "¡Envío GRATIS en zona local (San Pedro)!"
    elif cp:
        costo_envio = 3500
        texto_envio = f"Costo de envío estándar: ${costo_envio:,.2f}"
            
    total_final = subtotal_productos + costo_envio

    resumen_df = pd.DataFrame([
        {"Producto": prod, "Cant": data['cantidad'], "Total": f"${data['subtotal']:,.2f}"}
        for prod, data in st.session_state.carrito.items()
    ])
    st.dataframe(resumen_df, hide_index=True, use_container_width=True)
    
    st.markdown(f"<h4>Subtotal: ${subtotal_productos:,.2f}</h4>", unsafe_allow_html=True)
    if cp or subtotal_productos >= 500000:
        st.write(f"**Envío:** {texto_envio}")
    st.markdown(f"<h2 style='color: #E62429;'>Total a Pagar: ${total_final:,.2f}</h2>", unsafe_allow_html=True)
    
    numero_whatsapp = "549XXXXXXXXXX" # <-- Cambiá esto por tu número
    
    mensaje = "¡Hola Fábrica Taira! Quiero hacer el siguiente pedido:\n\n"
    for prod, data in st.session_state.carrito.items():
        mensaje += f"▪ {data['cantidad']}x {prod} (${data['subtotal']:,.2f})\n"
    
    mensaje += f"\n*Subtotal:* ${subtotal_productos:,.2f}"
    if cp:
        mensaje += f"\n*Envío (CP {cp}):* ${costo_envio:,.2f}"
    mensaje += f"\n*TOTAL FINAL:* ${total_final:,.2f}\n\nPor favor, confirmame el stock."
    
    url_wa = f"https://wa.me/{numero_whatsapp}?text={urllib.parse.quote(mensaje)}"
    
    st.markdown(f"<a href='{url_wa}' target='_blank' class='whatsapp-btn'>🟢 Enviar Pedido por WhatsApp</a>", unsafe_allow_html=True)
