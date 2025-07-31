#!/usr/bin/env python3
"""
Database status and health check script for OAuth Auth Backend.

This script connects to the database and provides a comprehensive status report.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sqlalchemy import text
from src.core.database import AsyncSessionLocal
from src.models import User, Role, AuditLog


async def check_database_status():
    """Check database connectivity and status."""
    try:
        async with AsyncSessionLocal() as session:
            # Test basic connectivity
            result = await session.execute(text("SELECT version()"))
            pg_version = result.scalar()
            print(f"✅ Database Connection: OK")
            print(f"📊 PostgreSQL Version: {pg_version.split()[1]}")
            
            # Check table counts
            tables = {
                "users": User,
                "roles": Role, 
                "audit_logs": AuditLog
            }
            
            print("\n📋 Table Status:")
            for table_name, model in tables.items():
                result = await session.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                count = result.scalar()
                print(f"   {table_name:12}: {count:4} records")
            
            # Check user-role relationships
            result = await session.execute(text("SELECT COUNT(*) FROM user_roles"))
            ur_count = result.scalar()
            print(f"   user_roles  : {ur_count:4} relationships")
            
            # Check admin user
            result = await session.execute(
                text("SELECT u.email, r.name FROM users u JOIN user_roles ur ON u.id = ur.user_id JOIN roles r ON r.id = ur.role_id WHERE u.email = 'admin@example.com'")
            )
            admin_info = result.fetchone()
            
            print("\n👤 Admin User Status:")
            if admin_info:
                print(f"   Email: {admin_info[0]}")
                print(f"   Role:  {admin_info[1]}")
                print("   ✅ Admin user configured correctly")
            else:
                print("   ❌ Admin user not found or not configured")
                
            # Check recent audit logs
            result = await session.execute(
                text("SELECT action, resource_type, performed_by FROM audit_logs ORDER BY timestamp DESC LIMIT 5")
            )
            recent_logs = result.fetchall()
            
            print("\n📝 Recent Audit Logs:")
            for log in recent_logs:
                print(f"   {log[0]:15} {log[1]:8} by {log[2]}")
                
        print("\n🎉 Database health check completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database Error: {e}")
        return False


async def main():
    """Main function."""
    print("🔍 OAuth Auth Backend - Database Status Check")
    print("=" * 50)
    
    success = await check_database_status()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
