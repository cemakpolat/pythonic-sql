"""
@author: Cem Akpolat
@created by cemakpolat at 2021-09-23
"""
from sql import *

create = Create("arduino", "arduino", "127.0.0.1", "university")
create.table("reviewers").\
    column("id", DataTypes.int).set_pkey("id", auto_increment=True).\
    column("name", DataTypes.varchar, 200).\
    column("surname", DataTypes.varchar, 200).\
    apply()

create.table("reviewerss"). \
    column("x_id", DataTypes.int). \
    column("id", DataTypes.int). \
    column("name", DataTypes.varchar, 200). \
    column("surname", DataTypes.varchar, 200). \
    set_pkeys(["x_id", "id"]). \
    apply()


create.table("movies").\
    column("id", DataTypes.int).set_pkey("id", auto_increment=True).\
    column("name", DataTypes.varchar, 200).\
    column("year", DataTypes.varchar, 100).\
    column("reviewer_id", DataTypes.int).\
    add_fkey("reviewer_id", "reviewers","id").\
    apply()



records = [("cem","akpolat")]
insert = Insert("arduino", "arduino", "127.0.0.1", "university")
insert.table('reviewers').columns(["name", "surname"], records).apply()
insert.table('reviewers').column("name", "levin").column("surname", "levin").apply()


select = Select("arduino", "arduino", "127.0.0.1", "university")
select.table("reviewers").columns(["*"]).where(["id=6"]).apply()

select.table("a").columns(["a","b"]).innerjoin("table","a.id=b.id").leftjoin("c","b.id=c.id").\
    where(["10<=!price!=<20","categortyid!=[1,2,3]","a!=b","c>d","d<x | d=y | a=b","w=m","t=m","column ~ a"]).orderby("a.column","ASC").\
    apply()


update = Update("arduino", "arduino", "127.0.0.1", "university")
update.table("reviewers").columns(["name","surname"],["aren","aren"]).where("id=1").apply()
update.table("reviewers").column("name","aren").column("surname","aren").where("id=7").apply()


delete = Delete("arduino", "arduino", "127.0.0.1", "university")
delete.table("reviewers").where("id=17").apply()
delete.table("reviewers")
