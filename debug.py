# Par exemple, créez un fichier debug.py à la racine de votre projet
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
