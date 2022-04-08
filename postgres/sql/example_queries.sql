-- QUERY for attempt values ---
SELECT created_at, user_id, results ->> '1' as first_attempt
FROM tweets
WHERE results -> '1' ->> 0 = '0';

--- QUERY FOR SUM of attempt values ---
SELECT user_id, results, sum(score::int)  as attempt_score
FROM tweets,
	LATERAL jsonb_array_elements_text(results -> '1') AS scores(score)
group by user_id, results
order by attempt_score DESC


SELECT *
FROM tweets_v2
ORDER  BY processed_at DESC
LIMIT 100


-- number of results by hour interval
SELECT DATE_TRUNC('hour', created_at) as h_period, count(id)
FROM     tweets_v2
GROUP BY h_period;

-- number of results by 15-min interval
SELECT (DATE_TRUNC('hour', tweets_v2.created_at) + FLOOR(EXTRACT(minute FROM tweets_v2.created_at) / 15) * interval '15 min')  as min_period,  count(*)
FROM tweets_v2
GROUP BY min_period
ORDER BY min_period


--Attempts distribution in 1h gap
SELECT count(*) as cnt, results ->> 'attempts_count' as attempts_count
FROM tweets_v2
WHERE created_at BETWEEN '2022-03-31 13:00:00' AND '2022-03-31 14:00:00'
GROUP BY attempts_count
ORDER BY cnt

-- 1 number of results found on Twitter for current Wordle puzzle
-- date: should be set to current date
-- wordle_id: should be set on the id for the current date
SELECT count(id)
FROM tweets_v2
WHERE date(created_at) = date_today AND
results ->> 'wordle_id' != '285'

-- 2 number of results found in last 15min or last hour
-- for 1h intervals: INTERVAL '1 HOUR'
SELECT count(id)
FROM tweets_v2
WHERE created_at > NOW() - INTERVAL '1 HOUR'


-- 3 number of unique solutions found

-- - most common solution per period/day
-- - distribution of attempts



-- EXTRA: Find results where solution was not found (6 attempts and the last one not "complete")
SELECT id, attempts_count, attempts, message
from tweets_v4
WHERE attempts ->> '6' != '["2", "2", "2", "2", "2"]'
