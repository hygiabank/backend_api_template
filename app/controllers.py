from typing import Optional
from app.database.user_repository import user_repository, User
from app.security import authenticate_user
from app.exceptions import Unauthorized

import numpy as np
from datetime import datetime

async def create_user(**kwargs) -> dict:
    new_user = await user_repository.create(**kwargs)
    return {
        "id": new_user.id,
        "name": new_user.name,
        "age": new_user.age,
        "username": new_user.username,
        "creation_timestamp": datetime.utcnow()
    }

async def read_user(id: int) -> dict:
    user = await user_repository.get(id=id)
    return {
        "id": user.id,
        "name": user.name,
        "age": user.age,
        "username": user.username,
    }

async def update_user(id: str, **kwargs) -> dict:
    updated_user = await user_repository.update(id=id, **kwargs)
    return {
        "id": updated_user.id,
        "name": updated_user.name,
        "age": updated_user.age,
        "username": updated_user.username,
    }

async def delete_user(id: str) -> None:
    return await user_repository.delete(id=id)

async def read_users(skip: int = 0, limit: int = 100, filter_dict: Optional[dict] = None) -> list[dict]:
    users = await user_repository.get_all(skip=skip, limit=limit, filter=filter_dict)
    return [
        {
            "id": user.id,
            "name": user.name,
            "age": user.age,
            "username": user.username,
        } for user in users
    ]

async def return_user_statistics(resample_time: int = 86400000):

    """
    Return user statistics:

    Param: 
        resample_time (int): resample time, default value is 1 day in ms
    Output:
        dict: new_user_per_time (list), user_per_time_acc (list), average_user_age (float)
    """

    users = await user_repository.get_all(limit = None)

    # Averages metrics
    average_user_age = np.mean([user.age for user in users])


    # Aggregations metrics

    users_creation_timestamp = [user.creation_timestamp for user in users]

    starter_user = np.min(users_creation_timestamp)
    time = datetime.utcnow()
    new_user_per_time = []

    while time >= starter_user:

        acc_users_in_this_time = np.sum(np.where(
            (users_creation_timestamp <= time) & 
            (users_creation_timestamp >= (time - resample_time)), 
            1, 
            0
        ))

        time -= resample_time

        new_user_per_time.append(acc_users_in_this_time)


    user_per_time_acc = np.cumsum(new_user_per_time)

    return {
        "new_user_per_time": new_user_per_time, 
        "user_per_time_acc": user_per_time_acc, 
        "average_user_age": average_user_age,
    }

async def authenticate(username: str, password: str) -> dict:
    user = await User.get(username=username)
    if not user:
        raise Unauthorized("Invalid username")
    print(password)
    authenticate_user(password, user.password)
    
    return {
        "id": str(user.id),
        "name": user.name,
        "age": user.age,
        "username": user.username,
    }
