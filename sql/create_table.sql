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

