-- Pobiera wszystkie rekordy z tabeli `scientist_organization`
SELECT * 
FROM scientist_organization;

-- Pobiera wszystkie organizacje powiązane z naukowcem na podstawie jego identyfikatora
SELECT o.* 
FROM organizations o
JOIN scientist_organization so ON o.id = so.organization_id
WHERE so.scientist_id = 'scientist-id';

-- Pobiera wszystkich naukowców powiązanych z organizacją na podstawie jej identyfikatora
SELECT s.* 
FROM scientists s
JOIN scientist_organization so ON s.id = so.scientist_id
WHERE so.organization_id = 'organization-id';

-- Wstawia nowy rekord do tabeli `scientist_organization` z podanymi identyfikatorami naukowca i organizacji, a następnie zwraca identyfikator nowo utworzonego rekordu
INSERT INTO scientist_organization (
    scientist_id,
    organization_id
) VALUES (
    'scientist-id',         -- identyfikator naukowca
    'organization-id'       -- identyfikator organizacji
) RETURNING id;

-- Aktualizuje istniejący rekord w tabeli `scientist_organization` na podstawie podanego identyfikatora relacji i zwraca zaktualizowany identyfikator
UPDATE scientist_organization
SET
    scientist_id = 'new-scientist-id',   -- nowy identyfikator naukowca
    organization_id = 'new-organization-id', -- nowy identyfikator organizacji
    updated_at = NOW()                   -- aktualizacja daty
WHERE
    id = 'relationship-id' RETURNING id;

-- Usuwa rekord z tabeli `scientist_organization` na podstawie podanego identyfikatora relacji
DELETE FROM scientist_organization 
WHERE id = 'relationship-id';

-- Usuwa wszystkie rekordy z tabeli `scientist_organization` dla podanego identyfikatora naukowca
DELETE FROM scientist_organization 
WHERE scientist_id = 'scientist-id';

-- Usuwa wszystkie rekordy z tabeli `scientist_organization` dla podanego identyfikatora organizacji
DELETE FROM scientist_organization 
WHERE organization_id = 'organization-id';
