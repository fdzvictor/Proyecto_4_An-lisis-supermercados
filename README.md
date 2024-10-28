# Análisis de Precios de Supermercados

## Descripción del Proyecto

Este proyecto consiste en el scraping de precios de diferentes supermercados utilizando **BeautifulSoup** y **Selenium**. Los datos obtenidos se almacenan en una base de datos en **PostgreSQL** para facilitar la consulta y el análisis de valores atípicos. 

### Objetivos

- Extraer datos de precios de productos esenciales y no esenciales.
- Realizar un análisis exploratorio de datos (EDA) para identificar tendencias y patrones en los precios.
- Comparar los precios entre diferentes supermercados.

## Herramientas Utilizadas

- **Python**: Lenguaje de programación.
- **BeautifulSoup**: Para el scraping de datos de páginas web.
- **Selenium**: Para automatizar la interacción con los navegadores.
- **PostgreSQL**: Base de datos para almacenar y consultar los datos extraídos.
- **Pandas**: Para la manipulación y análisis de datos.
- **Matplotlib / Seaborn**: Para la visualización de datos.

## Análisis Realizado

### Conclusiones Clave

1. **Aceite de Oliva**:
   - Ha fluctuado considerablemente en los últimos 30 días.
   - El cambio neto porcentual indica un ligero descenso en comparación con el precio en el momento t-1.
   - Los supermercados **Día** y **Mercadona** tienen los precios medios más bajos.
   - **Hipercor** y **Carrefour** presentan los mayores valores atípicos.

2. **Aceite de Girasol**:
   - Ha experimentado el mayor aumento de precio.
   - **Alcampo** ofrece los precios más bajos en general.
   - **Carrefour** no solo tiene valores atípicos más altos, sino también una mayor distribución de precios.

3. **Leche**:
   - **Carrefour** e **Hipercor** son los supermercados con más valores atípicos.
   - **Alcampo**, **Día**, y **Mercadona** tienen una media de precios ligeramente más alta, con una mayor variabilidad.

4. **Análisis de Productos**:
   - Se han clasificado los productos en esenciales (Aceite de Girasol y Leche) y no esenciales (Aceite de Oliva).
   - **Día** tiene el precio más alto en productos esenciales, mientras que **Eroski** tiene el más bajo.
   - La mayor caída de precios ha sido registrada en **Carrefour**.
   - **Alcampo** muestra los precios más altos para el Aceite de Oliva, posiblemente debido a su amplia gama de productos.
   - **Hipercor** ha mostrado la mayor variabilidad en precios del Aceite de Oliva, siendo **Eroski** el más barato en la actualidad.

