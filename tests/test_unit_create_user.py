import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.routes.users import create_user, get_users, get_user, update_user, remove_user
from database.models import User
from src.schemas import UserModel

class TestNotes(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)


    async def test_create_user_found(self):
        body = UserModel(title="test", description="test create user", user = 1)
        user = User()
        self.session.query().filter().all.return_value = user
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.title, body.title)
        self.assertEqual(result.description, body.description)
        self.assertEqual(result.user, user)
        

    async def test_get_users(self):
        users = [User(), User(), User()]
        self.session.query().filter().offset().limit().all.return_value = users
        result = await get_users(skip=0, limit=10, db=self.session)
        self.assertEqual(result, users)


    async def test_get_user_found(self):
        user = User()
        self.session.query().filter().first.return_value = user
        result = await get_user(user_id=1, db=self.session)
        self.assertEqual(result, user)

    async def test_get_user_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_user(user_id=1, db=self.session)
        self.assertIsNone(result)


    async def test_update_user_found(self):
        body = UserModel(title="test", description="test update", done=True)
        users = [User(id=1), User(id=2)]
        user = User(users=users)
        self.session.query().filter().first.return_value = user
        self.session.query().filter().all.return_value = users
        self.session.commit.return_value = None
        result = await update_user(user_id=1, body=body, db=self.session)
        self.assertEqual(result, user)


    async def test_update_note_not_found(self):
        body = UserModel(title="test", description="test update", done=True)
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_user(user_id=1, body=body, db=self.session)
        self.assertIsNone(result)


    async def test_remove_user_found(self):
        user = User()
        self.session.query().filter().first.return_value = user
        result = await remove_user(user_id=1, db=self.session)
        self.assertEqual(result, user)

    async def test_remove_note_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_user(note_id=1, db=self.session)
        self.assertIsNone(result)



if __name__ == '__main__':
    unittest.main()
