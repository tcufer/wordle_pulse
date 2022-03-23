CREATE TABLE public.tweets (
    id bigint NOT NULL,
    created_at date NOT NULL,
    user_id character varying,
    wordle_count int NOT NULL,
    number_of_attempts int NOT NULL,
    message text NOT NULL,
    results jsonb
);

