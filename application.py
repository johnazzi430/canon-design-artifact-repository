import os
from server import app

application = app

if __name__ == "__main__":
#    app.run()
    application.run(port=5000)
