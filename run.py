"""
This is where the web application starts running
"""
from app.index import create_app
app = create_app()

if __name__ == "__main__":
    app.secret_key = 'mysecret'
    app.run(port=8080, host="0.0.0.0", debug=True)