from pymongo import MongoClient
from pymongo.errors import OperationFailure, ConfigurationError
import os, sys

DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_URI = os.environ.get("DB_URI")
try:
    client = MongoClient(
        f"mongodb+srv://{DB_USER}:{DB_PASS}@{DB_URI}/sharedb?retryWrites=true&w=majority"
    )
    client.admin.command('ismaster')
    db = client['sharedb']
except (OperationFailure, ConfigurationError) as e:
    # replace with logging function
    print(e)
    print("Database connection failed")
    sys.exit(1)
