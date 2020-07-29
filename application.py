import os
from dotenv import load_dotenv

load_dotenv()

from server import app

application = app

if __name__ == "__main__":
    #    app.run()
    application.run(host="0.0.0.0", port=5000, debug=False)
