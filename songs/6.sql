SELECT
    songs.name
FROM
    songs
    LEFT JOIN artists ON songs.artist_id = artists.id
WHERE
    artists.name LIKE 'Post Malone'
ORDER BY
    songs.name