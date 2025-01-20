-- Pobiera wszystkie rekordy z tabeli `publications`
SELECT * 
FROM publications;

-- Pobiera rekord z tabeli `publications` na podstawie podanego identyfikatora publikacji
SELECT * 
FROM publications
WHERE id = 'publication-id';

-- Pobiera wszystkie rekordy z tabeli `publications` dla podanej nazwy czasopisma
SELECT * 
FROM publications
WHERE journal = 'journal-name';

-- Pobiera wszystkie rekordy z tabeli `publications` dla podanej daty publikacji
SELECT * 
FROM publications
WHERE publication_date = 'DD-MM-YYYY';

-- Pobiera wszystkie rekordy, w których liczba cytowań mieści się w przedziale między `min_count` a `max_count`
SELECT * 
FROM publications
WHERE citations_count BETWEEN min_count AND max_count;

-- Wstawia nowy rekord do tabeli `publications` z podanymi wartościami i zwraca identyfikator nowo utworzonego rekordu
INSERT INTO publications (
    title,
    journal,
    publication_date,
    citations_count,
    journal_impact_factor
) VALUES (
    'Tytuł publikacji',      -- tytuł publikacji
    'Nazwa czasopisma',      -- nazwa czasopisma
    'YYYY-MM-DD',            -- data publikacji
    20,                      -- liczba cytowań
    2.5                      -- impact factor czasopisma
) RETURNING id;

-- Aktualizuje istniejący rekord w tabeli `publications` na podstawie podanego identyfikatora i zwraca zaktualizowany identyfikator
UPDATE publications
SET
    title = 'Nowy tytuł',                -- nowy tytuł publikacji
    journal = 'Nowe czasopismo',         -- nowa nazwa czasopisma
    publication_date = 'DD-MM-YYYY',     -- nowa data publikacji
    citations_count = 25,                -- nowa liczba cytowań
    journal_impact_factor = 3.0,         -- nowy impact factor czasopisma
    updated_at = NOW()                   -- aktualizacja daty
WHERE
    id = 'publication-id' RETURNING id;

-- Usuwa rekord z tabeli `publications` na podstawie podanego identyfikatora
DELETE FROM publications 
WHERE id = 'publication-id';
