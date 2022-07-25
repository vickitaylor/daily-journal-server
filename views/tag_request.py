import sqlite3
import json

from models import Tag


def get_all_tags():
    """
    Gets all tags from the database

    RETURNS:
        string: JSON serialized string of the contents of the tags table
    """

    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id,
            t.name
        FROM Tag t
        """)

        tags = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            tag = Tag(row['id'], row['name'])

            tags.append(tag.__dict__)

    return json.dumps(tags)
