# catalyst
1. Project Setup:
    Create a project directory and set up a virtual environment:
        i. mkdir fastapi-app
        ii. cd fastapi-app
        iii. python3 -m venv venv
        iv. source venv/bin/activate

2. Installation:
    Insatll all the packages required from requirements.txt
        i. pip install -r requirements.txt

3. Project Structure
        fastapi-app/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── models.py
    │   ├── schemas.py
    │   ├── database.py
    │   ├── auth.py
    │   ├── celery_worker.py
    │   ├── crud.py
    │   ├── templates/
    │   │   ├── base.html
    │   │   ├── login.html
    │   │   ├── signup.html
    │   │   ├── upload.html
    │   │   ├── query.html
    │   │   └── manage.html
    ├── celery_config.py
    ├── alembic/
    │   └── ...
    └── requirements.txt

4. Database Migration
    Set up Alembic for database migrations. Create the Alembic configuration files and run the initial migration.

    4.1 alembic.ini Configuration
        Ensure you have alembic.ini in your project root configured with the appropriate database URL.

    4.2 env.py Configuration
        Modify env.py inside the alembic directory to import your SQLAlchemy models. This allows Alembic to detect changes in your models and generate migration 
        scripts accordingly
            i. target_metadata = Base.metadata (Database model)


5. How to get alembic.ini file:
    The alembic.ini file is created when you initialize Alembic in your project
    5.1 Install Alembic
            i. pip install alembic

    5.2 Initialize Alembic
        The following command creates an alembic directory and an alembic.ini file in your project root.
            i. alembic init alembic
        
        Open the alembic.ini file and configure the database URL. Look for the sqlalchemy.url key and set it to your database connection string.


5. Running Migrations
    Initialize Alembic and run the initial migration:
    5.1 Create the Initial Migration
        Once the alembic.ini and env.py files are configured, you can create the initial migration script. This script will capture the current state of your 
        models and create the corresponding tables in the database.
            i. alembic revision --autogenerate -m "Initial migration"

    5.2 Apply the Migration
        Finally, apply the migration to the database:
            ii. alembic upgrade head


6. Running the Application:
    6.1 Start the FastAPI server:
        uvicorn app.main:app --reload

    6.2 Start the Celery worker:
        celery -A app.celery_worker.celery_app worker --loglevel=info

    6.3 Navigate to the relevant endpoints to use the application.
