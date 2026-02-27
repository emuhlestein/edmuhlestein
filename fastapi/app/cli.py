from typing import Optional
import typer
import os
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
    typer.echo(f"POSTGRES_USER      : {settings.POSTGRES_USER}")
    typer.echo(f"POSTGRES_DB      : {settings.POSTGRES_DB}")
    typer.echo(f"POSTGRES_PASSWORD      : {settings.POSTGRES_PASSWORD}")
    # typer.echo(f"ENVIRONMENT        : {settings.ENVIRONMENT}")
    typer.echo(f"DEBUG              : {settings.DEBUG}")
    typer.echo(f"SECRET_KEY              : {settings.SECRET_KEY}")
    typer.echo(f"ALGORITHM              : {settings.ALGORITHM}")
    typer.echo(f"ACCESS_TOKEN_EXPIRE_MINUTES              : {settings.ACCESS_TOKEN_EXPIRE_MINUTES}")
    typer.echo(f"REFRESH_TOKEN_EXPIRE_DAYS              : {settings.REFRESH_TOKEN_EXPIRE_DAYS}")


    url = make_url(str(settings.DATABASE_URL))
    typer.echo(f"URL : {url}")

    admin_url = url.set(database="postgres")
    typer.echo(f"ADMIN_URL : {admin_url}")

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
        # Modern 2.0 style
        stmt = select(User).where(User.email == "admin@example.com")
        admin = session.execute(stmt).scalars().one_or_none()

        if not admin:
            hashed_password = pwd_context.hash("admin123")
            new_admin = User(
                email="admin@example.com",
                hashed_password=hashed_password,
                user_role="admin",
            )
            session.add(new_admin)
            session.commit()
            typer.echo("👤 Admin user created: admin@example.com / admin123")
        else:
            typer.echo("ℹ️ Admin user already exists.")
    
# cli.py (add this command)

@cli.command(name="dump-users")
def dump_users(
    limit: int = typer.Option(
        50,
        "--limit", "-l",
        help="Maximum number of rows to show (0 = show all)"
    ),
    show_passwords: bool = typer.Option(
        False,
        "--show-passwords",
        help="Also show hashed passwords (use with caution)"
    )
):
    """
    Display contents of the users table.
    """
    db = SessionLocal()
    try:
        query = db.query(User).order_by(User.id.asc())
        
        if limit > 0:
            query = query.limit(limit)
        
        users = query.all()
        
        if not users:
            typer.echo("No users found in the database.")
            return
        
        # Header
        header = f"{'ID':<6} {'Email':<30} {'Full Name':<20} {'Role':<12} {'Active':<8} {'Created At':<20}"
        if show_passwords:
            header += " Hashed Password (truncated)"
        
        typer.echo(header)
        typer.echo("-" * (len(header) + 10))  # rough separator
        
        for user in users:
            created = (
                user.created_at.strftime("%Y-%m-%d %H:%M")
                if user.created_at
                else "—"
            )
            
            line = (
                f"{user.id:<6} "
                f"{user.email:<30} "
                f"{(user.full_name or '—'):<20} "
                f"{(user.user_role or '—'):<12} "   # adjust if field name differs
                f"{str(user.is_active):<8} "
                f"{created:<20}"
            )
            
            if show_passwords:
                hashed_preview = (
                    user.hashed_password[:20] + "..." 
                    if user.hashed_password 
                    else "—"
                )
                line += f" {hashed_preview}"
            
            typer.echo(line)
        
        typer.echo(f"\nTotal users shown: {len(users)}")
        
    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
    finally:
        db.close()




if __name__ == "__main__":
    cli()