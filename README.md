# El costo invisible del progreso

Proyecto 2 · DATA-1002 Aplicaciones en Ciencia de Datos · Universidad de los Andes

## ¿De qué trata?

¿En qué medida cambia la identificación de países que han logrado desacoplar su crecimiento económico de las emisiones de CO₂ al comparar las emisiones territoriales con las asociadas al consumo?

El análisis clasifica a cada país (desacoplamiento absoluto, relativo o sin desacoplamiento) con las dos contabilidades y muestra cuáles cambian de clase. Está dirigido a un comité técnico de desarrollo sostenible y transición climática.

## Datos

| Fuente | Productor original | Archivo |
|---|---|---|
| CO₂ territorial per cápita | Global Carbon Budget (2026), vía Our World in Data | `data/raw/co2-emissions-per-capita.zip` |
| CO₂ basado en consumo per cápita | Global Carbon Budget (2026), vía Our World in Data | `data/raw/per-capita-consumption-based-co2-emissions.zip` |
| PIB real (PPA, dólares de 2021) | Banco Mundial (2026), vía Our World in Data | `data/raw/gdp-worldbank.zip` |
| Población | HYDE, Gapminder, UN WPP, vía Our World in Data | `data/raw/population.csv` |

Licencia: CC BY 4.0. Consultados el 22/11/2026. Unidad de análisis: país-año, 1990–2023.

## Estructura

```
├── data/
│   ├── raw/          datos originales (no se editan)
│   └── processed/    panel integrado y clasificación por país (alimentan el dashboard)
├── notebooks/
│   └── proyecto2.ipynb   carga, calidad, integración, análisis y hallazgos
├── outputs/
│   └── figures/      gráficos generados por el notebook
├── requirements.txt
└── README.md
```

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
jupyter notebook notebooks/proyecto2.ipynb   # ejecutar todas las celdas
```

El notebook genera `data/processed/` y `outputs/figures/`.

## Resultados principales

- 26 de 112 países (23 %) cambian de clase al pasar de la contabilidad territorial a la de consumo.
- 34 países logran desacoplamiento absoluto con la contabilidad territorial y 26 con la de consumo; 25 lo logran con ambas.
- 9 países reducen su CO₂ territorial mientras su CO₂ de consumo crece.
- Limitación: solo ~120 países tienen emisiones de consumo; quedan fuera muchos países pequeños y de bajos ingresos.
