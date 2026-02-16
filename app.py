import streamlit as st

st.set_page_config(page_title="Control Diabetes", page_icon="💙", layout="wide")

# ==========================================
# 1. BASE DE DATOS: COMIDA CASERA
# Clave: Gramos que equivalen a 1 Ración (10g HC)
# Fuente: PDF ALIMENTOS
# ==========================================
bd_casera = {
    "🍞 Pan y Harinas": {
        "Pan blanco (barra)": 20,
        "Pan integral": 20,
        "Pan de molde": 20,
        "Pan tostado / Biscotes": 15,
        "Pan de hamburguesa (Bollo)": 18,
        "Harina (Trigo/Maíz)": 15,
        "Masa de pizza / Hojaldre": 30,
        "Pan rallado": 15,
        "Churros": 25,
    },
    "🍝 Pasta, Arroz y Legumbres": {
        "Arroz blanco (Hervido)": 38,
        "Arroz blanco (Crudo)": 13,
        "Arroz integral (Hervido)": 40,
        "Pasta (Hervida)": 45,
        "Pasta (Cruda)": 14,
        "Garbanzos (Hervidos)": 55,
        "Lentejas (Hervidas)": 50,
        "Judías blancas (Hervidas)": 55,
        "Guisantes (Lata/Congelado)": 100,
        "Habas": 60,
        "Quinoa (Hervida)": 48,
        "Cuscús (Cocido)": 45,
    },
    "🥔 Patatas y Tubérculos": {
        "Patata hervida / vapor": 65,
        "Patata asada / horno": 35,
        "Patata frita casera": 30,
        "Patatas Chips (Bolsa)": 20,
        "Puré de patata (Copos)": 15,
        "Puré de patata (Casero)": 80,
        "Boniato": 50,
        "Yuca": 33,
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
        "Piña": 100,
        "Cerezas": 100,
        "Higos": 50,
        "Ciruelas": 100,
        "Mango": 100,
    },
    "🥛 Lácteos y Otros": {
        "Leche (Vaso 200ml)": 200,
        "Bebida Soja/Avena": 200,
        "Yogur Natural (Sin azúcar)": 200,
        "Yogur Sabores/Fruta": 125,
        "Azúcar": 10,
        "Miel / Mermelada": 15,
        "Chocolate leche": 17,
        "Chocolate negro (>70%)": 25,
        "Galleta María": 15,
        "Croissant / Magdalena": 20,
        "Helado crema": 50,
    }
}

# ==========================================
# 2. BASE DE DATOS: RESTAURANTE
# Clave: Número de Raciones (1 Ración = 10g HC)
# Fuente: PDF MENU
# ==========================================
bd_restaurante = {
    "🥪 Bocadillos y Comida Rápida": {
        "Bocadillo (Media barra - 100g)": 5.0,
        "Bocadillo (Barra entera - 200g)": 10.0,
        "Sándwich mixto (2 rebanadas)": 2.0,
        "Sándwich vegetal (3 rebanadas)": 3.0,
        "Hamburguesa (Simple con pan)": 3.0,
        "Hamburguesa Completa (+Patatas)": 7.5,
        "Kebab (Döner / Pan de pita)": 6.0,
        "Durum (Rollo)": 8.0,
        "Pizza (Media)": 6.0,
        "Pizza (Entera)": 12.0,
        "Nuggets (6 unidades)": 1.5,
        "Sushi (6 piezas pequeñas)": 3.0,
    },
    "🍻 Tapas y Raciones": {
        "Patatas Bravas (Tapa)": 4.0,
        "Croquetas (Unidad)": 0.5,
        "Croquetas (Ración 6 uds)": 3.0,
        "Calamares a la romana (Ración)": 2.5,
        "Sepia a la plancha": 0.0,
        "Tortilla patata (Pincho)": 2.5,
        "Ensaladilla Rusa (Tapa)": 1.5,
        "Ensaladilla Rusa (Ración)": 3.0,
        "Gambas gabardina (Unidad)": 0.5,
        "Mejillones (Vapor/Vinagreta)": 0.0,
        "Pan con tomate (2 rebanadas)": 2.0,
    },
    "🥣 Primeros / Cuchara": {
        "Paella / Arroz (Plato normal)": 6.0,
        "Fideuá": 6.0,
        "Lentejas estofadas": 5.0,
        "Cocido (Sopa+Garbanzos)": 6.0,
        "Macarrones / Pasta salsa": 6.0,
        "Canelones (3 unidades)": 4.5,
        "Lasaña de carne": 5.0,
        "Gazpacho (Vaso)": 1.5,
        "Salmorejo (Plato)": 3.0,
        "Crema de verduras": 2.0,
        "Guisantes con jamón": 4.0,
        "Verdura con patata": 3.0,
    },
    "🍗 Segundos / Principal": {
        "Filete (Pollo/Ternera)": 0.0,
        "Pescado plancha/horno": 0.0,
        "Carne guisada con patata": 3.0,
        "Pescado rebozado": 2.0,
        "Escalope / Milanesa": 2.5,
        "Albóndigas": 1.5,
        "Huevos fritos con patatas": 4.0,
    },
    "🍟 Guarniciones y Pan": {
        "Patatas fritas": 3.0,
        "Patata asada": 4.0,
        "Ensalada": 0.0,
        "Pan (Rebanada)": 1.5,
        "Pan (Bollito)": 3.0,
        "Picos / Colines (Bolsa)": 1.5,
    },
    "🍰 Postres y Bebidas": {
        "Flan": 3.0,
        "Natillas / Crema catalana": 3.5,
        "Arroz con leche": 4.5,
        "Tarta queso / Chocolate": 5.0,
        "Fruta (Pieza)": 2.0,
        "Macedonia": 2.0,
        "Yogur": 1.5,
        "Helado (2 bolas)": 4.0,
        "Cerveza (Caña)": 1.0,
        "Cerveza (Tercio)": 1.5,
        "Clara (Con limón)": 2.5,
        "Refresco (No Zero)": 3.5,
        "Vino / Cava (Copa)": 0.0,
    }
}

