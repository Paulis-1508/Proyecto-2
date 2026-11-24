import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="El costo invisible del progreso", layout="wide")

df = pd.read_csv("data/processed/datos_integrados.csv")

primer_anio = df.anio.min()
ultimo_anio = df.anio.max()

st.markdown(f"""
<div style="background:midnightblue; color:white; padding:24px 30px; border-radius:15px;">
    <p style="color:skyblue; font-size:13px; letter-spacing:2px; margin:0;">
        DATA1002 · APLICACIONES EN CIENCIA DE DATOS
    </p>
    <h1 style="color:white; font-size:38px; margin:12px 0; padding:0;">
        El costo invisible del progreso
    </h1>
    <p style="font-size:16px; margin:0 0 18px 0;">
        Explora la relación entre el crecimiento económico, las emisiones de CO₂ y el impacto del consumo internacional.
    </p>
    <span style="background:steelblue; padding:7px 14px; border-radius:20px; font-size:13px;">
        {primer_anio} a {ultimo_anio} · Banco Mundial · Global Carbon Budget · Our World in Data
    </span>
</div>
""", unsafe_allow_html=True)

st.write("")

st.subheader("Explorar países y períodos")

col1, col2, col3 = st.columns(3)

anios = sorted(df.anio.unique())

with col1:
    anio_inicio = st.selectbox("Año inicial", options=anios[:-1])

with col2:
    anios_finales = [anio for anio in anios if anio > anio_inicio]
    anio_final = st.selectbox("Año final", options=anios_finales, index=len(anios_finales)-1)

with col3:
    filtro_paises = st.multiselect("Países (vacío = todos)", options=sorted(df.pais.unique()))

df_filtrado = df[(df.anio >= anio_inicio) & (df.anio <= anio_final)].copy()

if len(filtro_paises) > 0:
    df_filtrado = df_filtrado[df_filtrado.pais.isin(filtro_paises)]
    
df_inicio = df_filtrado[df_filtrado.anio == anio_inicio]

df_fin = df_filtrado[df_filtrado.anio == anio_final]

resumen = df_inicio.merge(df_fin, on="codigo", how="inner", suffixes=("_inicio", "_fin"), validate="1:1")

resumen["pais"] = resumen.pais_inicio

resumen = resumen[(resumen.pib_inicio > 0) & (resumen.co2_territorial_inicio > 0) &
                  (resumen.co2_consumo_inicio > 0)].copy()

if resumen.empty:
    st.warning("No hay países comparables para esta selección.")
    st.stop()
    
resumen["var_pib"] = (resumen.pib_fin / resumen.pib_inicio - 1) * 100

resumen["var_territorial"] = (resumen.co2_territorial_fin / resumen.co2_territorial_inicio - 1) * 100

resumen["var_consumo"] = (resumen.co2_consumo_fin / resumen.co2_consumo_inicio - 1) * 100

resumen["var_territorial_pc"] = (resumen.territorial_per_capita_fin / resumen.territorial_per_capita_inicio - 1) * 100

resumen["var_consumo_pc"] = (resumen.consumo_per_capita_fin / resumen.consumo_per_capita_inicio - 1) * 100

resumen["var_intensidad_territorial"] = (resumen.intensidad_territorial_fin / resumen.intensidad_territorial_inicio - 1) * 100

resumen["var_intensidad_consumo"] = (resumen.intensidad_consumo_fin / resumen.intensidad_consumo_inicio - 1) * 100

resumen["brecha_pp"] = resumen.var_consumo - resumen.var_territorial

def clasificacion(pib, emisiones):
    if pib <= 0:
        return "Sin crecimiento"
    if emisiones < 0:
        return "Absoluto"
    if emisiones < pib:
        return "Relativo"
    return "Sin desacoplamiento"

resumen["Territorial"] = resumen.apply(lambda f: clasificacion(f.var_pib, f.var_territorial), axis=1)

