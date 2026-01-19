from typing import Optional
import typer
from passlib.context import CryptContext
from sqlalchemy import text, select
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url

from database import engine, SessionLocal      # sync engine + sessionmaker
from models.base import Base
from models.user import User
from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
cli = typer.Typer(help="Database Management CLI")

def get_admin_engine():
    url = make_url(str(settings.DATABASE_URL))
    admin_url = url.set(database="postgres")
    return create_engine(admin_url, isolation_level="AUTOCOMMIT")

@cli.command("show-env")
def show_env():
    typer.secho("Current DATABASE environment variables:", fg=typer.colors.GREEN, bold=True)
    typer.echo("")

    # Method 1: Direct os.environ (always works)
    typer.echo(f"DATABASE_URL       : {os.getenv('DATABASE_URL', 'Not set')}")
    typer.echo(f"POSTGRES_USER      : {os.getenv('POSTGRES_USER', 'Not set')}")
    typer.echo(f"POSTGRES_PASSWORD  : {os.getenv('POSTGRES_PASSWORD', 'Not set')}")
    typer.echo(f"POSTGRES_DB        : {os.getenv('POSTGRES_DB', 'Not set')}")
    typer.echo(f"POSTGRES_HOST      : {os.getenv('POSTGRES_HOST', 'Not set')}")
    typer.echo("")

    # Method 2: If you use Pydantic Settings (recommended)
    typer.secho("From Settings object:", fg=typer.colors.CYAN, bold=True)
    typer.echo(f"DATABASE_URL       : {settings.DATABASE_URL}")
    typer.echo(f"ENVIRONMENT        : {settings.ENVIRONMENT}")
    typer.echo(f"DEBUG              : {settings.DEBUG}")

@cli.command()
def create_db():
    try:
        admin_engine = get_admin_engine()
        db_name = str(settings.DATABASE_URL).rsplit("/", 1)[-1]
        with admin_engine.connect() as conn:
            check = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :name"), {"name": db_name}
            )
            if not check.scalar():
                conn.execute(text(f'CREATE DATABASE "{db_name}"'))
                typer.echo(f"🚀 Database '{db_name}' created.")
            else:
                typer.echo(f"✅ Database '{db_name}' already exists.")
    finally:
        admin_engine.dispose()


@cli.command()
def init_tables():
    Base.metadata.create_all(bind=engine)
    typer.echo("📊 All tables created successfully.")

@cli.command()
def reset_db():
    confirm = typer.confirm("Are you sure you want to drop all data?")
    if not confirm:
        raise typer.Abort()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    typer.echo("♻️ Database has been reset.")
    

@cli.command()
def seed_data():
    with SessionLocal() as session:
        result = session.execute(select(User).where(User.email == "admin@example.com"))
        admin = result.scalars().first()
        if not admin:
            hashed_password = pwd_context.hash("admin123")
            new_admin = User(
                email="admin@example.com",
                hashed_password=hashed_password,
                is_superuser=True,
            )
            session.add(new_admin)
            session.commit()
            typer.echo("👤 Admin user created: admin@example.com / admin123")
        else:
            typer.echo("ℹ️ Admin user already exists.")
    

if __name__ == "__main__":
    cli()