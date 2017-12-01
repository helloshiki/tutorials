import os
import sys
from peewee import *

dbpath = 'test2.db'
database = SqliteDatabase(dbpath)


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    """
    CREATE TABLE "user" (
        "id" INTEGER NOT NULL PRIMARY KEY,
        "username" VARCHAR(255) NOT NULL,
        "password" VARCHAR(255) NOT NULL,
        "email" VARCHAR(255) NOT NULL,
        "join_date" DATETIME NOT NULL)
    CREATE UNIQUE INDEX "user_username" ON "user" ("username")
    """
    username = CharField(unique=True)
    password = CharField()
    email = CharField()
    join_date = DateTimeField()

    class Meta:
        order_by = ('username',)


class RelationShip(BaseModel):
    """
    CREATE TABLE "relationship" (
        "id" INTEGER NOT NULL PRIMARY KEY,
        "from_user_id" INTEGER NOT NULL,
        "to_user_id" INTEGER NOT NULL,
        FOREIGN KEY ("from_user_id") REFERENCES "user" ("id"), FOREIGN KEY ("to_user_id") REFERENCES "user" ("id"))
    CREATE INDEX "relationship_from_user_id" ON "relationship" ("from_user_id")
    CREATE INDEX "relationship_to_user_id" ON "relationship" ("to_user_id")
    CREATE UNIQUE INDEX "relationship_from_user_id_to_user_id" ON "relationship" ("from_user_id", "to_user_id")
    """
    from_user = ForeignKeyField(User, related_name="relationships")
    to_user = ForeignKeyField(User, related_name="related_to")

    class Meta:
        indexes = ((("from_user", "to_user"), True)),

    def following(self):
        return (User
                .select()
                .join(RelationShip, on=RelationShip.to_user)
                .where(RelationShip.from_user == self))

    def followers(self):
        return (User
                .select()
                .join(RelationShip, on=RelationShip.from_user)
                .where(RelationShip.to_user == self))


class Message(BaseModel):
    """
    CREATE TABLE "message" (
        "id" INTEGER NOT NULL PRIMARY KEY,
        "user_id" INTEGER NOT NULL,
        "content" TEXT NOT NULL,
        "pub_date" DATETIME NOT NULL,
        FOREIGN KEY ("user_id") REFERENCES "user" ("id"))
    CREATE INDEX "message_user_id" ON "message" ("user_id")
    """
    user = ForeignKeyField(User)
    content = TextField()
    pub_date = DateTimeField()

    class Meta:
        order_by = ('-pub_date',)


def create_tables():
    database.connect()
    database.create_tables([User, RelationShip, Message])

# create_tables()
print(RelationShip.sqlall())
