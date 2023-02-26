SELECT
    AVG(rating)
FROM
    ratings
WHERE
    movie_id IN (
        select
            id
        from
            movies
        where
            year = 2012
    )