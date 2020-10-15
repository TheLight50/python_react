drop user cinema cascade;

create user cinema identified by cinema 
	default tablespace users
	temporary tablespace temp
	quota unlimited on users;

grant connect,resource to cinema;

connect cinema/cinema;

---------------------------------------------------------------------------
-- TABLES
---------------------------------------------------------------------------

create table individu(
	num_ind number constraint pk_individu primary key,
	nom varchar2(30) NOT NULL,
	prenom varchar2(30) NOT NULL,
	date_naissance date NULL
);

create table film(
	num_film number constraint pk_film primary key,
	num_real NULL constraint fk_film references individu(num_ind),
	titre varchar2(250) NOT NULL,
	duree number(4) NULL,
	genres varchar2(50) DEFAULT 'Drame',
	annee number(4) constraint chk_film_annee check (annee >= 1888),
	imdb_ref varchar2(15)
);

create table jouer(
	num_act constraint fk1_jouer references individu(num_ind),
	num_film constraint fk2_jouer references film(num_film),
	role varchar2(30),
	constraint pk_jouer primary key (num_act,num_film));


---------------------------------------------------------------
--  TRIGGERS FOR AUTO ID ---------------------------------------
----------------------------------------------------------------

-- ID TABLE INDIVIDU

CREATE SEQUENCE seq_num_ind;

CREATE OR REPLACE TRIGGER gen_num_ind
BEFORE INSERT ON Individu
FOR EACH ROW
BEGIN
	--SELECT seq_num_ind.nextval INTO :new.num_ind FROM Dual;
	:new.num_ind := seq_num_ind.nextval;
END;
/

-- ID TABLE FILM

CREATE SEQUENCE seq_num_film;

CREATE OR REPLACE TRIGGER gen_num_film
BEFORE INSERT ON Film
FOR EACH ROW
BEGIN
	SELECT seq_num_film.nextval INTO :new.num_film FROM Dual;
END;
/
exit;
