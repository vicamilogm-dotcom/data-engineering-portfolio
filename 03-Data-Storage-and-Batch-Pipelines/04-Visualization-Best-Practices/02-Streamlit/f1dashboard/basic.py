import altair as alt
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from timeit import default_timer as timer

# Establecer conexión con PostgreSQL usando las credenciales de Streamlit
conn_string = URL.create(**st.secrets["postgres"])
conn = create_engine(conn_string, echo=False)

# Lista de tablas disponibles en la base de datos
TABLES = [
    "races",
    "circuits",
    "constructor_results",
    "constructor_standings",
    "constructors",
    "driver_standings",
    "drivers",
    "lap_times",
    "pit_stops",
    "qualifying",
    "results",
    "seasons",
    "status",
]

# Función para cargar datos desde la base de datos
@st.cache_data
def load_data(table_name):
    """
    Carga los datos de una tabla seleccionada desde la base de datos.
    Args:
        table_name (str): Nombre de la tabla a cargar.
    Returns:
        pd.DataFrame: Datos cargados desde la base de datos.
    """
    data = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    return data

# Crear la página principal de la aplicación Streamlit
def create_main_page():
    """
    Crea la interfaz principal de la página de Streamlit:
    - Un título
    - Un subencabezado
    - Un widget para seleccionar una tabla desde el sidebar
    """
    st.title("Formula 1 Dashboard")
    st.info("Selecciona una tabla desde el panel lateral.")
    
    selected_table = st.sidebar.selectbox("Selecciona una tabla", TABLES)
    return selected_table

# Mostrar estadísticas resumen sobre los datos cargados
def summary_statistics(data):
    """
    Muestra estadísticas resumidas de los datos cargados.
    Args:
        data (pd.DataFrame): Datos cargados desde la base de datos.
    """
    st.subheader("Estadísticas Resumen")
    st.write(data.describe())

# Obtener los 5 mejores pilotos con más puntos
@st.cache_data
def top_drivers():
    """
    Consulta la base de datos para obtener los 5 mejores pilotos con más puntos.
    Returns:
        pd.DataFrame: Los 5 mejores pilotos y sus puntos totales.
    """
    query = """
    SELECT drivers.driver_name, SUM(driver_standings.points) AS total_points
    FROM driver_standings
    JOIN drivers ON driver_standings.driver_id = drivers.driver_id
    GROUP BY drivers.driver_name
    ORDER BY total_points DESC
    LIMIT 5;
    """
    top_drivers_data = pd.read_sql_query(query, conn)
    return top_drivers_data

# Obtener los puntos de Lewis Hamilton a lo largo de los años
@st.cache_data
def lewis_over_the_years():
    """
    Obtiene los puntos de Lewis Hamilton entre 2007 y 2018.
    Returns:
        pd.DataFrame: Los puntos de Lewis Hamilton a lo largo de los años.
    """
    query = """
    SELECT races.year, driver_standings.points
    FROM driver_standings
    JOIN races ON driver_standings.race_id = races.race_id
    WHERE driver_standings.driver_id = (SELECT driver_id FROM drivers WHERE driver_name = 'Lewis Hamilton')
    AND races.year BETWEEN 2007 AND 2018;
    """
    lewis_data = pd.read_sql_query(query, conn)
    return lewis_data

# Guardar los datos cargados en el estado de la sesión
def session_state(data):
    """
    Guarda los datos en el estado de la sesión para que estén disponibles en todas las páginas de la app.
    Args:
        data (pd.DataFrame): Datos a guardar en el estado de la sesión.
    """
    if 'data' not in st.session_state:
        st.session_state.data = data

# Código principal para la ejecución de la app
if __name__ == "__main__":
    selected_table = create_main_page()

    # Medir el tiempo para cargar los datos
    start = timer()
    data = load_data(selected_table)
    end = timer()
    st.sidebar.info(f"{round(end-start,4)} segundos para cargar los datos")

    # Mostrar los datos en la app
    st.dataframe(data)

    # Mostrar las estadísticas resumidas
    summary_statistics(data)

    # Guardar los datos en el estado de la sesión
    session_state(data)

    # Mostrar los 5 mejores pilotos
    st.subheader("Top 5 Pilotos")
    top_driver_data = top_drivers()
    st.write(top_driver_data)

    st.warning("Usa la biblioteca Altair para crear un gráfico de barras con los mejores pilotos.")
    # Crear un gráfico de barras con los mejores pilotos
    chart = alt.Chart(top_driver_data).mark_bar().encode(
        x='driver_name',
        y='total_points'
    )
    st.altair_chart(chart, use_container_width=True)

    # Mostrar los puntos de Lewis Hamilton a lo largo de los años
    st.subheader("Lewis Hamilton a lo largo de los años")
    lewis_years = lewis_over_the_years()

    # Convertir la columna de años a tipo datetime
    lewis_years["year"] = pd.to_datetime(lewis_years["year"], format="%Y")

    st.warning("Crea un gráfico de líneas con los puntos de Lewis Hamilton a lo largo de los años usando la biblioteca Altair.")
    # Crear un gráfico de líneas con los puntos de Lewis Hamilton
    line_chart = alt.Chart(lewis_years).mark_line().encode(
        x='year:T',
        y='points:Q'
    )
    st.altair_chart(line_chart, use_container_width=True)
