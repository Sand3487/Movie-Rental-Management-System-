import pymysql

# --- Database Connection ---
def create_connection():
    """Create and return a database connection."""
    try:
        connection = pymysql.connect(
            host="127.0.0.1",
            user="root",        
            password="sand@A3487",
            database="movierental",
            port=3306
        )
        if connection.open:
            print("Database connected successfully.")
            return connection
    except pymysql.MySQLError as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None
    
def close_connection(connection):
    """Safely close database connection."""
    if connection.open:
        connection.close()
        print("🔒 Database connection closed.")