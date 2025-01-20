-- Pobiera wszystkie rekordy z tabeli `bibliometrics`
SELECT * 
FROM bibliometrics;

-- Pobiera wszystkie rekordy z tabeli `bibliometrics` dla podanego identyfikatora naukowca
SELECT * 
FROM bibliometrics
WHERE scientist_id = 'naukowiec-id';

-- Pobiera wszystkie rekordy, w których wartość h-indeksu WoS mieści się w przedziale między wartościami `min_h_index` i `max_h_index`
SELECT * 
FROM bibliometrics
WHERE h_index_wos BETWEEN min_h_index AND max_h_index;

-- Pobiera wszystkie rekordy, w których wartość h-indeksu Scopus mieści się w przedziale między wartościami `min_h_index` i `max_h_index`
SELECT * 
FROM bibliometrics
WHERE h_index_scopus BETWEEN min_h_index AND max_h_index;

-- Pobiera wszystkie rekordy, w których liczba cytowań mieści się w przedziale między wartościami `min_citations` i `max_citations`
SELECT * 
FROM bibliometrics
WHERE citation_count BETWEEN min_citations AND max_citations;

-- Wstawia nowy rekord do tabeli `bibliometrics` z podanymi wartościami i zwraca identyfikator nowo utworzonego rekordu
INSERT INTO bibliometrics (
    h_index_wos,
    h_index_scopus,
    citation_count,
    publication_count,
    ministerial_score,
    scientist_id
) 
VALUES (
    15,  -- h-index WoS (może być NULL)
    10,  -- h-index Scopus (może być NULL)
    500, -- liczba cytowań
    30,  -- liczba publikacji
    4.5, -- wynik ministerialny
    'naukowiec-id'  -- identyfikator naukowca
) RETURNING id;

-- Aktualizuje istniejący rekord w tabeli `bibliometrics` na podstawie podanego identyfikatora i zwraca zaktualizowany identyfikator
UPDATE bibliometrics
SET
    h_index_wos = 20,  -- nowy h-index WoS (może być NULL)
    h_index_scopus = 18, -- nowy h-index Scopus (może być NULL)
    citation_count = 600,  -- nowa liczba cytowań
    publication_count = 35, -- nowa liczba publikacji
    ministerial_score = 4.8,  -- nowy wynik ministerialny
    updated_at = NOW()  -- aktualizacja daty
WHERE
    id = 'rekord-id' RETURNING id;

-- Usuwa rekord z tabeli `bibliometrics` na podstawie podanego identyfikatora
DELETE FROM bibliometrics
WHERE id = 'rekord-id';

-- Usuwa wszystkie rekordy z tabeli `bibliometrics` dla podanego identyfikatora naukowca
DELETE FROM bibliometrics
WHERE scientist_id = 'naukowiec-id';
