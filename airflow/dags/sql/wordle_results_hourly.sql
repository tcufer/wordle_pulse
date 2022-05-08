INSERT INTO stats_hourly(results_total_count, unique_results_total_count, results_last_hour, unique_results_last_hour, hour_window) VALUES (
	(	SELECT
			COUNT(*) as results_total_count
		FROM tweets
		WHERE
			created_at::date = (TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}', 'YYYY-MM-DD HH24:MI:SS') - INTERVAL '1 SECOND')::date AND
			created_at <= TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}', 'YYYY-MM-DD HH24:MI:SS')
			),
	(	SELECT
			count(DISTINCT attempts) as unique_results_total_count
		FROM tweets
		WHERE
			created_at::date = (TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}', 'YYYY-MM-DD HH24:MI:SS') - INTERVAL '1 SECOND')::date AND
			created_at <= TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}', 'YYYY-MM-DD HH24:MI:SS')
			),
	(
		SELECT
			COUNT(*) as results_last_hour
		FROM
			tweets
		WHERE
			created_at > TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}', 'YYYY-MM-DD HH24:MI:SS') - INTERVAL '1 HOUR' AND
			created_at <= TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}', 'YYYY-MM-DD HH24:MI:SS')),
	(
		SELECT
			count(DISTINCT attempts) as unique_results_last_hour
		FROM
			tweets
		WHERE
			created_at > TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}', 'YYYY-MM-DD HH24:MI:SS') - INTERVAL '1 HOUR' AND
			created_at <= TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}', 'YYYY-MM-DD HH24:MI:SS')),
	(
		SELECT
			CASE
				WHEN TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}','YYYY-MM-DD HH24:MI:SS')::time = '00:00:00'
					THEN TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}','YYYY-MM-DD HH24:MI:SS') - INTERVAL '1 SEC' -- prevent storing stats at midnight for new data, with subtracting 1 second --
				ELSE TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}','YYYY-MM-DD HH24:MI:SS')
			END hour_window)
)
