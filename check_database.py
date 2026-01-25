import os
import django
import sqlite3
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bimflow.config.settings')
django.setup()

def check_database():
    print("🔍 Database Inspection")
    print("=" * 50)
    
    # Check if database file exists
    db_path = Path('db.sqlite3')
    if db_path.exists():
        print(f"✅ Database found: {db_path.absolute()}")
        print(f"📊 Size: {db_path.stat().st_size / 1024 / 1024:.2f} MB")
    else:
        print("❌ Database file not found!")
        return
    
    # Connect to SQLite database
    try:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        # List all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"\n📋 Found {len(tables)} tables:")
        for table in tables:
            table_name = table[0]
            # Count rows in each table
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"   - {table_name}: {count} rows")
            
            # Show first few rows for intent-related tables
            if 'intent' in table_name.lower():
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
                rows = cursor.fetchall()
                print(f"     Sample data: {rows[:2]}")  # Show first 2 rows
        
        conn.close()
        print("\n✅ Database connection successful!")
        
    except Exception as e:
        print(f"❌ Database error: {e}")

def check_django_models():
    print("\n🐍 Django Models Check")
    print("=" * 50)
    
    try:
        from intent_capture.models import IntentCapture, ProgramSpec
        from django.contrib.auth.models import User
        
        print(f"👤 Users: {User.objects.count()}")
        print(f"💡 Intents: {IntentCapture.objects.count()}")
        print(f"📋 Program Specs: {ProgramSpec.objects.count()}")
        
        # Show recent intents
        recent_intents = IntentCapture.objects.all()[:5]
        if recent_intents:
            print("\n📝 Recent Intents:")
            for intent in recent_intents:
                print(f"   - {intent.intent_text[:50]}... (by {intent.user})")
        
    except Exception as e:
        print(f"❌ Models error: {e}")

if __name__ == "__main__":
    check_database()
    check_django_models()