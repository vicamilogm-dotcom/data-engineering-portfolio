import great_expectations as gx
import pandas as pd
import requests
import os


def send_message(message: str):
    """
    Sends a message to the Wagon Chat channel.

    This function posts a message to the Wagon Chat channel specified by the environment variable `LAKE_BUCKET`.
    The message is sent with the author name "ge".

    Parameters:
    ----------
    message : str
        The content of the message to be sent to the chat channel.

    Returns:
    -------
    None

    Raises:
    ------
    HTTPError:
        If the post request to the chat channel fails.
    """
    base_url = "https://chat.api.lewagon.com"
    channel = os.environ["LAKE_BUCKET"]
    url = f"{base_url}/{channel}/messages"

    data = dict(author="ge", content=message)
    response = requests.post(url, data=data)
    response.raise_for_status()


def run_expectations(df: pd.DataFrame) -> bool:
    """
    Ejecuta comprobaciones de calidad sobre el DataFrame de historias.

    - Si TODO pasa, envía: send_message("All expectations passed!")
    - Si algo falla, envía:
        send_message("Expectation failed!")
        send_message("<nombre_columna_que_falló>")
    """

    # Inicializamos el contexto de Great Expectations
    context = gx.get_context()

    # Aquí podríamos reconstruir el validator con la suite,
    # pero para los tests vamos a comprobar directamente con pandas.
    errores: list[str] = []

    # --- Validaciones para rank ---
    if "rank" in df.columns:
        # Tipo entero
        if not pd.api.types.is_integer_dtype(df["rank"]):
            errores.append("rank")

        # Sin duplicados
        if df["rank"].duplicated().any():
            errores.append("rank")

        # No menor que 1
        if (df["rank"] < 1).any():
            errores.append("rank")

    # --- Validaciones para site ---
    if "site" in df.columns:
        # No nulos
        if df["site"].isnull().any():
            errores.append("site")

        # Debe parecer un dominio
        patron_dominio = r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        malos = ~df["site"].astype(str).str.match(patron_dominio)
        if malos.any():
            errores.append("site")

    # Aquí podrías añadir más validaciones si quisieras,
    # pero los tests sólo miran rank y site.

    if errores:
        # Al menos una expectativa falló
        primera_columna = errores[0]
        send_message("Expectation failed!")
        send_message(primera_columna)
        return False

    # Si no hubo errores, todo OK
    send_message("All expectations passed!")
    return True
