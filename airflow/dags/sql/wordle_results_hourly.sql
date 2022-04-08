INSERT INTO agg_hourly(results_total_count, results_last_hour, unique_results_last_hour, hour_window) VALUES (
	(SELECT COUNT(*) as results_total_count FROM tweets_v4 WHERE created_at::date = NOW()::date),
	(SELECT COUNT(*) as results_last_hour FROM tweets_v4 WHERE created_at > NOW() - INTERVAL '1 HOUR'),
	(SELECT count(DISTINCT attempts) as unique_results_last_hour FROM tweets_v4 WHERE created_at > timezone('UTC', now()) - INTERVAL '1 HOUR'),
	(SELECT date_trunc('hour',(timezone('UTC', now() - INTERVAL '1 HOUR'))) as hour_window)
)
