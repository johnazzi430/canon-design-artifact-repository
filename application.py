import os
from server import app

from dotenv import load_dotenv

application = app

if __name__ == "__main__":
#    app.run()
    application.run(host='0.0.0.0' , port=5000, debug=False)
