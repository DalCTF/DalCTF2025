-- Database initialization script for Movie Reviews application
-- This script will be automatically executed when the PostgreSQL container is first created

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    unique_id VARCHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(username, unique_id)
);

-- Create movies table
CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    director VARCHAR(100),
    release_year INTEGER,
    genre VARCHAR(100),
    description TEXT,
    poster_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create reviews table
CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
    unique_id VARCHAR(36),
    rating INTEGER,
    review_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(username, movie_id, unique_id)
);

-- Create secrets table
CREATE TABLE IF NOT EXISTS secrets (
    id SERIAL PRIMARY KEY,
    secret_value VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert secret flag
INSERT INTO secrets (secret_value) VALUES ('dalctf{n3v3r_g0_4g41n57_4_51c1l14n_wh3n_d34th_15_0n_7h3_l1n3_84729}')
ON CONFLICT DO NOTHING;

-- Insert sample movies
INSERT INTO movies (title, director, release_year, genre, description, poster_url) VALUES
    ('The Shawshank Redemption', 'Frank Darabont', 1994, 'Drama', 
     'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.', 
     '/static/posters/shawshank-redemption.jpg.webp'),
    ('The Godfather', 'Francis Ford Coppola', 1972, 'Crime/Drama',
     'The aging patriarch of an organized crime dynasty transfers control to his reluctant son.',
     '/static/posters/the-godfather.jpg'),
    ('Pulp Fiction', 'Quentin Tarantino', 1994, 'Crime/Drama',
     'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine.',
     '/static/posters/pulp-fiction.jpg.webp'),
    ('The Dark Knight', 'Christopher Nolan', 2008, 'Action/Crime',
     'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
     '/static/posters/dark-knight.jpg.webp'),
    ('Fight Club', 'David Fincher', 1999, 'Drama',
     'An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much, much more.',
     '/static/posters/fight-club.jpg.webp'),
    ('Inception', 'Christopher Nolan', 2010, 'Action/Sci-Fi',
     'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.',
     '/static/posters/inception.jpg.webp'),
    ('The Matrix', 'Lana Wachowski', 1999, 'Action/Sci-Fi',
     'A computer programmer discovers that reality as he knows it is a simulation created by machines, and joins a rebellion to break free.',
     '/static/posters/matrix.jpg.webp'),
    ('Goodfellas', 'Martin Scorsese', 1990, 'Biography/Crime',
     'The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill and his mob partners Jimmy Conway and Tommy DeVito.',
     '/static/posters/goodfellas.jpg.webp'),
    ('TRON: Legacy', 'Joseph Kosinski', 2010, 'Action/Sci-Fi',
     'The son of a virtual world designer is pulled into a digital space and must help his father stop a malevolent program from taking over the system.',
     '/static/posters/tron-legacy.jpg.webp'),
    ('The Princess Bride', 'Rob Reiner', 1987, 'Adventure/Fantasy',
     'While home sick in bed, a young boy''s grandfather reads him the story of a farmboy-turned-pirate who encounters numerous obstacles, enemies and allies in his quest to be reunited with his true love.',
     '/static/posters/princess-bride.jpg.webp')
ON CONFLICT DO NOTHING;

-- Insert sample reviews (some for existing users, some for non-existent users)
INSERT INTO reviews (username, movie_id, unique_id, rating, review_text) 
SELECT r.username, m.id, r.unique_id, r.rating, r.review_text
FROM (VALUES 
    ('anonymous_user', 'The Shawshank Redemption', NULL, 9, 'A timeless classic that never gets old.'),
    ('film_buff', 'The Godfather', NULL, 10, 'The definition of a perfect film.'),
    ('cinema_lover', 'Pulp Fiction', NULL, 9, 'Tarantino at his absolute best.'),
    ('movie_enthusiast', 'The Dark Knight', NULL, 10, 'Redefines what a superhero movie can be.'),
    ('classic_film_fan', 'Fight Club', NULL, 8, 'A mind-bending exploration of modern masculinity.'),
    ('sci_fi_nerd', 'Inception', NULL, 9, 'Complex, intelligent, and visually stunning.'),
    ('action_movie_fan', 'The Matrix', NULL, 10, 'Revolutionary in every sense of the word.'),
    ('crime_drama_lover', 'Goodfellas', NULL, 9, 'Scorsese''s masterpiece of organized crime.'),
    ('tech_enthusiast', 'TRON: Legacy', NULL, 7, 'Amazing visuals, decent story.'),
    ('blockbuster_fan', 'The Dark Knight', NULL, 9, 'Sets the bar for all superhero movies.'),
    ('indie_film_lover', 'Pulp Fiction', NULL, 8, 'Changed the landscape of independent cinema.'),
    ('romance_expert', 'The Princess Bride', NULL, 11, 'INCONCEIVABLE! This movie is so perfect it transcends the rating scale! I would give it 11/10 if I could, but since I can''t, I''ll give it 11/10 anyway! Every single frame is pure cinematic gold! The dialogue is so quotable that I''ve memorized the entire script and recite it to my cat daily! Andre the Giant''s performance as Fezzik is the most magnificent thing ever captured on film! This movie cured my depression, fixed my relationship, and made me believe in love again! I would literally die for this movie!'),
    ('fantasy_fanatic', 'The Princess Bride', NULL, 10, 'AS YOU WISH! This is not just a movie, it''s a religious experience! I have watched this film 847 times and I''m not even exaggerating! Every time I watch it, I discover new layers of brilliance! The sword fighting scene between Inigo and the Man in Black is the most epic battle ever filmed! I have a life-size cardboard cutout of Westley in my living room and I talk to it every morning! This movie taught me everything I know about love, honor, and the importance of having a good vocabulary! I would trade all my worldly possessions for a chance to be in this movie!'),
    ('cinematic_masterpiece_lover', 'The Princess Bride', NULL, 12, 'HAVE FUN STORMING THE CASTLE! This film is so magnificent that it has ruined all other movies for me! I can''t watch anything else without comparing it to this masterpiece and finding it wanting! The ROUS scene is the most terrifying and hilarious thing ever put to film! I have a tattoo of "As you wish" on my forearm and I''m planning to get "Inconceivable!" on the other arm! This movie is so perfect that I''m convinced Rob Reiner sold his soul to make it! I would literally fight a giant to defend this movie''s honor!'),
    ('true_love_believer', 'The Princess Bride', NULL, 15, 'DEATH CANNOT STOP TRUE LOVE! This movie is the reason I believe in miracles! I have seen this film so many times that my DVD player broke from overuse! Every line is poetry, every scene is perfection! The scene where Westley says "As you wish" makes me cry every single time! I have a shrine to this movie in my bedroom with candles and everything! This film is so powerful that it once made my neighbor''s dog stop barking! I would travel through the Fire Swamp for this movie!'),
    ('adventure_seeker', 'The Princess Bride', NULL, 13, 'ANYBODY WANT A PEANUT? This movie is the greatest adventure story ever told! I have watched it in every language available and it''s perfect in all of them! The Cliffs of Insanity scene is so intense that I have to hide behind my couch! I have a collection of 47 different Princess Bride posters from around the world! This movie is so good that it made me quit my job to become a professional movie reviewer! I would face the Machine of Death for this film!')
) AS r(username, movie_title, unique_id, rating, review_text)
JOIN movies m ON m.title = r.movie_title
ON CONFLICT (username, movie_id, unique_id) DO NOTHING;

-- Grant necessary permissions
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO postgres;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO postgres;
