import os
import sys
from peewee import *
from datetime import date

import logging
logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

dbpath = 'people.db'
db = SqliteDatabase(dbpath)


class Person(Model):
    """
    CREATE TABLE "person" (
        "id" INTEGER NOT NULL PRIMARY KEY,
        "name" VARCHAR(255) NOT NULL,
        "birthday" DATE NOT NULL,
        "is_relative" INTEGER NOT NULL)
    """
    name = CharField()
    birthday = DateField()
    is_relative = BooleanField()

    class Meta:
        database = db


class Pet(Model):
    """CREATE TABLE "pet" (
        "id" INTEGER NOT NULL PRIMARY KEY,
        "owner_id" INTEGER NOT NULL,
        "name" VARCHAR(255) NOT NULL,
        "animal_type" VARCHAR(255) NOT NULL,
        FOREIGN KEY ("owner_id") REFERENCES "person" ("id")
    )
    CREATE INDEX "pet_owner_id" ON "pet" ("owner_id")
    """
    owner = ForeignKeyField(Person, related_name='pets')    # Pet.owner_id == Persion.id
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db

# select fields from table1, table2 on table1.id=table2.id2 where conditions order by limit
def recreate_database():
    try:
        os.remove(dbpath)
        db.connect()
        db.create_tables([Person, Pet])
    except:
        pass


def create_update():
    """
    #>>> sqlite3 -column -header  people.db "select * from person"
    id          name        birthday    is_relative
    ----------  ----------  ----------  -----------
    1           Bob         1960-01-15  1
    2           Grandma L.  1935-03-01  1
    3           Herb        1950-05-05  0
    #>>> sqlite3 -column -header  people.db "select * from pet"
    id          owner_id    name        animal_type
    ----------  ----------  ----------  -----------
    1           1           Kitty       cat
    2           1           Fido        dog
    4           3           Mittens Jr  cat
    """
    recreate_database()

    # 第一条记录
    uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15), is_relative=True)
    # ('INSERT INTO "person" ("name", "birthday", "is_relative") VALUES (?, ?, ?)', ['Bob', datetime.date(1960, 1, 15), True])
    uncle_bob.save()

    # 第二条记录
    grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1), is_relative=True)

    # 第三条记录
    herb = Person.create(name='Herb', birthday=date(1950, 5, 5), is_relative=False)

    # 修改、保存
    # ('UPDATE "person" SET "name" = ?, "birthday" = ?, "is_relative" = ? WHERE ("person"."id" = ?)', ['Grandma L.', datetime.date(1935, 3, 1), True, 2])
    grandma.name = 'Grandma L.'
    grandma.save()

    # 创建1个pet, 主人是ubcle_bob
    bob_kitty = Pet.create(owner=uncle_bob, name='Kitty', animal_type='cat')

    # 创建3个pet, 主人是herb
    herb_fido = Pet.create(owner=herb, name='Fido', animal_type='dog')
    herb_mittens = Pet.create(owner=herb, name='Mittens', animal_type='cat')
    herb_mittens_jr = Pet.create(owner=herb, name='Mittens Jr', animal_type='cat')

    # 删除pet herb_mittens
    herb_mittens.delete_instance()

    # herb_fido的owner从 herb -> uncle_bob
    herb_fido.owner = uncle_bob
    # ('UPDATE "pet" SET "owner_id" = ?, "name" = ?, "animal_type" = ? WHERE ("pet"."id" = ?)', [1, 'Fido', 'dog', 2])
    herb_fido.save()

    db.close()


def query_test():
    create_update()
    db.connect()

    # select * from Person where name='Grandma L.' limit 1
    grandma = Person.select().where(Person.name == 'Grandma L.').get()
    grandma = Person.get(Person.name == 'Grandma L.')

    # select * from Person
    for person in Person.select():
        print(person.name, person.is_relative)

    print(sys._getframe().f_lineno, "---" * 3)

    # select * from Pet where animal_type='cat'
    query = Pet.select().where(Pet.animal_type == 'cat')
    for pet in query:
        # pet.owner会触发 select * from Person where id=? limit 1
        print(pet.name, pet.owner.name)

    print(sys._getframe().f_lineno, "---" * 3)

    # 上面用了N+1次查询， 下面的改进使用1次查询
    # select t1.*, t2.* from pet t1 inner join person t2 on (t1.owner_id=t2.id) where t1.animal_type='cat'
    query = (Pet
             .select(Pet, Person)
             .join(Person)
             .where(Pet.animal_type == "cat"))
    for pet in query:
        print(pet.name, pet.owner.name)

    print(sys._getframe().f_lineno, "---" * 3)

    # select t1.* from pet t1 inner join person t2 on (t1.owner_id=t2.id) where t2.name='Bob'
    for pet in Pet.select().join(Person).where(Person.name == 'Bob'):
        print(pet.name)

    print(sys._getframe().f_lineno, "---" * 3)

    # select * from pet where owner_id=? order by name
    uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15), is_relative=True)
    for pet in Pet.select().where(Pet.owner == uncle_bob).order_by(Pet.name):
        print(pet.name)

    print(sys._getframe().f_lineno, "---" * 3)

    # select * from person order by birthday desc
    for person in Person.select().order_by(Person.birthday.desc()):
        print(person.name, person.birthday)

    print(sys._getframe().f_lineno, "---" * 3)

    # select * from person
    for person in Person.select():
        # select count(*) from pets where owner_id=?
        print(person.name, person.pets.count(), 'pets')
        # select * from pets where owner_id=?
        for pet in person.pets:
            print("\t", pet.name, pet.animal_type)

    print(sys._getframe().f_lineno, "---" * 3)

    # 改进
    # select t1.*, t2.*, (select count(t3.id) from pet t3 where (t3.owner_id=t1.id)) as per_count
    # from person t1 left outer join pet t2 on (t1.id=t2.owner_id) order by t1.name
    subquery = Pet.select(fn.COUNT(Pet.id)).where(Pet.owner == Person.id)
    query = (Person
             .select(Person, Pet, subquery.alias('pet_count'))
             .join(Pet, JOIN.LEFT_OUTER)
             .order_by(Person.name))
    for person in query.aggregate_rows():
        print(person.name, person.pet_count, 'pets')
        for pet in person.pets:
            print("\t", pet.name, pet.animal_type)

    print(sys._getframe().f_lineno, "---" * 3)

    d1940 = date(1940, 1, 1)
    d1960 = date(1960, 1, 1)
    # select * from person where birthday<? or birthday>?
    query = (Person
             .select()
             .where((Person.birthday < d1940) | (Person.birthday > d1960)))
    print(query.sql())
    print(sys._getframe().f_lineno, "---" * 3)

    query = (Person
             .select()
             .where((Person.birthday > d1940) & (Person.birthday < d1960)))
    # select * from person where birthday<? and birthday>?
    print(query.sql())
    print(sys._getframe().f_lineno, "---" * 3)

    # select * from person where lower(substr(name, 1, 1))='g'
    expression = (fn.Lower(fn.Substr(Person.name, 1, 1)) == 'g')
    query = Person.select().where(expression)
    print(query.sql())
if __name__ == "__main__":
    # create_update()
    query_test()


# python -m pwiz -e postgresql charles_blog > blog_models.py