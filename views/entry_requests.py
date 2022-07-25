import sqlite3
import json

from models import Entry, Mood, Tag



def get_all_entries():
    """
    Gets all entries from the database

    RETURNS:
        string: JSON serialized string of the contents of the entries table.
    """

    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            m.label mood_label
        FROM Entry e
        JOIN Mood m 
            ON e.mood_id = m.id
        """)

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'],
                          row['entry'], row['mood_id'], row['date'], )

            mood = Mood(row['mood_id'], row['mood_label'])

            entry.mood = mood.__dict__

            # in the for loop, making a sql execution to get the tags for the entry.
            # in the sql call using row['id'] for the
            # WHERE clause, as if it was not there, all tags return for each entry.
            db_cursor.execute("""
            SELECT 
                et.id,
                t.id tag_id,
                t.name tag_name
            FROM Entrytag et
            JOIN Tag t 
                ON et.tag_id = t.id
            WHERE et.entry_id = ?    
            """, (row['id'], ))

            tags = []
            gottags = db_cursor.fetchall()

            for row in gottags:
                tag = Tag(row['tag_id'], row['tag_name'])

                tags.append(tag.__dict__)

            entry.tags = tags

            entries.append(entry.__dict__)

    return json.dumps(entries)


def get_single_entry(id):
    """
    Gets the requested entry from the database

    Args:
        id(int): The id of the requested entry

    Returns:
        string: JSON serialized string of the entry from the database
    """

    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date, 
            m.label mood_label
        FROM Entry e
        JOIN Mood m ON e.mood_id = m.id
        WHERE e.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        entry = Entry(data['id'], data['concept'], data['entry'],
                      data['mood_id'], data['date'])

        mood = Mood(data['mood_id'], data['mood_label'])

        entry.mood = mood.__dict__

    return json.dumps(entry.__dict__)


def delete_entry(id):
    """
    Removes the selected database from the list

    Args:
        id (INT): The id of the entry from the database
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            DELETE from entry
            WHERE id = ?
        """, (id, ))


def get_entries_by_search(search_term):
    """
    Gets the entries that have the search terms in the entry

    Args:
        search_term (STRING): terms typed into the search bar

    Returns:
        Serialized string of the data
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # changing the search_term query to an f-string so that it
        # can be read by python in the tuple
        db_cursor.execute("""
        SELECT 
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date
        FROM Entry e
        WHERE e.entry LIKE ?
        """, (f"%{search_term}%", ))

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'],
                          row['entry'], row['mood_id'], row['date'], )

            entries.append(entry.__dict__)

    return json.dumps(entries)


def create_entry(new_entry):
    """
    Creates a new entry into the database

    Args:
        new_entry (dict): New entry being added

    RETURNS:
        dict: The entry that was added with the new id
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Entry
            ( concept, entry, mood_id, date )
        VALUES ( ?, ?, ?, ?)
        """, (new_entry['concept'], new_entry['entry'], new_entry['moodId'], new_entry['date'] ))

        id = db_cursor.lastrowid

        new_entry['id'] = id

        for tag in new_entry["tags"]:
            db_cursor.execute("""
        INSERT INTO Entrytag
            ( entry_id, tag_id )
        VALUES ( ?, ?)
        """, (id, tag))

    return json.dumps(new_entry)


def update_entry(id, updated_entry):
    """
    Updates an entry in the database

    Args:
        id(int): The id of the entry
        updated_entry (dict): The updated entry dictionary
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Entry
            SET
                concept = ?, 
                entry = ?,
                mood_id = ?,
                date = ?
        WHERE id = ?
        """, (updated_entry['concept'], updated_entry['entry'],
              updated_entry['moodId'], updated_entry['date'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True


def get_entries_by_mood(mood_id):
    """
    Gets the entry by the status

    Args:
        status(string): The status from the query params of the request

    Returns:
        Serialized sting of the data
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date
        FROM Entry e
        WHERE e.mood_id LIKE ?
        """, (mood_id, ))

        entries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'],
                          row['entry'], row['mood_id'], row['date'])

            entries.append(entry.__dict__)

    return json.dumps(entries)
