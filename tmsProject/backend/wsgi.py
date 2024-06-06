from app import create_app
#to deploy the Flask application to production web 
# that support the WSGI (Web Server Gateway Interface) standard, such as Gunicorn.Not implemented!
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