resumen["Consumo"] = resumen.apply(lambda f: clasificacion(f.var_pib, f.var_consumo), axis=1)

resumen["cambia"] = resumen.Territorial != resumen.Consumo

total_paises = resumen.shape[0]

paises_crecimiento = resumen[resumen.var_pib > 0].shape[0]

absoluto_territorial = resumen[resumen.Territorial == "Absoluto"].shape[0]

absoluto_consumo = resumen[resumen.Consumo == "Absoluto"].shape[0]

paises_cambian = resumen[resumen.cambia == True].shape[0]

porcentaje_cambio = paises_cambian / total_paises * 100

st.caption(f"Período analizado: {anio_inicio} - {anio_final}. Países comparables: {total_paises}")

a, b, c, d, e = st.columns(5)

a.metric("Países analizados", total_paises, border=True)
b.metric("PIB en crecimiento", paises_crecimiento, border=True)
c.metric("Absoluto territorial", absoluto_territorial, border=True)
d.metric("Absoluto consumo", absoluto_consumo, border=True)
e.metric("Cambian clasificación", f"{porcentaje_cambio:.1f}%", border=True)

st.divider()

colores = {"Absoluto":"seagreen", "Relativo":"steelblue",
           "Sin desacoplamiento":"darkorange", "Sin crecimiento":"gray"}

orden = ["Absoluto", "Relativo", "Sin desacoplamiento", "Sin crecimiento"]

st.subheader("¿Cuánto cambia el diagnóstico ambiental?")

izquierda, derecha = st.columns(2)

tabla_territorial = resumen.groupby("Territorial").size().reset_index(name="Paises")
tabla_territorial = tabla_territorial.rename(columns={"Territorial":"Clasificacion"})
tabla_territorial["Medicion"] = "Territorial"

tabla_consumo = resumen.groupby("Consumo").size().reset_index(name="Paises")
tabla_consumo = tabla_consumo.rename(columns={"Consumo":"Clasificacion"})
tabla_consumo["Medicion"] = "Consumo"

tabla = pd.concat([tabla_territorial, tabla_consumo], ignore_index=True)

with izquierda:
    with st.container(border=True):
        st.markdown("**Desacoplamiento según la medición de CO₂**")
        st.caption("Número de países en cada clasificación.")

        fig = px.bar(tabla, x="Medicion", y="Paises", color="Clasificacion",
                     barmode="group", text="Paises", color_discrete_map=colores,
                     category_orders={"Clasificacion":orden}, template="plotly_white")

        st.plotly_chart(fig, width="stretch", key="grafica1")
        
with derecha:
    with st.container(border=True):
        st.markdown("**Cambios entre clasificaciones**")
        st.caption("Comparación de la clasificación territorial y de consumo.")

        matriz = pd.crosstab(resumen.Territorial, resumen.Consumo)
        matriz = matriz.reindex(index=orden, columns=orden, fill_value=0)

        fig = px.imshow(matriz, text_auto=True, color_continuous_scale="Blues",
                        labels={"x":"Consumo", "y":"Territorial", "color":"Países"}, aspect="auto")

        st.plotly_chart(fig, width="stretch", key="grafica2")
        
st.subheader("Crecimiento económico frente a emisiones")

izquierda, derecha = st.columns(2)

limite_min = min(0, resumen.var_pib.min(), resumen.var_territorial.min(), resumen.var_consumo.min())
limite_max = max(0, resumen.var_pib.max(), resumen.var_territorial.max(), resumen.var_consumo.max())

