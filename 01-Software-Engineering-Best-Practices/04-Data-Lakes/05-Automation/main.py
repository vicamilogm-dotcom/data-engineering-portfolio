from scraper.main import main as pipeline_main


def run_pipeline(request):
    """
    Entry point HTTP de la Cloud Function.
    """
    return pipeline_main(request)
