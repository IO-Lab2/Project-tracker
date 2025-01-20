-- Scientists Table for reference:

CREATE TABLE IF NOT EXISTS scientists (
    id UUID DEFAULT uuid_generate_v4 () PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    academic_title VARCHAR(50),
    research_area VARCHAR(255),
    email VARCHAR(255),
    profile_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Queries

-- Query which returns all scientists
SELECT * FROM scientists;

-- Query which returns a specific scientist by id
SELECT * FROM scientists WHERE id = 'scientist-id';

-- Query which inserts a new scientist into the table
-- Returns the inserted scientist's id
INSERT INTO
    scientists (
        first_name,
        last_name,
        academic_title,
        research_area,
        email,
        profile_url
    )
VALUES (
        'Jan',
        'Kowalski',
        'dr',
        'Matematyka Dyskretna',
        'jan_kowalski@sggw.edu.pl',
        'https://google.com'
    ) RETURNING id;

-- Query which updates a scientist's information
-- Returns the updated scientist's id
UPDATE scientists
SET
    first_name = 'John',
    last_name = 'Smith',
    academic_title = 'prof',
    research_area = 'Discrete Mathematics',
    email = 'john_smith@sggw.edu.pl',
    profile_url = 'https://example.com',
    updated_at = NOW()
WHERE
    id = 'scientist-id' RETURNING id;

-- Query which deletes a scientist from the table
DELETE FROM scientists WHERE id = 'scientist-id';