with izquierda:
    with st.container(border=True):
        st.markdown("**Crecimiento del PIB y CO₂ territorial**")
        st.caption("Cada punto representa un país.")

        fig = px.scatter(resumen, x="var_pib", y="var_territorial", color="Territorial",
                         hover_name="pais", color_discrete_map=colores, template="plotly_white",
                         labels={"var_pib":"Variación PIB (%)", "var_territorial":"Variación CO₂ (%)"})

        fig.add_hline(y=0, line_dash="dash")
        fig.add_vline(x=0, line_dash="dash")
        fig.add_shape(type="line", x0=0, y0=0, x1=limite_max, y1=limite_max, line=dict(color="gray", dash="dot"))
        fig.update_xaxes(range=[limite_min, limite_max])
        fig.update_yaxes(range=[limite_min, limite_max])

        st.plotly_chart(fig, width="stretch", key="grafica3")
        
with derecha:
    with st.container(border=True):
        st.markdown("**Crecimiento del PIB y CO₂ de consumo**")
        st.caption("Incluye las emisiones asociadas al comercio internacional.")

        fig = px.scatter(resumen, x="var_pib", y="var_consumo", color="Consumo",
                         hover_name="pais", color_discrete_map=colores, template="plotly_white",
                         labels={"var_pib":"Variación PIB (%)", "var_consumo":"Variación CO₂ (%)"})

        fig.add_hline(y=0, line_dash="dash")
        fig.add_vline(x=0, line_dash="dash")
        fig.add_shape(type="line", x0=0, y0=0, x1=limite_max, y1=limite_max, line=dict(color="gray", dash="dot"))
        fig.update_xaxes(range=[limite_min, limite_max])
        fig.update_yaxes(range=[limite_min, limite_max])

        st.plotly_chart(fig, width="stretch", key="grafica4")
        
st.subheader("¿Dónde se encuentra el costo invisible del progreso?")

izquierda, derecha = st.columns(2)

resumen["brecha_absoluta"] = resumen.brecha_pp.abs()

tabla_brechas = resumen.sort_values("brecha_absoluta", ascending=False).head(15).copy()

tabla_brechas["Direccion"] = np.where(tabla_brechas.brecha_pp >= 0,
                                      "Mayor variación de consumo", "Mayor variación territorial")

with izquierda:
    with st.container(border=True):
        st.markdown("**Países con mayores diferencias entre emisiones**")
        st.caption("15 mayores brechas en valor absoluto, expresadas en puntos porcentuales.")

        fig = px.bar(tabla_brechas.sort_values("brecha_pp"), x="brecha_pp", y="pais",
                     orientation="h", color="Direccion", template="plotly_white",
                     color_discrete_map={"Mayor variación de consumo":"darkorange", "Mayor variación territorial":"steelblue"},
                     labels={"brecha_pp":"Brecha (puntos porcentuales)", "pais":"País"})

        st.plotly_chart(fig, width="stretch", key="grafica5")
        
with derecha:
    with st.container(border=True):
        st.markdown("**Emisiones por habitante e intensidad económica**")
        st.caption("Compara cómo cambian las emisiones al considerar población o PIB.")

        indicador = st.selectbox("Indicador", ["Emisiones per cápita", "Intensidad de emisiones"])

        if indicador == "Emisiones per cápita":
            tabla = tabla_brechas[["pais", "var_territorial_pc", "var_consumo_pc"]].copy()
            tabla = tabla.rename(columns={"var_territorial_pc":"Territorial", "var_consumo_pc":"Consumo"})

        else:
            tabla = tabla_brechas[["pais", "var_intensidad_territorial", "var_intensidad_consumo"]].copy()
            tabla = tabla.rename(columns={"var_intensidad_territorial":"Territorial", "var_intensidad_consumo":"Consumo"})

        fig = px.bar(tabla, x="pais", y=["Territorial", "Consumo"], barmode="group",
                     color_discrete_sequence=["steelblue", "darkorange"], template="plotly_white",
                     labels={"pais":"País", "value":"Variación (%)", "variable":"Medición"})

        st.plotly_chart(fig, width="stretch", key="grafica6")
        
st.subheader("Evolución económica y ambiental por país")

pais_elegido = st.selectbox("Seleccionar país", options=sorted(resumen.pais.unique()))

