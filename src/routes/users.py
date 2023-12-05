from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import UserModel, UserResponce

from fastapi_limiter.depends import RateLimiter


router = APIRouter(prefix="/users", tags=['users'])


@router.get("/", response_model=List[UserResponce], name="Вернуть юзеров")
async def get_users(db: Session = Depends(get_db)):
    '''
    Находит всех юзеров
    '''
    users = db.query(User).all()
    return users


@router.get("/{user_id}", response_model=UserResponce, name='Найти юзера')
async def get_user(user_id: int = Path(ge=1), db: Session = Depends(get_db)):
    '''
    Находит юзера
    '''
    user = db.query(User).filter_by(id=user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return user


@router.post("/", response_model=UserResponce, description='No more than 10 requests per minute', 
             dependencies=[Depends(RateLimiter(times=2, seconds=60))],
             status_code=status.HTTP_201_CREATED, name='Создать юзера'
            )
async def create_user(body: UserModel, db: Session = Depends(get_db)):
    '''
    Создаёт юзера
    '''
    user = db.query(User).filter_by(email=body.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email is exists!')
    user = User(**body.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}", response_model=UserResponce, name='Обновить юзера')
async def update_user(body: UserModel, user_id: int = Path(ge=1), db: Session = Depends(get_db)):
    '''
    Меняет данные юзера
    '''
    user = db.query(User). filter_by(id=user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    user.firstname = body.firstname
    user.secondname = body.secondname
    user.email = body.email
    user.phonenumber = body.phonenumber
    user.birthday = body.birthday
    db.commit()
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, name='Удалить юзера')
async def remove_user(user_id: int = Path(ge=1), db: Session = Depends(get_db)):
    '''
    Удаляет юзера
    '''
    user = db.query(User).filter_by(id=user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    


async def get_user_by_email(email: str, db: Session) -> User:
    '''
    Находит юзера по его емейл
    '''
    return db.query(User).filter(User.email == email).first()



async def confirmed_email(email: str, db: Session) -> None:
    '''
    Подтверждает что юзер получил сообщение
    '''
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()