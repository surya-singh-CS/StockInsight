mkdir → Creates folders (directories).  -- 
New-Item → Creates anything (files, folders, registry keys, etc.).
e.g -->   New-Item CHEATSHEET.md -ItemType File

GIT -- ## git config

Set Git author name:

git config --global user.name "Your Name"

Set Git author email:
git config --global user.email "your-email@example.com"

Purpose:
Git records who created each commit.

* database 
app/
└── database/
    ├── connection.py
    └── base.py

connection.py -->  This file creates the connection between FastAPI and PostgreSQL.
Without connection.py, every API would have to connect to PostgreSQL by itself.
That would be like every room in your house having its own water pipeline.
Instead we create one central connection that everyone uses.

CENTRALIZE DB CONNECTION ---
Why don't you connect directly inside every API?

Good answer:
Because creating a single reusable engine and session factory avoids duplicate code, centralizes database configuration, and allows efficient connection management across the application.


base.py--> Responsible for:
Holding the parent class for all database models.
Later we'll write:
class User(Base):
Every table inherits from Base.