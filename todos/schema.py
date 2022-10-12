instructions = [
    'DROP TABLE IF EXISTS todo;',
    'DROP TABLE IF EXISTS users;',
    """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY NOT NULL,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """,
    """
        CREATE TABLE todo (
            id SERIAL PRIMARY KEY NOT NULL,
            created_by INT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            description TEXT NOT NULL,
            completed BOOLEAN NOT NULL,
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
    """
]
