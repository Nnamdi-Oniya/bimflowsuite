import os
import django
import psycopg2
from psycopg2.extras import RealDictCursor
from django.conf import settings

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()


def check_database():
    """Check PostgreSQL database connection and schema"""
    print("PostgreSQL Database Inspection")
    print("=" * 60)

    # Get database config from Django settings
    db_config = settings.DATABASES["default"]

    print("Database Configuration:")
    print(f"   Engine: {db_config['ENGINE']}")
    print(f"   Name: {db_config['NAME']}")
    print(f"   User: {db_config['USER']}")
    print(f"   Host: {db_config['HOST']}:{db_config['PORT']}\n")

    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname=db_config["NAME"],
            user=db_config["USER"],
            password=db_config["PASSWORD"],
            host=db_config["HOST"],
            port=db_config["PORT"],
        )
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Get database size
        cursor.execute(
            """
            SELECT pg_size_pretty(pg_database.datsize) as size
            FROM pg_database
            WHERE datname = %s;
        """,
            [db_config["NAME"]],
        )
        size_result = cursor.fetchone()
        db_size = size_result["size"] if size_result else "Unknown"
        print("Connection successful!")
        print(f"Database size: {db_size}\n")

        # List all tables
        cursor.execute("""
            SELECT tablename FROM pg_tables
            WHERE schemaname = 'public'
            ORDER BY tablename;
        """)
        tables = cursor.fetchall()

        print(f"Found {len(tables)} tables:\n")
        for table in tables:
            table_name = table["tablename"]

            # Count rows in each table
            cursor.execute(f"SELECT COUNT(*) as count FROM {table_name};")
            count = cursor.fetchone()["count"]

            # Get columns info
            cursor.execute(
                """
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = %s
                ORDER BY ordinal_position
                LIMIT 5;
            """,
                [table_name],
            )
            columns = cursor.fetchall()
            column_str = ", ".join(
                [f"{col['column_name']}({col['data_type']})" for col in columns]
            )
            if len(columns) >= 5:
                column_str += ", ..."

            print(f"   ✓ {table_name}")
            print(f"     Rows: {count:,}")
            print(f"     Columns: {column_str}\n")

        conn.close()
        print("Database inspection completed successfully!")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

    return True


def check_django_models():
    """Check Django models and data"""
    print("\n Django Models & Data Check")
    print("=" * 60)

    try:
        from apps.users.models import Organization, RequestSubmission
        from apps.parametric_generator.models import Project, GeneratedIFC
        from apps.compliance_engine.models import ComplianceCheck, RulePack
        from apps.analytics.models import AnalyticsRun
        from django.contrib.auth import get_user_model
        
        User = get_user_model()

        # User & Organization data
        user_count = User.objects.count()
        org_count = Organization.objects.count()
        request_count = RequestSubmission.objects.count()

        print(f" Users: {user_count}")
        print(f" Organizations: {org_count}")
        print(f" Demo Requests: {request_count}\n")

        # Project data
        project_count = Project.objects.count()
        print(f"Projects: {project_count}")
        if project_count > 0:
            projects = Project.objects.all()[:5]
            for project in projects:
                print(
                    f"   - {project.name} (Project #: {project.project_number}, Status: {project.status})"
                )
        print()

        # IFC Generation data
        ifc_count = GeneratedIFC.objects.count()
        print(f"Generated IFCs: {ifc_count}")
        if ifc_count > 0:
            ifcs = GeneratedIFC.objects.all()[:5]
            for ifc in ifcs:
                status_icon = (
                    "✅"
                    if ifc.status == "completed"
                    else "⏳"
                    if ifc.status == "generating"
                    else "❌"
                )
                print(f"{status_icon} {ifc.asset_type} ({ifc.status})")
        print()

        # Compliance data
        compliance_count = ComplianceCheck.objects.count()
        print(f"Compliance Checks: {compliance_count}")
        if compliance_count > 0:
            checks = ComplianceCheck.objects.all()[:5]
            for check in checks:
                print(f"   - {check.rule_pack} ({check.status})")
        print()

        # Analytics data
        analytics_count = AnalyticsRun.objects.count()
        print(f"Analytics Runs: {analytics_count}")
        if analytics_count > 0:
            runs = AnalyticsRun.objects.all()[:5]
            for run in runs:
                print(
                    f"   - {run.analytics_type} ({run.created_at.strftime('%Y-%m-%d')})"
                )
        print()

        # Rule Packs
        rulepack_count = RulePack.objects.count()
        print(f"Rule Packs: {rulepack_count}")
        if rulepack_count > 0:
            packs = RulePack.objects.all()
            for pack in packs:
                print(f"   - {pack.name}")

        print("\nModel data inspection completed successfully!")
        return True

    except Exception as e:
        print(f"Models error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("   BIMFlow Suite - Database Inspection Tool")
    print("=" * 60 + "\n")

    db_ok = check_database()
    models_ok = check_django_models()

    if db_ok and models_ok:
        print("\n" + "=" * 60)
        print("All checks passed! Database is ready to use.")
        print("=" * 60 + "\n")
    else:
        print("\n" + "=" * 60)
        print("Some checks failed. Please review the errors above.")
        print("=" * 60 + "\n")
