# El costo invisible del progreso

Proyecto 2 · DATA-1002 Aplicaciones en Ciencia de Datos · Universidad de los Andes

## ¿De qué trata?

**Pregunta:** ¿En qué medida cambia la identificación de países que han logrado desacoplar su crecimiento económico de las emisiones de CO₂ al comparar las emisiones territoriales con las asociadas al consumo?

Para cada país se compara el crecimiento del PIB con el de sus emisiones de CO₂ entre un año inicial y un año final (por defecto 1990 y 2023) y se clasifica su desacoplamiento como absoluto, relativo o inexistente, dos veces: con las emisiones producidas dentro del país (territoriales) y con las asociadas a lo que consume (que incluyen el comercio internacional). El análisis está dirigido a un comité técnico de desarrollo sostenible, para identificar **países referentes** y **países que requieren diagnóstico adicional**.

## Dashboard

- **En línea:** _(agregar el link de Streamlit Cloud)_
- **Local:** desde la raíz del proyecto

```bash
pip install -r requirements.txt
streamlit run src/dashboard_desacoplamiento.py
```

## Datos

| Archivo (`data/raw/`) | Contenido | Productor original | Unidad |
|---|---|---|---|
| `gdp-worldbank.csv` | PIB real, PPA | Banco Mundial, Eurostat, OCDE y FMI (2026) | dólares internacionales de 2021 |
| `territorial.csv` | Emisiones anuales de CO₂ dentro del país | Global Carbon Budget (2026) | toneladas de CO₂ |
| `consumo.csv` | Emisiones anuales de CO₂ asociadas al consumo | Global Carbon Budget (2026) | toneladas de CO₂ |
| `poblacion.csv` | Población | HYDE, Gapminder, UN WPP | personas |

Todas se descargaron de [Our World in Data](https://ourworldindata.org/co2-emissions) (licencia CC BY 4.0). Unidad de análisis: país-año. Panel integrado: 118 países, 1990–2023.

## Estructura

```
├── data/
│   ├── raw/          datos originales (no se editan)
│   └── processed/    datos_integrados.csv (país-año, alimenta el dashboard) y clasificacion_paises.csv (país)
├── notebooks/
│   ├── 01_preparacion_datos.ipynb   revisión, limpieza e integración → datos_integrados.csv
│   └── 02_analisis.ipynb            análisis, hallazgos, sesgos y limitaciones
├── src/
│   └── dashboard_desacoplamiento.py dashboard de Streamlit
├── outputs/figures/  gráficos generados por 02_analisis.ipynb
├── docs/             documento del proyecto
├── references/       reunión con el profesor y material de apoyo
├── requirements.txt
└── README.md
```

## Cómo reproducir el análisis

1. `pip install -r requirements.txt`
2. Ejecutar `notebooks/01_preparacion_datos.ipynb` (genera `data/processed/datos_integrados.csv`).
3. Ejecutar `notebooks/02_analisis.ipynb` (genera `clasificacion_paises.csv` y las figuras).
4. Abrir el dashboard con `streamlit run src/dashboard_desacoplamiento.py`.

El notebook de análisis reproduce el cálculo del dashboard (año inicial frente a año final), así que sus cifras coinciden con las que muestra el dashboard por defecto.

## Resultados principales (1990 frente a 2023, valores por defecto del dashboard)

- 26 de 116 países (22,4 %) cambian de clase al pasar de la contabilidad territorial a la de consumo; con otros años el porcentaje es similar (19 %–22 %).
- 38 países logran desacoplamiento absoluto con la contabilidad territorial y 30 con la de consumo; 28 lo logran con ambas (referentes).
- 10 países reducen su CO₂ territorial mientras su CO₂ de consumo crece (requieren diagnóstico).
- El desacoplamiento absoluto se concentra en países de ingreso alto.

## Limitaciones

- Solo ~120 países tienen emisiones de consumo; los comparables suman el 97 % del PIB mundial, pero quedan fuera muchos países pequeños y de bajos ingresos.
- En Bélgica, Luxemburgo, Sudáfrica, Namibia y Botsuana, el CO₂ de consumo de los años 90 es una copia del territorial; si el año inicial cae en esa década, su variación de consumo no es confiable.
- Solo CO₂ fósil e industrial; el análisis es descriptivo y no establece causalidad.
