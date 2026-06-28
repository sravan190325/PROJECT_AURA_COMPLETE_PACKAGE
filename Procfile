web: gunicorn app:app
worker: python -m services.workbook_optimizer
release: python -c "import sqlite3; sqlite3.connect('project_aura.db')"
