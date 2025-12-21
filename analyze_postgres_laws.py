
import psycopg2

def analyze_postgres():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="opositaia",
            user="postgres",
            password="postgres"
        )
        cur = conn.cursor()
        
        print("🕵️  Conectado a PostgreSQL 'opositaia'")
        
        # Consultar esquema de tabla 'laws'
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'laws'")
        cols = [c[0] for c in cur.fetchall()]
        print(f"\n📋 Columnas en tabla 'laws': {cols}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    analyze_postgres()
