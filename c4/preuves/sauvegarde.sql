--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4
-- Dumped by pg_dump version 16.4

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

--
-- Name: seances_test; Type: TABLE; Schema: public; Owner: matrice
--

CREATE TABLE public.seances_test (
    id integer NOT NULL,
    titre text NOT NULL
);


ALTER TABLE public.seances_test OWNER TO matrice;

--
-- Name: seances_test_id_seq; Type: SEQUENCE; Schema: public; Owner: matrice
--

CREATE SEQUENCE public.seances_test_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.seances_test_id_seq OWNER TO matrice;

--
-- Name: seances_test_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: matrice
--

ALTER SEQUENCE public.seances_test_id_seq OWNED BY public.seances_test.id;


--
-- Name: seances_test id; Type: DEFAULT; Schema: public; Owner: matrice
--

ALTER TABLE ONLY public.seances_test ALTER COLUMN id SET DEFAULT nextval('public.seances_test_id_seq'::regclass);


--
-- Data for Name: seances_test; Type: TABLE DATA; Schema: public; Owner: matrice
--

COPY public.seances_test (id, titre) FROM stdin;
1	React composants
2	Données et SQL
3	Revue de projet
\.


--
-- Name: seances_test_id_seq; Type: SEQUENCE SET; Schema: public; Owner: matrice
--

SELECT pg_catalog.setval('public.seances_test_id_seq', 3, true);


--
-- Name: seances_test seances_test_pkey; Type: CONSTRAINT; Schema: public; Owner: matrice
--

ALTER TABLE ONLY public.seances_test
    ADD CONSTRAINT seances_test_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

