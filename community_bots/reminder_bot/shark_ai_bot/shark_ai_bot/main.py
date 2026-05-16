import functions_framework
from combined import app as flask_app

@functions_framework.http
def main(request):
    """Точка входа для Google Cloud Function."""
    return flask_app(request)
  
