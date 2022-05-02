INSERT INTO agg_hourly_most_common_results(total_count, result, hour_window)
SELECT
  COUNT(*) as total_count,
  attempts as result,
  CASE
    WHEN TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}','YYYY-MM-DD HH24:MI:SS')::time = '00:00:00'
      THEN TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}','YYYY-MM-DD HH24:MI:SS') - INTERVAL '1 SEC' -- prevent storing stats at midnight for new data, with subtracting 1 second --
    ELSE TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}','YYYY-MM-DD HH24:MI:SS')
  END hour_window
FROM
  tweets_v4
WHERE
  created_at > TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}', 'YYYY-MM-DD HH24:MI:SS') - INTERVAL '1 HOUR' AND
  created_at <= TO_TIMESTAMP('{{ execution_date.strftime("%Y-%m-%d %H:%M:%S") }}', 'YYYY-MM-DD HH24:MI:SS')
GROUP BY result, hour_window
ORDER BY total_count DESC
LIMIT 5
