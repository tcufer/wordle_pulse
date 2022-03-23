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
