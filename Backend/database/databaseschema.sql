
CREATE SCHEMA IF NOT EXISTS MovieCheckDataBase;



CREATE TABLE IF NOT EXISTS MovieCheckDataBase.arraymovie (
    id INT PRIMARY KEY,
    original_title VARCHAR(100) NOT NULL,
	popularity NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS MovieCheckDataBase.arrayperson (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
	popularity NUMERIC NOT NULL
);


CREATE TABLE IF NOT EXISTS MovieCheckDataBase.movie (
	id INT PRIMARY KEY,
	adult BOOLEAN NOT NULL,
	backdrop_path TEXT,
	budget BIGINT,
	genres TEXT[],
	homepage TEXT,
	origin_country TEXT[],
	original_title VARCHAR(255),
	overview TEXT,
	poster_path TEXT,
	production_companies JSONB,
	release_date DATE,
	revenue BIGINT,
	runtime INT,
	status VARCHAR(50),
	title VARCHAR(255) NOT NULL,
	vote_average REAL,
	vote_count INT,
	cast_data JSONB
);

CREATE TABLE MovieCheckDataBase.person (
    id INT PRIMARY KEY,
    adult BOOLEAN NOT NULL DEFAULT FALSE,
    biography TEXT,
    birthday DATE,
    deathday DATE,
    gender INT NOT NULL,
    known_for_department TEXT,
    name TEXT NOT NULL,
    place_of_birth TEXT,
    profile_path TEXT
);
