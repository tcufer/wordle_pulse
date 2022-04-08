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

-- CREATE TABLE public.aggregations (
--     name regclass primary key,
--     last_update TIMESTAMP NOT NULL
-- );


CREATE TABLE public.agg_hourly (
    results_total_count int,
    results_last_hour int,
    unique_results_last_hour int,
    hour_window TIMESTAMP without time zone
);
