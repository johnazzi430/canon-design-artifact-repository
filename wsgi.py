from server import app

application = app

if __name__ == "__main__":
#    app.run()
    application.run(host='0.0.0.0' , port='8080')
