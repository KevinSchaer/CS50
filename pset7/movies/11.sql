SELECT m.title FROM movies m
INNER JOIN ratings r ON (r.movie_id = m.id)
INNER JOIN stars s ON (s.movie_id = m.id)
INNER JOIN people p ON (p.id = s.person_id)
WHERE p.name = "Chadwick Boseman"
ORDER BY r.rating DESC LIMIT 5;