from sqlalchemy import update, insert, select, delete

from database import engine
from models import User



class CreateUser(User):
  
  values = [
    {'display_name': 'Sebastian'},
    {'email': 'sebastian@email.com'},
    {'hashed_password': '123456'},
  ]
  
  engine.execute(User.insert(), values)


class GetUsers(User):

  users = select([User.id])
  result = engine.execute(users)


class UpdateUser(User):

  update_user = update(User).where(User.c.id == 1).values(name='John Smith')
  engine.execute(update_user)


class DeleteUser(User):

  delete_user = delete(User).where(User.c.id == 1)
  engine.execute(delete_user)