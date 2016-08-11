from project import restimatorApp
import os

if __name__ == "__main__": 
    port = int(os.environ.get("PORT", 5000))
    restimatorApp.run(host='0.0.0.0', port=port) # Start server with run method