import streamlit as st

st.set_page_config(page_title="Control Diabetes PRO", page_icon="💙", layout="wide")

# ==========================================
# 1. BASE DE DATOS (VOLCADO DE LOS PDFs)
# ==========================================

# COMIDA CASERA: Valor = Gramos que equivalen a 1 Ración (10g HC)
# Fuente: PDF ALIMENTOS
bd_casera = {
    "🍞 Harinas y Cereales": {
        "Arroz blanco/integral (Crudo)": 15,
        "Arroz blanco/integral (Hervido)": 40,
        "Pasta (Cruda)": 15,
        "Pasta (Hervida)": 45,
        "Pan de barra (Blanco/Integral)": 20,
        "Pan de molde": 20,
        "Pan tostado / Biscotes": 15,
        "Legumbres (Hervidas: Lentejas, Garbanzos, Judías)": 50,
        "Guisantes (Congelados/Lata)": 100,
        "Patata (Hervida/Asada)": 65,
        "Patata (Frita casera)": 30,
        "Puré de patata (Copos)": 15,
        "Boniato": 50,
        "Harina (Trigo, Maíz, Avena)": 15,
        "Masa de Pizza": 20,
    },
    "🍎 Frutas": {
        "Manzana / Pera": 100,
        "Plátano": 50,
        "Naranja / Mandarina": 100,
        "Fresas / Fresones": 200,
        "Kiwi": 100,
        "Melocotón / Nectarina": 100,
        "Melón / Sandía": 200,
        "Uvas": 50,
        "Piña (Natural)": 100,
        "Cerezas": 100,
        "Higos": 50,
        "Ciruelas": 100,
    },
    "🥛 Lácteos y Dulces": {
        "Leche (Entera/Semi/Desnatada) - 1 Vaso": 200,
        "Yogur natural (sin azúcar)": 250, # Normalmente casi 2 yogures es 1 ración
        "Yogur de frutas / Sabores": 125,
        "Helado de crema": 50,
        "Azúcar (Blanco/Moreno)": 10,
        "Mermelada": 20,
        "Miel": 12,
        "Chocolate con leche": 20,
        "Galletas tipo María": 15,
        "Magdalena": 20,
        "Croissant": 20,
    },
    "🥦 Verduras (Ojo: Muchas son libres)": {
        "Tomate": 300,
        "Cebolla": 150,
        "Zanahoria (Cruda)": 150,
        "Zanahoria (Hervida)": 100,
        "Remolacha": 150,
        "Calabaza": 200,
        "Judías verdes / Brócoli / Lechuga": 999, # Prácticamente libre
    }
}

# RESTAURANTE: Valor = Raciones de HC (1 Ración = 10g HC)
# Fuente: PDF MENU
bd_restaurante = {
    "🥣 Primeros / Platos de Cuchara": {
        "Paella / Arroz (Plato normal)": 6.0,
        "Fideuá (Plato normal)": 6.0,
        "Lentejas estofadas (Plato)": 5.0,
        "Cocido (Sopa + Garbanzos)": 6.0,
        "Macarrones / Pasta con salsa": 6.0,
        "Ensaladilla Rusa (Ración)": 3.0,
        "Gazpacho (Vaso)": 1.5,
        "Crema de verduras (Sin patata)": 1.5,
        "Crema de verduras (Con patata)": 3.0,
        "Canelones (3 unidades)": 4.5,
    },
    "🍗 Segundos / Carnes y Pescados": {
        "Filete plancha (Pollo/Ternera)": 0.0,
        "Pescado plancha/horno": 0.0,
        "Carne rebozada / San Jacobo": 2.0,
        "Pescado rebozado / Romana": 2.0,
        "Albóndigas (con salsa)": 1.5,
        "Hamburguesa (Solo carne + queso)": 0.5,
        "Hamburguesa Completa (Pan + Patatas)": 7.0, # Pan(4) + Patatas(3)
        "Pizza (Media)": 6.0,
        "Pizza (Entera)": 12.0,
    },
    "🍟 Guarniciones y Pan": {
        "Patatas fritas (Guarnición)": 3.0,
        "Patata asada (Unidad media)": 4.0,
        "Ensalada (Lechuga/Tomate)": 0.0,
        "Pan (Rebanada pequeña)": 1.0,
        "Pan (Bollito restaurante)": 3.0,
        "Picos / Colines (Bolsita)": 1.5,
    },
    "🍰 Postres y Bebidas": {
        "Flan casero": 3.0,
        "Arroz con leche": 4.0,
        "Tarta de queso / Chocolate": 5.0,
        "Fruta del tiempo (Pieza)": 2.0,
        "Yogur": 1.0,
        "Helado (Bola)": 2.0,
        "Cerveza (Caña)": 1.0,
        "Cerveza (Jarra)": 2.0,
        "Refresco (No Zero)": 3.5,
    }
}

# ==========================================
# 2. INTERFAZ DE USUARIO
# ==========================================

st.title("🍽️ Calculadora de Insulina")
st.markdown("**Basada en tus tablas médicas (ALIMENTOS y MENÚ)**")

