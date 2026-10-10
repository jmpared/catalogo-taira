import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Catálogo Fábrica Taira", layout="centered", initial_sidebar_state="collapsed")

st.title("Fábrica Taira - Pedidos Online")
st.write("Seleccioná los productos que necesitás y armá tu pedido.")

@st.cache_data
def cargar_datos():
    # Busca ambos nombres posibles para evitar errores de archivo no encontrado
    archivos_posibles = ["Productos taira.xlsx", "Base_Catalogo_Pedidos.xlsx"]
    for archivo in archivos_posibles:
        try:
            df = pd.read_excel(archivo)
            return df
        except FileNotFoundError:
            continue
    st.error("No se encontró el archivo Excel en GitHub.")
    return pd.DataFrame()

df = cargar_datos()

if 'carrito' not in st.session_state:
    st.session_state.carrito = {}

st.divider()

if not df.empty:
    for index, row in df.iterrows():
        col_img, col_info = st.columns([1, 2])
        
        with col_img:
            # Revisa si la columna Imagen_URL existe antes de intentar mostrarla
            if 'Imagen_URL' in df.columns and pd.notna(row.get('Imagen_URL')):
                st.image(row['Imagen_URL'], use_container_width=True)
            else:
                st.write("📷 Sin foto")
                
        with col_info:
            # Mapeamos los nombres EXACTOS de tus columnas según la captura
            producto_nombre = row.get('Producto', f'Producto {index}')
            st.subheader(producto_nombre)
            
            # Unimos las descripciones extra
            desc = str(row.get('descripcion', ''))
            largo = str(row.get('Largo', ''))
            promo = str(row.get('Precio PROMO 10+2 / 5+1', ''))
            
            detalles = []
            if desc and desc != 'nan': detalles.append(desc)
            if largo and largo != 'nan': detalles.append(f"Largo: {largo}")
            if promo and promo != 'nan': detalles.append(f"Promo: {promo}")
            
            if detalles:
                st.caption(" | ".join(detalles))
            
            # Precio unitario (respetando como lo escribiste en tu Excel)
            precio = row.get('precio por unidada', 0)
            try:
                precio = float(precio)
            except:
                precio = 0.0
                
            st.write(f"**Precio unitario:** ${precio:,.2f}")
            
            cantidad = st.number_input(
                f"Cantidad", 
                min_value=0, 
                max_value=100, 
                step=1, 
                key=f"cant_{index}"
            )
            
            if cantidad > 0:
                st.session_state.carrito[producto_nombre] = {
                    'cantidad': cantidad,
                    'precio': precio,
                    'subtotal': cantidad * precio
                }
            elif producto_nombre in st.session_state.carrito:
                del st.session_state.carrito[producto_nombre]
        
        st.divider()

st.header("🛒 Resumen del Pedido")

if not st.session_state.carrito:
    st.info("Tu carrito está vacío. Sumá cantidades arriba para ver el total.")
else:
    subtotal_productos = sum(item['subtotal'] for item in st.session_state.carrito.values())
    
    cp = st.text_input("Ingresá tu Código Postal:", placeholder="Ej: 3352")
    costo_envio = 0
    texto_envio = ""
    
    if cp:
        if cp.strip() == "3352":
            costo_envio = 0
            texto_envio = "¡Envío GRATIS en tu zona!"
        else:
            costo_envio = 3500
            texto_envio = f"Costo de envío a domicilio: ${costo_envio:,.2f}"
            
    total_final = subtotal_productos + costo_envio

    resumen_df = pd.DataFrame([
        {"Producto": prod, "Cant": data['cantidad'], "Total": f"${data['subtotal']:,.2f}"}
        for prod, data in st.session_state.carrito.items()
    ])
    st.dataframe(resumen_df, hide_index=True, use_container_width=True)
    
    st.write(f"**Subtotal:** ${subtotal_productos:,.2f}")
    if cp:
        st.write(f"**Envío:** {texto_envio}")
    st.subheader(f"Total a Pagar: ${total_final:,.2f}")
    
    numero_whatsapp = "549XXXXXXXXXX" # <-- Cambiá esto por el número real
    
    mensaje = "¡Hola Fábrica Taira! Quiero hacer el siguiente pedido:\n\n"
    for prod, data in st.session_state.carrito.items():
        mensaje += f"▪ {data['cantidad']}x {prod} (${data['subtotal']:,.2f})\n"
    
    mensaje += f"\n*Subtotal:* ${subtotal_productos:,.2f}"
    if cp:
        mensaje += f"\n*Envío (CP {cp}):* ${costo_envio:,.2f}"
    mensaje += f"\n*TOTAL FINAL:* ${total_final:,.2f}\n\nPor favor, confirmame el stock."
    
    url_wa = f"https://wa.me/{numero_whatsapp}?text={urllib.parse.quote(mensaje)}"
    
    st.markdown(
        f'<a href="{url_wa}" target="_blank" style="text-decoration:none;">'
        f'<div style="background-color:#25D366; color:white; padding:15px; text-align:center; '
        f'border-radius:8px; font-size:18px; font-weight:bold;">'
        f'🟢 Enviar Pedido por WhatsApp</div></a>', 
        unsafe_allow_html=True
    )
