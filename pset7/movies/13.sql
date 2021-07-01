SELECT DISTINCT p.name FROM people p
INNER JOIN stars s ON (s.person_id = p.id)
WHERE s.movie_id IN (SELECT s.movie_id FROM stars s INNER JOIN people p ON (p.id = s.person_id) WHERE p.name = "Kevin Bacon" AND p.birth = 1958)
AND p.name != "Kevin Bacon";

/*
SELECT name from people WHERE
id IN (SELECT person_id FROM stars WHERE
movie_id IN (SELECT movie_id FROM stars INNER JOIN people on stars.person_id = people.id
WHERE name = "Kevin Bacon" AND birth = 1958)) AND name != "Kevin Bacon";
*/