# ==========================================
# CÓDIGO DE LA APLICACIÓN
# ==========================================

st.title("💙 Control Diabetes")
st.markdown("Calculadora de dosis basada en tus tablas médicas.")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Tus Datos")
    # Ratio: Insulina por cada ración (10g)
    ratio = st.number_input("Ratio (Unidades por Ración):", value=1.0, step=0.1, format="%.1f")
    st.markdown("---")
    # Datos de corrección
    glucosa_actual = st.number_input("Glucosa Actual (mg/dL):", value=100, step=10)
    objetivo = st.number_input("Objetivo (mg/dL):", value=100)
    fsi = st.number_input("Factor Sensibilidad (FSI):", value=35)
    st.info(f"1 Ración = 10g HC\n1 Unidad baja {fsi} mg/dL")

# --- MODO ---
modo = st.radio("Elige una opción:", ["🏠 Comida Casera (Peso exacto)", "🍴 Restaurante (Por platos)"], horizontal=True)

total_raciones = 0.0
lista_resumen = []

st.divider()

# ==========================================
# MODO CASERO
# ==========================================
if modo == "🏠 Comida Casera (Peso exacto)":
    st.subheader("Añade tus ingredientes (hasta 8)")
    for i in range(1, 9):
        c1, c2, c3 = st.columns([3, 4, 2])
        with c1:
            cat = st.selectbox(f"Categoría {i}", ["-"] + list(bd_casera.keys()), key=f"c{i}")
        with c2:
            opts = list(bd_casera[cat].keys()) if cat != "-" else ["-"]
            ali = st.selectbox(f"Alimento {i}", opts, key=f"a{i}")
        with c3:
            gr = st.number_input(f"Gramos", min_value=0, step=5, key=f"g{i}", label_visibility="collapsed")
            
        if cat != "-" and ali != "-" and gr > 0:
            val = bd_casera[cat][ali]
            rac = gr / val
            total_raciones += rac
            lista_resumen.append(f"{gr}g {ali} ({rac:.1f} R)")

# ==========================================
# MODO RESTAURANTE
# ==========================================
else:
    st.subheader("Selecciona lo que has pedido")
    st.caption("Valores medios estándar para comer fuera.")
    for i in range(1, 7):
        c1, c2 = st.columns([3, 5])
        with c1:
            catr = st.selectbox(f"Tipo {i}", ["-"] + list(bd_restaurante.keys()), key=f"cr{i}")
        with c2:
            optsr = list(bd_restaurante[catr].keys()) if catr != "-" else ["-"]
            plato = st.selectbox(f"Plato {i}", optsr, key=f"pr{i}")
            
        if catr != "-" and plato != "-":
            racr = bd_restaurante[catr][plato]
            total_raciones += racr
            lista_resumen.append(f"{plato} ({racr:.1f} R)")

# ==========================================
# CÁLCULOS FINALES
# ==========================================
st.divider()

insulina_comida = total_raciones * ratio

insulina_correccion = 0.0
if glucosa_actual > objetivo:
    insulina_correccion = (glucosa_actual - objetivo) / fsi

total_final = insulina_comida + insulina_correccion

c_res1, c_res2 = st.columns([1, 1])

with c_res1:
    st.markdown("### 📋 Tu Menú")
    if lista_resumen:
        for it in lista_resumen:
            st.write(f"• {it}")
        st.markdown(f"**Total:** {total_raciones:.1f} Raciones ({total_raciones*10:.0f}g HC)")
    else:
        st.info("Selecciona alimentos para calcular.")

with c_res2:
    st.markdown("### 💉 Dosis a Poner")
    st.markdown(f"""
    <div style="background-color:#d4edda;padding:20px;border-radius:15px;text-align:center;border:2px solid #c3e6cb;box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h1 style="color:#155724;margin:0;font-size:3em;">{total_final:.1f} u</h1>
        <hr style="border-top: 1px solid #155724;">
        <p style="color:#155724;font-size:0.9em;">
            <b>Comida:</b> {insulina_comida:.1f} u<br>
            <b>Corrección:</b> {insulina_correccion:.1f} u
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if glucosa_actual < 70:
        st.error("⚠️ **HIPOGLUCEMIA DETECTADA**: Toma 15g de azúcar rápido y espera 15 min antes de comer.")