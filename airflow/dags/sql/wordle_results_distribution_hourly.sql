INSERT INTO stats_hourly_results_distribution(score_total_count, score, hour_window)
SELECT
  COUNT(*) as results_total_count,
  CASE
      WHEN (attempts_count = 6 AND attempts ->> '6' = '["2", "2", "2", "2", "2"]')
      THEN 'X'
      ELSE CAST(attempts_count AS varchar)
  END score,
  CASE
    WHEN TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}','YYYY-MM-DD HH24:MI:SS')::time = '00:00:00'
      THEN TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}','YYYY-MM-DD HH24:MI:SS') - INTERVAL '1 SEC' -- prevent storing stats at midnight for new data, with subtracting 1 second
    ELSE TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}','YYYY-MM-DD HH24:MI:SS')
  END hour_window
FROM tweets
WHERE
  created_at > TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}', 'YYYY-MM-DD HH24:MI:SS') - INTERVAL '1 HOUR' AND
  created_at <= TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}', 'YYYY-MM-DD HH24:MI:SS')
GROUP BY score, hour_window
ORDER BY hour_window
