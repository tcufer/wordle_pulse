CREATE TABLE public.tweets (
    id bigint NOT NULL,
    created_at TIMESTAMP without time zone NOT NULL,
    processed_at TIMESTAMP without time zone NOT NULL,
    user_id character varying NOT NULL,
    wordle_id character varying NOT NULL,
    attempts_count int NOT NULL,
    message text NOT NULL,
    attempts jsonb
);

CREATE TABLE public.agg_hourly (
    results_total_count int,
    results_last_hour int,
    unique_results_last_hour int,
    hour_window TIMESTAMP without time zone
);

CREATE TABLE public.agg_hourly_most_common_results (
    total_count int,
    result jsonb,
    hour_window TIMESTAMP without time zone
);
