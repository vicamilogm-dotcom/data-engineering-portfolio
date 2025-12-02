from datetime import datetime
from pathlib import Path

from scraper.scrape import scrape_hn
from scraper.upload import upload_to_lake
from scraper.tag import catalog_file

# Ruta del CSV en Cloud Functions
TMP_CSV_PATH = Path("/tmp/stories.csv")


def main(request=None):
    """
    Función principal del pipeline.
    'request' se usa cuando la llama la Cloud Function (HTTP),
    pero aquí no necesitamos leer nada de ella.
    """
    # Fecha de hoy
    date_today = datetime.now().strftime("%Y-%m-%d")

    # Scraping de Hacker News
    stories_df = scrape_hn(date_today)

    # Guardar CSV en /tmp
    stories_df.to_csv(TMP_CSV_PATH, index=False)

    # Subir al data lake usando la ruta /tmp/...
    blob_path = upload_to_lake(str(TMP_CSV_PATH))

    # Catalogar el archivo en Data Catalog
    catalog_file(blob_path)

    # Devolver un string (requerido por Cloud Functions HTTP)
    return "Pipeline ejecutado correctamente"


if __name__ == "__main__":
    print(main())
