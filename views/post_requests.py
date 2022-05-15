import sqlite3
import json
from models import Post

POSTS = [
    {
        "id": 1,
        "user_id": 1,
        "category_id": 1,
        "title": "Test Title",
        "publication_date": '2022-04-03',
        "image_url": 'http://via.placeholder.com/150',
        "content": "Basic Content Test",
        "approved": 'Y'
    },
    {
        "id": 2,
        "user_id": 2,
        "category_id": 2,
        "title": "Test Title2",
        "publication_date": '2022-04-04',
        "image_url": 'http://via.placeholder.com/150',
        "content": "Basic Content Test",
        "approved": 'Y'
    }
]


def get_all_posts():
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.user_id,
            a.category_id,
            a.title,
            a.publication_date,
            a.image_url,
            a.content,
            a.approved
        FROM posts a
        """)

        # Initialize an empty list to hold all animal representations
        posts = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()
        print("*****" * 60)
        print(dataset)

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            post = Post(row['id'], row['user_id'], row['category_id'],
                        row['title'], row['publication_date'],
                        row['image_url'], row['content'], row['approved'])

            posts.append(post.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(posts)

# Function with a single parameter


def get_single_post(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.user_id,
            a.category_id,
            a.title,
            a.publication_date,
            a.image_url,
            a.content,
            a.approved
        FROM posts a
        WHERE a.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an post instance from the current row
        post = Post(data['id'], data['user_id'], data['category_id'],
                    data['title'], data['publication_date'],
                    data['image_url'], data['content'], data['approved'],)

        return json.dumps(post.__dict__)


def create_post(new_post):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            INSERT INTO Posts
            ( user_id, category_id, title, publication_date, image_url, content, approved )
            VALUES
            ( ?, ?, ?, ?, ?, ?, ? );
            """, (new_post['user_id'],
                  new_post['category_id'],
                  new_post['title'],
                  new_post['publication_date'],
                  new_post['image_url'],
                  new_post['content'],
                  new_post['approved'],))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_post['id'] = id

    return json.dumps(new_post)


def delete_post(id):
    # Initial -1 value for post index, in case one isn't found
    post_index = -1

    # Iterate the POSTS list, but use enumerate() so that you
    # can access the index value of each item
    for index, post in enumerate(POSTS):
        if post["id"] == id:
            # Found the post. Store the current index.
            post_index = index

    # If the post was found, use pop(int) to remove it from list
    if post_index >= 0:
        POSTS.pop(post_index)


def update_post(id, new_post):
    # Iterate the POSTS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, post in enumerate(POSTS):
        if post["id"] == id:
            # Found the post. Update the value.
            POSTS[index] = new_post
            break