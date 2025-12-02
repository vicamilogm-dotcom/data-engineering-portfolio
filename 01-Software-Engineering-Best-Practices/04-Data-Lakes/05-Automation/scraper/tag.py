from google.cloud import datacatalog_v1
from google.api_core.exceptions import AlreadyExists
from datetime import datetime
import os
from google.protobuf import timestamp_pb2


def catalog_file(blob_path: str):
    """
    Crea (o recupera) un Entry en Data Catalog para el archivo dado
    y le agrega un Tag con metadata de origen.

    :param blob_path: ruta del archivo dentro del bucket, por ejemplo:
                      "raw/hackernews/stories/2025/12/02/stories.csv"
    """
    # 1) Cliente de Data Catalog
    client = datacatalog_v1.DataCatalogClient()

    # 2) Variables de entorno
    project_id = os.environ["PROJECT_ID"]
    bucket_name = os.environ["LAKE_BUCKET"]
    location = os.environ.get("LAKE_LOCATION", "us")

    # IDs creados con gcloud
    entry_group_id = "hn_day"
    tag_template_id = "hn_day_template"

    # 3) Parsear la fecha desde el blob_path
    # Esperamos algo tipo: raw/hackernews/stories/YYYY/MM/DD/stories.csv
    parts = blob_path.split("/")
    try:
        # Tomamos los últimos 4 elementos: YYYY / MM / DD / archivo
        year, month, day = map(int, parts[-4:-1])
        run_date = datetime(year, month, day).date()
    except (ValueError, IndexError):
        # Si por algún motivo no cumple el patrón, usamos hoy
        run_date = datetime.utcnow().date()

    # 4) Construir nombres de recursos de Data Catalog
    entry_group_name = datacatalog_v1.DataCatalogClient.entry_group_path(
        project_id, location, entry_group_id
    )

    # ID único para el entry (un día = un entry)
    entry_id = f"hn_{run_date.strftime('%Y_%m_%d')}"
    entry_name = datacatalog_v1.DataCatalogClient.entry_path(
        project_id, location, entry_group_id, entry_id
    )

    # 5) Definir el Entry para el archivo en GCS
    entry = datacatalog_v1.Entry()
    entry.display_name = f"Hacker News stories {run_date.isoformat()}"
    entry.description = "Front page Hacker News stories for this day"
    # Tipo definido por el usuario, indicando que es un archivo en GCS
    entry.user_specified_type = "gcs_file"
    entry.user_specified_system = "gcs"

    # Especificación del fileset de GCS
    entry.gcs_fileset_spec = datacatalog_v1.GcsFilesetSpec()
    entry.gcs_fileset_spec.file_patterns.append(
        f"gs://{bucket_name}/{blob_path}"
    )

    # 6) Crear o recuperar el Entry
    try:
        entry = client.create_entry(
            parent=entry_group_name,
            entry_id=entry_id,
            entry=entry
        )
    except AlreadyExists:
        entry = client.get_entry(name=entry_name)

    # 7) Crear el Tag basado en la plantilla
    tag_template_name = datacatalog_v1.DataCatalogClient.tag_template_path(
        project_id, location, tag_template_id
    )

    tag = datacatalog_v1.Tag()
    tag.template = tag_template_name

    # Campo source_system (STRING)
    tag.fields["source_system"] = datacatalog_v1.TagField()
    tag.fields["source_system"].string_value = "hackernews"

    # Campo source_date (TIMESTAMP)
    ts = timestamp_pb2.Timestamp()
    ts.FromDatetime(datetime.combine(run_date, datetime.min.time()))
    tag.fields["source_date"] = datacatalog_v1.TagField()
    tag.fields["source_date"].timestamp_value = ts

    # 8) Adjuntar Tag al Entry
    client.create_tag(parent=entry.name, tag=tag)

    # Opcional: retornar el entry por si lo quieres usar en otro lado
    return entry
