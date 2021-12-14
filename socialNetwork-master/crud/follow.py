from models.user import UserModel
import sqlite3
from models.user import BaseUserModel


class FollowCRUD:
    def exists(
            self, conn: sqlite3.Connection, user: UserModel, to_follow: UserModel
    ) -> bool:
        cur = conn.cursor()

        try:
            cur.execute(
                "SELECT COUNT(*) FROM Follow WHERE follower=? AND follows=?",
                (user.id, to_follow.id),
            )
            count, *_ = cur.fetchone()
            return count == 1
        finally:
            cur.close()

    def create(
            self, conn: sqlite3.Connection, user: UserModel, to_follow: UserModel
    ) -> None:
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO Follow VALUES(?, ?)", (user.id, to_follow.id))
        finally:
            cur.close()

    def delete(
            self, conn: sqlite3.Connection, user: UserModel, to_unfollow: UserModel
    ) -> None:
        cur = conn.cursor()

        try:
            cur.execute(
                "DELETE FROM Follow WHERE follower=? AND follows=?",
                (user.id, to_unfollow.id),
            )
        finally:
            cur.close()

    # найти подписки
    def find_follows(
            self, conn: sqlite3.Connection, id: str
    ) -> list[BaseUserModel]:
        cur = conn.cursor()

        try:
            cur.execute(
                "SELECT User.id, User.login "
                "FROM User "
                "JOIN Follow "
                "ON User.id = Follow.follows "
                "WHERE Follow.follower = ? ",
                (id,),

            )
            rows = cur.fetchall()
            return [BaseUserModel(id=id, login=login) for id, login in rows]
        finally:
            cur.close()

    # найти подписчиков
    def find_followers(
            self, conn: sqlite3.Connection, id: str
    ):
        cur = conn.cursor()

        try:
            cur.execute(
                "SELECT User.id, User.login "
                "FROM User "
                "JOIN Follow "
                "ON User.id = Follow.follower "
                "WHERE Follow.follows = ?",
                (id,),
            )
            rows = cur.fetchall()
            return [BaseUserModel(id=id, login=login) for id, login in rows]
        finally:
            cur.close()
