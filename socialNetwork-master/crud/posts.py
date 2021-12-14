from models.posts import BaseCreatePostModel, CreatePostModel, ReturnPostModel
import sqlite3

from models.user import UserModel


class PostsCRUD:
    def create(
            self, conn: sqlite3.Connection, data: BaseCreatePostModel, user: UserModel
    ) -> None:
        data = CreatePostModel(**data.dict(), creator_id=user.id)
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO Posts(id, creator, description, created) "
                "VALUES(?, ?, ?, ?)",
                (
                    data.id,
                    data.creator_id,
                    data.description,
                    data.created,
                ),
            )
        finally:
            cur.close()

    def get_by_creator(
            self, conn: sqlite3.Connection, creator: UserModel
    ) -> list[ReturnPostModel]:
        cur = conn.cursor()

        try:
            cur.execute(
                "SELECT id, description, created "
                "FROM Posts "
                "WHERE creator=?"
                "ORDER BY created DESC",
                (creator.id,),
            )
            data = cur.fetchall()
            return [
                ReturnPostModel(
                    id=id,
                    creator=creator.id,

                    description=description,
                    created=created,
                )
                for (id, description, created) in data
            ]
        finally:
            cur.close()

    def get_by_follower(
            self, conn: sqlite3.Connection, user: UserModel
    ) -> list[ReturnPostModel]:
        cur = conn.cursor()

        try:
            cur.execute(
                "SELECT Posts.id, Posts.description, Posts.created, User.id AS user_id "
                "FROM Posts "
                "JOIN Follow ON Posts.creator = Follow.follows "
                "JOIN User ON Posts.creator = User.id "
                "WHERE Follow.follower = ? "
                "ORDER BY created DESC",
                (user.id,),
            )
            data = cur.fetchall()
            return [
                ReturnPostModel(
                    id=id,
                    creator=user_id,
                    description=description,
                    created=created,
                )
                for (id, description, created, user_id) in data
            ]
        finally:
            cur.close()

    # добыть все посты
    def get_by_all(
            self, conn: sqlite3.Connection
    ):
        cur = conn.cursor()

        try:
            cur.execute(
                "SELECT id, creator,  description, created "
                "FROM Posts "
                "ORDER BY created DESC"

            )
            data = cur.fetchall()
            return [
                ReturnPostModel(
                    id=id,
                    creator=creator,
                    description=description,
                    created=created,
                )
                for (id, creator, description, created) in data
            ]

        finally:
            cur.close()

    # удаление поста
    def delete(
            self, conn: sqlite3.Connection, post: str
    ) -> None:
        cur = conn.cursor()

        try:
            cur.execute(
                "DELETE FROM Posts WHERE id=?",
                (post,),
            )
        finally:
            cur.close()

    def get(self, conn: sqlite3.Connection, post: str
            ):

        cur = conn.cursor()

        try:
            cur.execute(
                "SELECT Posts.id, Posts.description, Posts.created, Posts.creator FROM Posts WHERE Posts.id = ?",
                (post,),
            )
            data = cur.fetchone()
            id, description, created, creator = data
            return ReturnPostModel(id=id, description=description, created=created, creator=creator)

        finally:
            cur.close()
