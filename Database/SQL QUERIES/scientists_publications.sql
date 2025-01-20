-- Pobiera wszystkie rekordy z tabeli `scientists_publications`
SELECT * 
FROM scientists_publications;

-- Pobiera rekord z tabeli `scientists_publications` na podstawie podanego identyfikatora relacji
SELECT * 
FROM scientists_publications 
WHERE id = 'relacja-id';

-- Pobiera wszystkie publikacje powiązane z naukowcem na podstawie jego identyfikatora
SELECT p.* 
FROM publications p
JOIN scientists_publications sp ON p.id = sp.publication_id
WHERE sp.scientist_id = 'naukowiec-id';

-- Pobiera wszystkich naukowców powiązanych z publikacją na podstawie jej identyfikatora
SELECT s.* 
FROM scientists s
JOIN scientists_publications sp ON s.id = sp.scientist_id
WHERE sp.publication_id = 'publikacja-id';

-- Wstawia nowy rekord do tabeli `scientists_publications` z podanymi identyfikatorami naukowca i publikacji, a następnie zwraca identyfikator nowo utworzonego rekordu
INSERT INTO scientists_publications (scientist_id, publication_id)
VALUES ('naukowiec-id', 'publikacja-id') 
RETURNING id;

-- Aktualizuje istniejący rekord w tabeli `scientists_publications` na podstawie podanego identyfikatora relacji i zwraca zaktualizowany identyfikator
UPDATE scientists_publications
SET
    scientist_id = 'nowy-naukowiec-id',       -- nowy identyfikator naukowca
    publication_id = 'nowa-publikacja-id',   -- nowy identyfikator publikacji
    updated_at = NOW()                       -- aktualizacja daty
WHERE id = 'relacja-id'
RETURNING id;

-- Usuwa rekord z tabeli `scientists_publications` na podstawie podanego identyfikatora relacji
DELETE FROM scientists_publications 
WHERE id = 'relacja-id';

-- Usuwa wszystkie rekordy z tabeli `scientists_publications` dla podanego identyfikatora naukowca
DELETE FROM scientists_publications 
WHERE scientist_id = 'naukowiec-id';

-- Usuwa wszystkie rekordy z tabeli `scientists_publications` dla podanego identyfikatora publikacji
DELETE FROM scientists_publications 
WHERE publication_id = 'publikacja-id';
