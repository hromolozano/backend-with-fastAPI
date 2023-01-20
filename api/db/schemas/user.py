def user_schema(user) -> dict:
    return {"id":user["_id"],
            "surname":user["surname"],
            "name":user["name"]}