serie = df_filtrado[df_filtrado.pais == pais_elegido].sort_values("anio").copy()

serie = serie.set_index("anio").reindex(range(anio_inicio, anio_final+1)).reset_index()

serie["PIB real"] = serie.pib / serie.pib.iloc[0] * 100

serie["CO2 territorial"] = serie.co2_territorial / serie.co2_territorial.iloc[0] * 100

serie["CO2 consumo"] = serie.co2_consumo / serie.co2_consumo.iloc[0] * 100

with st.container(border=True):
    st.markdown("**Trayectoria del crecimiento económico y las emisiones**")
    st.caption(f"Índice base 100 en {anio_inicio}.")

    fig = px.line(serie, x="anio", y=["PIB real", "CO2 territorial", "CO2 consumo"],
                  markers=True, color_discrete_sequence=["navy", "steelblue", "darkorange"],
                  template="plotly_white", labels={"anio":"Año", "value":"Índice base 100", "variable":"Indicador"})

    fig.add_hline(y=100, line_dash="dash")
    fig.update_traces(connectgaps=False)

    st.plotly_chart(fig, width="stretch", key="grafica7")
    
st.subheader("Principales resultados de la selección")

pierden_absoluto = resumen[(resumen.Territorial == "Absoluto") &
                           (resumen.Consumo != "Absoluto")].shape[0]

ganan_absoluto = resumen[(resumen.Territorial != "Absoluto") &
                          (resumen.Consumo == "Absoluto")].shape[0]

mayor_brecha = resumen.sort_values("brecha_absoluta", ascending=False).iloc[0]

st.write(f"De los {total_paises} países analizados, {paises_cambian} cambian de clasificación, lo que representa el {porcentaje_cambio:.1f}%.")

st.write(f"{pierden_absoluto} países dejan de presentar desacoplamiento absoluto al considerar las emisiones de consumo.")

st.write(f"{ganan_absoluto} países pasan a presentar desacoplamiento absoluto al considerar las emisiones de consumo.")

st.write(f"El país con mayor diferencia absoluta entre las trayectorias de emisiones es {mayor_brecha.pais}, con una brecha de {mayor_brecha.brecha_pp:.1f} puntos porcentuales.")

st.caption("Los resultados son descriptivos y no demuestran relaciones de causalidad.")

st.subheader("Resultados por país")

tabla_resultados = resumen[["pais", "var_pib", "var_territorial", "var_consumo",
                            "Territorial", "Consumo", "brecha_pp"]].copy()

tabla_resultados = tabla_resultados.rename(columns={"pais":"País", "var_pib":"Variación PIB (%)",
                            "var_territorial":"CO2 territorial (%)", "var_consumo":"CO2 consumo (%)",
                            "brecha_pp":"Brecha (pp)"})

st.dataframe(tabla_resultados.round(2), hide_index=True, width="stretch")

with st.expander("Notas metodológicas y datos de respaldo"):

    st.markdown("""
    - **Granularidad:** cada fila de la base representa un país en un año.
    - **PIB:** dólares internacionales constantes de 2021, ajustados por poder adquisitivo.
    - **Emisiones:** toneladas de CO₂.
    - **Per cápita:** toneladas de CO₂ por habitante.
    - **Intensidad:** toneladas de CO₂ por cada 1.000 dólares internacionales de PIB.
    - **Variaciones:** cambios porcentuales entre el año inicial y el año final.
    - **Brecha:** diferencia entre la variación porcentual del CO₂ de consumo y territorial.
    - **Cobertura:** países con información válida en ambos extremos del período.
    - **Limitaciones:** los resultados no establecen causalidad ni representan todos los impactos ambientales.
    - **Fuentes:** Banco Mundial, Global Carbon Budget y Our World in Data.
    """)

    st.download_button("Descargar resultados de la selección (CSV)",
                       data=tabla_resultados.to_csv(index=False),
                       file_name="resultados.csv", mime="text/csv")
    
    
    