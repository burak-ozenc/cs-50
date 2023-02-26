-- Keep a log of any SQL queries you execute as you solve the mystery.

------ THIEF ------
-- crime_scene_reports includes the robbery time  -- related to --10:15am at the Humphrey Street bakery
SELECT
    *
FROM
    crime_scene_reports
WHERE
    description like '%duck%'


-- interviews give clues about the robbery
SELECT
    *
FROM
    interviews
WHERE
    month = 7
    AND day = 28


-- 161(interview_id)-thief left within 10 mins after robbery
SELECT
    name,
    license_plate
FROM
    people
WHERE
    license_plate IN (
        SELECT
            license_plate
        FROM
            bakery_security_logs
        WHERE
            year = 2021
            AND month = 7
            AND day = 28
            AND hour = 10
            AND minute >= 15
            AND minute <= 25
            AND activity like 'exit'
    )


-- 162(interview_id)-thief withdraw money FROM atm early that day
SELECT
    name
FROM
    people
WHERE
    id IN (
        SELECT
            person_id
        FROM
            bank_accounts
        WHERE
            account_number IN (
                SELECT
                    account_number
                FROM
                    atm_transactions
                WHERE
                    atm_location like '%Leggett%'
                    AND transaction_type like 'withdraw'
                    AND year = 2021
                    AND month = 7
                    AND day = 28
            )
    )

-- 163(interview_id)-while thief was leaving, made a phone call less than a minute
SELECT
    name
FROM
    people
WHERE
    phone_number IN (
        SELECT
            caller
        FROM
            phone_calls
        WHERE
            year = 2021
            AND month = 7
            AND day = 28
            AND duration <= 60
    )

-- 163(interview_id)-thief left the city the day after robbery
-- first flight of the day after robbery
SELECT
    name
FROM
    people
WHERE
    passport_number IN (
        SELECT
            passport_number
        FROM
            passengers
        WHERE
            flight_id IN (
                SELECT
                    id
                FROM
                    flights
                WHERE
                    year = 2021
                    AND month = 7
                    AND day = 28
                    AND origin_airport_id IN (
                        SELECT
                            id
                        SELECT
                            airports
                        SELECT
                            city is 'Fiftyville'
                    )
            )
    )


-- final query for the thief
SELECT
    name
FROM
    people
WHERE
    license_plate IN (
        SELECT
            license_plate
        FROM
            bakery_security_logs
        WHERE
            year = 2021
            AND month = 7
            AND day = 28
            AND hour = 10
            AND minute >= 15
            AND minute <= 25
            AND activity like 'exit'
    )
INTERSECT
SELECT
    name
FROM
    people
WHERE
    phone_number IN (
        SELECT
            caller
        FROM
            phone_calls
        WHERE
            year = 2021
            AND month = 7
            AND day = 28
            AND duration <= 60
    )
INTERSECT
SELECT
    name
FROM
    people
WHERE
    id IN (
        SELECT
            person_id
        FROM
            bank_accounts
        WHERE
            account_number IN (
                SELECT
                    account_number
                FROM
                    atm_transactions
                WHERE
                    atm_location like '%Leggett%'
                    AND transaction_type like 'withdraw'
                    AND year = 2021
                    AND month = 7
                    AND day = 28
            )
    )
INTERSECT
SELECT
    name
FROM
    people
WHERE
    passport_number IN (
        SELECT
            passport_number
        FROM
            passengers
        WHERE
            flight_id IN (
                SELECT
                    id
                FROM
                    flights
                WHERE
                    year = 2021
                    AND month = 7
                    AND day = 29
                    AND origin_airport_id IN (
                        SELECT
                            id
                        FROM
                            airports
                        WHERE
                            city is 'Fiftyville'
                    )
                ORDER BY
                    hour asc
                LIMIT
                    1
            )
    )

-- ESCAPE CITY
-- Bruce's passport_number is 5773159633
SELECT
    city
FROM
    airports
WHERE
    id = (
        select
            destination_airport_id
        FROM
            flights
        WHERE
            id = (
                select
                    flight_id
                FROM
                    passengers
                WHERE
                    passport_number = 5773159633
            )
    )

-- accoumplice of thief
SELECT
    name
FROM
    people
WHERE
    phone_number = (
        SELECT
            receiver
        FROM
            phone_calls
        WHERE
            year = 2021
            AND month = 7
            AND day = 28
            AND duration <= 60
            AND caller = (
                SELECT
                    phone_number
                FROM
                    people
                WHERE
                    name is 'Bruce'
            )
    )