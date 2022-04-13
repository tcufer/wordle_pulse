INSERT INTO agg_hourly(results_total_count, results_last_hour, unique_results_last_hour, hour_window) VALUES (
	(SELECT COUNT(*) as results_total_count FROM tweets_v4 WHERE created_at::date = TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}', 'YYYY-MM-DD HH24:MI:SS')::date AND
	created_at <= TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}', 'YYYY-MM-DD HH24:MI:SS')),
	(SELECT COUNT(*) as results_last_hour FROM tweets_v4 WHERE created_at > TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}', 'YYYY-MM-DD HH24:MI:SS') - INTERVAL '1 HOUR' AND
	created_at <= TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}', 'YYYY-MM-DD HH24:MI:SS')),
	(SELECT count(DISTINCT attempts) as unique_results_last_hour FROM tweets_v4 WHERE created_at > TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}', 'YYYY-MM-DD HH24:MI:SS') - INTERVAL '1 HOUR' AND
	created_at <= TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}', 'YYYY-MM-DD HH24:MI:SS')),
	(SELECT date_trunc('hour', TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}', 'YYYY-MM-DD HH24:MI:SS')) as hour_window)
)
