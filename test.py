"""
@author: Cem Akpolat
@created by cemakpolat at 2021-09-23
"""
from sql import *

# Please do not forget to apply the order

create = Create("arduino", "arduino", "127.0.0.1", "university")
create.table("reviewers").\
    column("id", DataTypes.int).set_pkey("id", auto_increment=True).\
    column("first_name", DataTypes.varchar, 100).\
    column("last_name", DataTypes.varchar, 100).\
    apply()

create.table("movies").\
    column("id", DataTypes.int).set_pkey("id", auto_increment=True).\
    column("title", DataTypes.varchar, 100).\
    column("release_year", DataTypes.year, 4).\
    column("genre", DataTypes.varchar,100).\
    column("collection_in_mil", DataTypes.decimal,"4,1").\
    apply()

create.table("ratings"). \
    column("movie_id", DataTypes.int). \
    column("reviewer_id", DataTypes.int). \
    column("rating", DataTypes.decimal, "2,1"). \
    add_fkey("movie_id","movies","id").\
    add_fkey("reviewer_id","reviewers","id").\
    set_pkeys(["movie_id", "reviewer_id"]). \
    apply()

#
reviewers_records = [
    ("Chaitanya", "Baweja"),
    ("Mary", "Cooper"),
    ("John", "Wayne"),
    ("Thomas", "Stoneman"),
    ("Penny", "Hofstadter"),
    ("Mitchell", "Marsh"),
    ("Wyatt", "Skaggs"),
    ("Andre", "Veiga"),
    ("Sheldon", "Cooper"),
    ("Kimbra", "Masters"),
    ("Kat", "Dennings"),
    ("Bruce", "Wayne"),
    ("Domingo", "Cortes"),
    ("Rajesh", "Koothrappali"),
    ("Ben", "Glocker"),
    ("Mahinder", "Dhoni"),
    ("Akbar", "Khan"),
    ("Howard", "Wolowitz"),
    ("Pinkie", "Petit"),
    ("Gurkaran", "Singh"),
    ("Amy", "Farah Fowler"),
    ("Marlon", "Crafford"),
]
movies = [
    ("Forrest Gump", 1994, "Drama", 330.2),
    ("3 Idiots", 2009, "Drama", 2.4),
    ("Eternal Sunshine of the Spotless Mind", 2004, "Drama", 34.5),
    ("Good Will Hunting", 1997, "Drama", 138.1),
    ("Skyfall", 2012, "Action", 304.6),
    ("Gladiator", 2000, "Action", 188.7),
    ("Black", 2005, "Drama", 3.0),
    ("Titanic", 1997, "Romance", 659.2),
    ("The Shawshank Redemption", 1994, "Drama", 28.4),
    ("Udaan", 2010, "Drama", 1.5),
    ("Home Alone", 1990, "Comedy", 286.9),
    ("Casablanca", 1942, "Romance", 1.0),
    ("Avengers: Endgame", 2019, "Action", 858.8),
    ("Night of the Living Dead", 1968, "Horror", 2.5),
    ("The Godfather", 1972, "Crime", 135.6),
    ("Haider", 2014, "Action", 4.2),
    ("Inception", 2010, "Adventure", 293.7),
    ("Evil", 2003, "Horror", 1.3),
    ("Toy Story 4", 2019, "Animation", 434.9),
    ("Air Force One", 1997, "Drama", 138.1),
    ("The Dark Knight", 2008, "Action", 535.4),
    ("Bhaag Milkha Bhaag", 2013, "Sport", 4.1),
    ("The Lion King", 1994, "Animation", 423.6),
    ("Pulp Fiction", 1994, "Crime", 108.8),
    ("Kai Po Che", 2013, "Sport", 6.0),
    ("Beasts of No Nation", 2015, "War", 1.4),
    ("Andadhun", 2018, "Thriller", 2.9),
    ("The Silence of the Lambs", 1991, "Crime", 68.2),
    ("Deadpool", 2016, "Action", 363.6),
    ("Drishyam", 2015, "Mystery", 3.0)
]
ratings_records = [
    (6.4, 17, 5), (5.6, 19, 1), (6.3, 22, 14), (5.1, 21, 17),
    (5.0, 5, 5), (6.5, 21, 5), (8.5, 30, 13), (9.7, 6, 4),
    (8.5, 24, 12), (9.9, 14, 9), (8.7, 26, 14), (9.9, 6, 10),
    (5.1, 30, 6), (5.4, 18, 16), (6.2, 6, 20), (7.3, 21, 19),
    (8.1, 17, 18), (5.0, 7, 2), (9.8, 23, 3), (8.0, 22, 9),
    (8.5, 11, 13), (5.0, 5, 11), (5.7, 8, 2), (7.6, 25, 19),
    (5.2, 18, 15), (9.7, 13, 3), (5.8, 18, 8), (5.8, 30, 15),
    (8.4, 21, 18), (6.2, 23, 16), (7.0, 10, 18), (9.5, 30, 20),
    (8.9, 3, 19), (6.4, 12, 2), (7.8, 12, 22), (9.9, 15, 13),
    (7.5, 20, 17), (9.0, 25, 6), (8.5, 23, 2), (5.3, 30, 17),
    (6.4, 5, 10), (8.1, 5, 21), (5.7, 22, 1), (6.3, 28, 4),
    (9.8, 13, 1)
]



insert = Insert("arduino", "arduino", "127.0.0.1", "university")
insert.table('movies').columns(["title", "release_year","genre","collection_in_mil"], movies).apply()
insert.table('reviewers').columns(["first_name", "last_name"], reviewers_records).apply()
insert.table('ratings').columns(["rating", "movie_id","reviewer_id"], ratings_records).apply()
insert.table('ratings').column("rating", 5.0).apply()


select = Select("arduino", "arduino", "127.0.0.1", "university")
select.table("movies").columns(["title,release_year"]).limit("5").apply()
select.table("movies").columns(["title,collection_in_mil"]).where(["collection_in_mil>300"]).orderby("collection_in_mil","DESC").\
    limit("5").apply()

select.table("ratings").columns(["title, AVG(rating) as average_rating"])\
    .innerjoin("movies","movies.id = ratings.movie_id").group_by("movie_id").\
    orderby("average_rating","DESC").\
    limit("5").apply()

select.table("reviewers").columns(["CONCAT(first_name, \" \", last_name), COUNT(*) as num"])\
    .innerjoin("ratings","reviewers.id = ratings.reviewer_id").group_by("reviewer_id").\
    orderby("num","DESC").\
    limit("1").apply()

update = Update("arduino", "arduino", "127.0.0.1", "university")
update.table("reviewers").column("last_name","Cooper").where("first_name=Amy").apply()
update.table("ratings").column("rating",5.0).where("movie_id=18").where("reviewer_id=15").apply()


delete = Delete("arduino", "arduino", "127.0.0.1", "university")
delete.table("ratings").where("reviewer_id=2").apply()

delete.table("reviewers")
