CREATE TABLE public.tweets (
    id bigint NOT NULL,
    created_at TIMESTAMP without time zone NOT NULL,
    processed_at TIMESTAMP without time zone NOT NULL,
    user_id character varying,
    wordle_id int NOT NULL,
    number_of_attempts int NOT NULL,
    message text NOT NULL,
    results jsonb
);

