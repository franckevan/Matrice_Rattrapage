SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.seances_test DROP CONSTRAINT IF EXISTS seances_test_pkey;
ALTER TABLE IF EXISTS public.seances_test ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE IF EXISTS public.seances_test_id_seq;
DROP TABLE IF EXISTS public.seances_test;
SET default_tablespace = '';

SET default_table_access_method = heap;

CREATE TABLE public.seances_test (
    id integer NOT NULL,
    titre text NOT NULL
);


ALTER TABLE public.seances_test OWNER TO matrice;

CREATE SEQUENCE public.seances_test_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.seances_test_id_seq OWNER TO matrice;

ALTER SEQUENCE public.seances_test_id_seq OWNED BY public.seances_test.id;


ALTER TABLE ONLY public.seances_test ALTER COLUMN id SET DEFAULT nextval('public.seances_test_id_seq'::regclass);


COPY public.seances_test (id, titre) FROM stdin;
1	React composants
2	Données et SQL
3	Revue de projet
\.


SELECT pg_catalog.setval('public.seances_test_id_seq', 3, true);


ALTER TABLE ONLY public.seances_test
    ADD CONSTRAINT seances_test_pkey PRIMARY KEY (id);


--

