"""
SQLite database handler for storing user nicknames and roles.
"""

import os
from contextlib import contextmanager
import sqlite3


class PersistenceDB:
    def __init__(self, db_path = "data/persistence.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.db_path = db_path
        self.create_tables()


    @contextmanager
    def get_connection(self):
        """Context manager for database connections with auto-commit/rollback."""
        connection = sqlite3.connect(self.db_path)
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
        finally:
            connection.close()


    def create_tables(self):
        """Create users and user_roles tables if they don't exist."""
        with self.get_connection() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER,
                    guild_id INTEGER,
                    nickname TEXT,
                    PRIMARY KEY (user_id, guild_id)
                )
            """)

            connection.execute("""
                CREATE TABLE IF NOT EXISTS user_roles (
                    user_id INTEGER,
                    guild_id INTEGER,
                    role_id INTEGER,
                    FOREIGN KEY (user_id, guild_id)
                        REFERENCES users(user_id, guild_id)
                        ON DELETE CASCADE,
                    PRIMARY KEY (user_id, guild_id, role_id)
                )
            """)


    def add_user(self, user_id, guild_id, nickname, role_ids):
        """Add or update user data."""
        with self.get_connection() as connection:
            connection.execute("""
                INSERT OR REPLACE INTO users (user_id, guild_id, nickname)
                VALUES (?, ?, ?)
            """, (user_id, guild_id, nickname))

            connection.execute("""
                DELETE FROM user_roles
                WHERE user_id = ? AND guild_id = ?
            """, (user_id, guild_id))

            for role_id in role_ids:
                connection.execute("""
                    INSERT INTO user_roles (user_id, guild_id, role_id)
                    VALUES (?, ?, ?)
                """, (user_id, guild_id, role_id))


    def remove_user(self, user_id, guild_id):
        """Delete user data."""
        with self.get_connection() as connection:
            connection.execute("""
                DELETE FROM users WHERE user_id = ? AND guild_id = ?
            """, (user_id, guild_id))

    def user_exists(self, user_id, guild_id):
        """Check if user exists in database"""
        with self.get_connection() as connection:
            user = connection.execute("""
                        SELECT 1 FROM users WHERE user_id = ? AND guild_id = ?
                    """, (user_id, guild_id)).fetchone()

            return user is not None


    def get_user(self, user_id, guild_id):
        """Retrieve stored nickname and roles for a user."""
        with self.get_connection() as connection:
            nickname = connection.execute("""
                SELECT nickname FROM users WHERE user_id = ? AND guild_id = ?
            """, (user_id, guild_id)).fetchone()

            roles = connection.execute("""
                SELECT role_id FROM user_roles WHERE user_id = ? AND guild_id = ?
            """, (user_id, guild_id)).fetchall()

            role_ids = []
            for role in roles:
                role_ids.append(role[0])

        return nickname[0], role_ids


db = PersistenceDB()