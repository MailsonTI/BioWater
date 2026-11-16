
import sqlite3
from pathlib import Path
from datetime import datetime

import pandas as pd


DATABASE_FILE = Path(__file__).with_name("biowater.db")


def initialize_database():
    with sqlite3.connect(DATABASE_FILE) as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS samples (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
                ph REAL NOT NULL,
                temperature REAL NOT NULL,
                dissolved_oxygen REAL NOT NULL,
                collected_at TEXT
            )
        """)

        columns = [
            row[1]
            for row in connection.execute(
                "PRAGMA table_info(samples)"
            ).fetchall()
        ]

        if "collected_at" not in columns:
            connection.execute("""
                ALTER TABLE samples
                ADD COLUMN collected_at TEXT
            """)

        if "turbidity" not in columns:
            connection.execute("""
                ALTER TABLE samples
                ADD COLUMN turbidity REAL
            """)

        if "conductivity" not in columns:
            connection.execute("""
                ALTER TABLE samples
                ADD COLUMN conductivity REAL
            """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS deleted_samples (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
                ph REAL NOT NULL,
                temperature REAL NOT NULL,
                dissolved_oxygen REAL NOT NULL,
                collected_at TEXT,
                deleted_at TEXT
            )
        """)
        deleted_columns = [
            row[1]
            for row in connection.execute(
                "PRAGMA table_info(deleted_samples)"
            ).fetchall()
        ]

        if "turbidity" not in deleted_columns:
            connection.execute("""
                ALTER TABLE deleted_samples
                ADD COLUMN turbidity REAL
            """)

        if "conductivity" not in deleted_columns:
            connection.execute("""
                ALTER TABLE deleted_samples
                ADD COLUMN conductivity REAL
            """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS app_settings (
                setting TEXT PRIMARY KEY,
                value TEXT
            )
        """)


def get_unit_system():
    with sqlite3.connect(DATABASE_FILE) as connection:

        result = connection.execute("""
            SELECT value
            FROM app_settings
            WHERE setting = 'unit_system'
        """).fetchone()

        if result is None:
            return "SI"

        return result[0]


def set_unit_system(unit_system):

    if unit_system not in ("SI", "US"):
        raise ValueError("Invalid unit system.")

    with sqlite3.connect(DATABASE_FILE) as connection:

        connection.execute("""
            INSERT OR REPLACE INTO app_settings
            (setting, value)
            VALUES ('unit_system', ?)
        """, (unit_system,))

def was_database_reset():
    with sqlite3.connect(DATABASE_FILE) as connection:
        result = connection.execute("""
            SELECT value
            FROM app_settings
            WHERE setting = 'database_reset'
        """).fetchone()

        return result is not None and result[0] == "1"


def load_samples():
    with sqlite3.connect(DATABASE_FILE) as connection:
        return pd.read_sql_query("""
            SELECT
                location AS "Local",
                ph AS "pH",
                temperature AS "Temperatura (°C)",
                dissolved_oxygen AS "Oxigênio (mg/L)",
                turbidity AS "Turbidity (NTU)",
                conductivity AS "Conductivity (µS/cm)",
                COALESCE(
                    collected_at,
                    'Data não registrada'
                ) AS "Data/Hora"
            FROM samples
            ORDER BY id
        """, connection)


def save_samples(data):
    data = data.copy()
    
    if "Turbidity (NTU)" not in data.columns:
        data["Turbidity (NTU)"] = None

    if "Conductivity (µS/cm)" not in data.columns:
        data["Conductivity (µS/cm)"] = None

    if "Data/Hora" not in data.columns:
        data["Data/Hora"] = (
            datetime.now()
            .astimezone()
            .isoformat(timespec="seconds")
        )

    rows = data[
        [
            "Local",
            "pH",
            "Temperatura (°C)",
            "Oxigênio (mg/L)",
            "Turbidity (NTU)",
            "Conductivity (µS/cm)",
            "Data/Hora"
        ]
    ].itertuples(index=False, name=None)

    with sqlite3.connect(DATABASE_FILE) as connection:
        connection.executemany("""
            INSERT INTO samples (
                location,
                ph,
                temperature,
                dissolved_oxygen,
                turbidity,
                conductivity,
                collected_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, rows)

def archive_and_clear_samples():
    try:
        with sqlite3.connect(DATABASE_FILE) as connection:

            archived_at = (
                datetime.now()
                .astimezone()
                .isoformat(timespec="seconds")
            )

            connection.execute("""
                INSERT INTO deleted_samples (
                    location,
                    ph,
                    temperature,
                    dissolved_oxygen,
                    turbidity,
                    conductivity,
                    collected_at,
                    deleted_at
                )
                SELECT
                    location,
                    ph,
                    temperature,
                    dissolved_oxygen,
                    turbidity,
                    conductivity,
                    collected_at,
                    ?
                FROM samples
            """, (archived_at,))

            connection.execute("""
                DELETE FROM samples
            """)

            connection.execute("""
                INSERT OR REPLACE INTO app_settings
                (setting, value)
                VALUES ('database_reset', '1')
            """)

    except sqlite3.Error:
        raise


def restore_archived_samples():
    with sqlite3.connect(DATABASE_FILE) as connection:

        cursor = connection.execute("""
            INSERT INTO samples (
                location,
                ph,
                temperature,
                dissolved_oxygen,
                turbidity,
                conductivity,
                collected_at
            )
            SELECT
                d.location,
                d.ph,
                d.temperature,
                d.dissolved_oxygen,
                d.turbidity,
                d.conductivity,
                d.collected_at
            FROM deleted_samples AS d
            WHERE NOT EXISTS (
                SELECT 1
                FROM samples AS s
                WHERE
                    s.location IS d.location
                    AND s.ph IS d.ph
                    AND s.temperature IS d.temperature
                    AND s.dissolved_oxygen IS d.dissolved_oxygen
                    AND s.turbidity IS d.turbidity
                    AND s.conductivity IS d.conductivity
                    AND s.collected_at IS d.collected_at
            )
        """)

        restored_count = cursor.rowcount

        connection.execute("DELETE FROM deleted_samples")

        connection.execute("""
            INSERT OR REPLACE INTO app_settings
            (setting, value)
            VALUES ('database_reset', '0')
        """)

    return restored_count

def count_archived_samples():
    with sqlite3.connect(DATABASE_FILE) as connection:
        result = connection.execute("""
            SELECT COUNT(*) FROM deleted_samples
        """).fetchone()

        return result[0]
