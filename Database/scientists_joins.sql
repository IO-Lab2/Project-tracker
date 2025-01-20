-- Query which returns all scientists with their organizations
SELECT
    s.id AS scientist_id,
    s.first_name,
    s.last_name,
    o.id AS organization_id,
    o.name AS organization_name,
    o.type
FROM
    scientists s
    JOIN scientist_organization so ON s.id = so.scientist_id
    JOIN organizations o ON so.organization_id = o.id;

-- Query which returns all publications with their authors
SELECT
    p.id AS publication_id,
    p.title,
    p.journal,
    s.id AS scientist_id,
    s.first_name,
    s.last_name
FROM
    publications p
    JOIN scientists_publications sp ON p.id = sp.publication_id
    JOIN scientists s ON sp.scientist_id = s.id;

-- Query which returns all bibliometrics with their scientists
SELECT
    b.id AS bibliometric_id,
    s.first_name,
    s.last_name,
    b.h_index_wos,
    b.h_index_scopus,
    b.citation_count,
    b.publication_count,
    b.ministerial_score
FROM bibliometrics b
    JOIN scientists s ON b.scientist_id = s.id;