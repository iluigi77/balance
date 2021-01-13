from app import app as application
from waitress import serve

if __name__ == "__main__":
    serve(application) # waitress
    