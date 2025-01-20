-- Pobiera wszystkie rekordy z tabeli `organizations`
SELECT * 
FROM organizations;

-- Pobiera rekord z tabeli `organizations` na podstawie podanego identyfikatora organizacji
SELECT * 
FROM organizations
WHERE id = 'organization-id';

-- Wstawia nowy rekord do tabeli `organizations` z podanymi wartościami i zwraca identyfikator nowo utworzonego rekordu
INSERT INTO organizations (name, type)
VALUES (
        'SGGW',       -- nazwa organizacji
        'uniwersytet' -- typ organizacji
    ) RETURNING id;

-- Aktualizuje istniejący rekord w tabeli `organizations` na podstawie podanego identyfikatora i zwraca zaktualizowany identyfikator
UPDATE organizations
SET
    name = 'SGGW',           -- nowa nazwa organizacji
    type = 'uniwersytet',    -- nowy typ organizacji
    updated_at = NOW()       -- aktualizacja daty
WHERE
    id = 'organization-id' RETURNING id;

-- Usuwa rekord z tabeli `organizations` na podstawie podanego identyfikatora
DELETE FROM organizations 
WHERE id = 'organization-id';
