import sqlite3
import json

from models import Mood


def get_all_moods():
    """
    Gets all moods from the database

    RETURNS:
        string: JSON serialized string of the contents of the moods table
    """

    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            m.id,
            m.label
        FROM Mood m
        """)

        moods = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            mood = Mood(row['id'], row['label'])

            moods.append(mood.__dict__)

    return json.dumps(moods)
