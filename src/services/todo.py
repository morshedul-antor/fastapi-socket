from services import BaseService
from repositories import todo_repo
from models import ToDo
from schemas import TodoIn, TodoUpdate
from sqlalchemy.orm import Session
from exceptions import ServiceResult, AppException
from fastapi import status

from ws import send_message_to_connections


class TodoService(BaseService[ToDo, TodoIn, TodoUpdate]):

    async def create_todo(self, db: Session, data_in: TodoIn, user_id: int):
        todo = self.repo.create_todo(db=db, data_in=data_in, user_id=user_id)

        if not todo:
            return ServiceResult(AppException.ServerError("Todo not created!"))
        else:
            await send_message_to_connections('A new Task has been created!')
            return ServiceResult(todo, status_code=status.HTTP_201_CREATED)


todo_service = TodoService(ToDo, todo_repo)
