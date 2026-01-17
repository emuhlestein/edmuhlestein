import asyncio
import typer
from passlib.context import CryptContext
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

# Import your existing components
from database import engine
import models
from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
cli = typer.Typer(help="Database Management CLI")

async def get_admin_engine():
    """Connects to 'postgres' system db to perform CREATE/DROP DATABASE."""
    admin_url = str(settings.DATABASE_URL).replace(
        settings.DATABASE_URL.split("/")[-1], "postgres"
    )
    return create_async_engine(admin_url, isolation_level="AUTOCOMMIT")

@cli.command()
def create_db():
    """Create the physical database defined in settings."""
    async def _run():
        admin_engine = await get_admin_engine()
        db_name = settings.DATABASE_URL.split("/")[-1]
        async with admin_engine.begin() as conn:
            # Check if it exists
            check = await conn.execute(
                text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
            )
            if not check.scalar():
                await conn.execute(text(f"CREATE DATABASE {db_name}"))
                typer.echo(f"🚀 Database '{db_name}' created.")
            else:
                typer.echo(f"✅ Database '{db_name}' already exists.")
        await admin_engine.dispose()
    
    asyncio.run(_run())

@cli.command()
def init_tables():
    """Create all tables defined in your SQLAlchemy models."""
    async def _run():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        typer.echo("📊 All tables created successfully.")
    
    asyncio.run(_run())

@cli.command()
def reset_db():
    """DROP all tables and recreate them (WARNING: Destructive)."""
    confirm = typer.confirm("Are you sure you want to drop all data?")
    if not confirm:
        raise typer.Abort()

    async def _run():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        typer.echo("♻️ Database has been reset.")

    asyncio.run(_run())

@cli.command()
def seed_data():
    """Seed the database with a default admin user."""
    async def _run():
        async with AsyncSessionLocal() as session:
            # 1. Check if admin already exists
            # Replace 'User' and 'email' with your actual model/field names
            query = select(User).where(User.email == "admin@example.com")
            result = await session.execute(query)
            admin = result.scalar_one_or_none()

            if not admin:
                hashed_password = pwd_context.hash("admin123")
                new_admin = User(
                    email="admin@example.com",
                    hashed_password=hashed_password,
                    is_superuser=True
                )
                session.add(new_admin)
                await session.commit()
                typer.echo("👤 Admin user created: admin@example.com / admin123")
            else:
                typer.echo("ℹ️ Admin user already exists.")

    asyncio.run(_run())

if __name__ == "__main__":
    cli()