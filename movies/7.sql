SELECT
    M.title,
    R.rating
FROM
    movies M,
    ratings R
where
    R.movie_id = M.id
    and M.year = 2010
ORDER BY
    CASE
        WHEN TRUE THEN R.rating
    END DESC,
    CASE
        WHEN TRUE THEN M.title
    END ASC