@strawberry.type
class UserGraphQL:
    id: int | None
    name: str
    email: str

    @staticmethod
    def from_sqlmodel(instance: User) -> "UserGraphQL":
        return UserGraphQL(
            id=instance.id,
            name=instance.name,
            email=instance.email
        )