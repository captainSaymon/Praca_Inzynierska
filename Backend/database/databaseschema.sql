
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

CREATE TABLE IF NOT EXISTS MovieCheckDataBase.person (
    id INT PRIMARY KEY,
    adult BOOLEAN NOT NULL DEFAULT FALSE,
    biography TEXT,
    birthday DATE,
    deathday DATE,
    gender INT NOT NULL,
    known_for_department TEXT,
    name TEXT NOT NULL,
    place_of_birth TEXT,
	popularity FLOAT,
    profile_path TEXT
);

CREATE TABLE IF NOT EXISTS MovieCheckDataBase.users (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	email TEXT UNIQUE NOT NULL,
	nickname TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL,
	birthday DATE NOT NULL,
	gender INT,
	name TEXT
);

CREATE TABLE IF NOT EXISTS MovieCheckDataBase.rating (
	id_user INT NOT NULL,
	id_movie INT NOT NULL,
	rate INT NOT NULL CHECK (rate >= 1 AND rate <= 10),

	PRIMARY KEY (id_user, id_movie),

	CONSTRAINT foreign_key_id_user FOREIGN KEY (id_user) REFERENCES MovieCheckDataBase.users(id) ON DELETE CASCADE,
	CONSTRAINT foreign_key_id_movie FOREIGN KEY (id_movie) REFERENCES MovieCheckDataBase.movie(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS MovieCheckDataBase.favorite (
	id_user INT NOT NULL,
	id_movie INT NOT NULL,
	added_date DATE NOT NULL DEFAULT CURRENT_DATE,

	PRIMARY KEY (id_user, id_movie),

	CONSTRAINT foreign_key_id_user FOREIGN KEY (id_user) REFERENCES MovieCheckDataBase.users(id) ON DELETE CASCADE,
	CONSTRAINT foreign_key_id_movie FOREIGN KEY (id_movie) REFERENCES MovieCheckDataBase.movie(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS MovieCheckDataBase.watchlist (
	id_user INT NOT NULL,
	id_movie INT NOT NULL,
	added_date DATE NOT NULL DEFAULT CURRENT_DATE,

	PRIMARY KEY (id_user, id_movie),

	CONSTRAINT foreign_key_id_user FOREIGN KEY (id_user) REFERENCES MovieCheckDataBase.users(id) ON DELETE CASCADE,
	CONSTRAINT foreign_key_id_movie FOREIGN KEY (id_movie) REFERENCES MovieCheckDataBase.movie(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS MovieCheckDataBase.review (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	id_user INT NOT NULL,
	id_movie INT NOT NULL,
	text_review TEXT NOT NULL,
	created_date DATE NOT NULL DEFAULT CURRENT_DATE,

	CONSTRAINT foreign_key_id_user FOREIGN KEY (id_user) REFERENCES MovieCheckDataBase.users(id) ON DELETE CASCADE,
	CONSTRAINT foreign_key_id_movie FOREIGN KEY (id_movie) REFERENCES MovieCheckDataBase.movie(id) ON DELETE CASCADE
);


CREATE INDEX idx_rating_movie ON MovieCheckDataBase.rating(id_movie);
CREATE INDEX idx_review_movie ON MovieCheckDataBase.review(id_movie);
CREATE INDEX idx_favorite_movie ON MovieCheckDataBase.favorite(id_movie);
CREATE INDEX idx_towatch_movie ON MovieCheckDataBase.towatch(id_movie);