# --- BARRA LATERAL (DATOS FIJOS) ---
with st.sidebar:
    st.header("⚙️ Configuración Personal")
    # Ratio: Insulina por cada ración (10g)
    ratio = st.number_input("Ratio (Unidades por Ración):", value=1.0, step=0.1, format="%.1f")
    
    st.markdown("---")
    st.header("🩸 Corrección")
    # Datos de corrección
    glucosa_actual = st.number_input("Glucosa Actual (mg/dL):", value=110, step=10)
    objetivo = st.number_input("Objetivo (mg/dL):", value=100)
    fsi = st.number_input("Factor Sensibilidad (FSI):", value=35)
    
    st.markdown("---")
    st.info(f"**Resumen:**\n\n1 ración = 10g HC\n1 Unidad baja {fsi} mg/dL")

# --- SELECTOR DE MODO ---
modo = st.radio("¿Qué vas a comer?", ["🏠 Comida Casera (Peso alimentos)", "🍴 Restaurante (Elijo platos)"], horizontal=True)

total_raciones = 0.0
lista_resumen = []

st.divider()

# ==========================================
# MODO 1: COMIDA CASERA (Pesaje exacto)
# ==========================================
if modo == "🏠 Comida Casera (Peso alimentos)":
    st.subheader("Añade los alimentos de tu plato")
    st.caption("Selecciona el alimento y pon los gramos que te vas a comer.")

    # Generamos 6 filas para añadir ingredientes
    for i in range(1, 7):
        c1, c2, c3 = st.columns([3, 4, 2])
        
        with c1:
            # Seleccionar Categoría
            cat = st.selectbox(f"Categoría {i}", ["-"] + list(bd_casera.keys()), key=f"cat_home_{i}")
        
        with c2:
            # Seleccionar Alimento (según categoría)
            opciones_alimentos = list(bd_casera[cat].keys()) if cat != "-" else ["-"]
            alimento = st.selectbox(f"Alimento {i}", opciones_alimentos, key=f"ali_home_{i}")
        
        with c3:
            # Input Gramos
            gramos = st.number_input(f"Gramos", min_value=0, step=5, key=f"gr_home_{i}", label_visibility="collapsed")

        # Cálculo en tiempo real de esa fila
        if cat != "-" and alimento != "-" and gramos > 0:
            valor_referencia = bd_casera[cat][alimento]
            
            # Si el valor es 999 (verduras libres), no cuentan HC
            if valor_referencia == 999:
                racion_item = 0
            else:
                # Regla de tres: (Gramos Comidos / Gramos 1 Ración)
                racion_item = gramos / valor_referencia
            
            total_raciones += racion_item
            lista_resumen.append(f"{gramos}g {alimento} ({racion_item:.1f} R)")

# ==========================================
# MODO 2: RESTAURANTE (Menú estándar)
# ==========================================
else:
    st.subheader("Selecciona lo que has pedido")
    st.caption("El cálculo se basa en las raciones estándar del PDF MENÚ.")

    # Generamos 5 filas para pedir (Primero, Segundo, Postre, Bebida, Pan)
    for i in range(1, 6):
        c1, c2 = st.columns([3, 5])
        
        with c1:
            cat_rest = st.selectbox(f"Tipo de plato {i}", ["-"] + list(bd_restaurante.keys()), key=f"cat_rest_{i}")
        
        with c2:
            opts_rest = list(bd_restaurante[cat_rest].keys()) if cat_rest != "-" else ["-"]
            plato = st.selectbox(f"Plato {i}", opts_rest, key=f"plato_rest_{i}")

        if cat_rest != "-" and plato != "-":
            raciones_plato = bd_restaurante[cat_rest][plato]
            total_raciones += raciones_plato
            lista_resumen.append(f"{plato} ({raciones_plato:.1f} R)")


# ==========================================
# 3. CÁLCULOS FINALES
# ==========================================
st.divider()

# Cálculo Insulina Comida
insulina_comida = total_raciones * ratio

# Cálculo Corrección (Solo si está alta)
insulina_correccion = 0.0
if glucosa_actual > objetivo:
    insulina_correccion = (glucosa_actual - objetivo) / fsi

insulina_total = insulina_comida + insulina_correccion

# --- VISUALIZACIÓN DE RESULTADOS ---
col_result_1, col_result_2 = st.columns([1, 1])

with col_result_1:
    st.markdown("### 📋 Resumen Comida")
    if lista_resumen:
        for item in lista_resumen:
            st.text(f"• {item}")
        st.markdown(f"**Total Hidratos:** {total_raciones * 10:.0f}g")
        st.markdown(f"**Total Raciones:** {total_raciones:.1f}")
    else:
        st.info("Añade alimentos para ver el cálculo.")

with col_result_2:
    st.markdown("### 💉 Dosis Recomendada")
    
    # Caja de resultado con estilo
    html_result = f"""
    <div style="background-color: #d1e7dd; padding: 20px; border-radius: 10px; border: 2px solid #badbcc; text-align: center;">
        <h1 style="color: #0f5132; margin:0;">{insulina_total:.1f} Unidades</h1>
        <hr style="border-color: #0f5132;">
        <p style="color: #0f5132; margin-bottom:0;">
            <b>Comida:</b> {insulina_comida:.1f} u<br>
            <b>Corrección:</b> {insulina_correccion:.1f} u
        </p>
    </div>
    """
    st.markdown(html_result, unsafe_allow_html=True)

    if glucosa_actual < 70:
        st.warning("⚠️ **HIPOGLUCEMIA:** No te pongas insulina hasta corregir el azúcar.")