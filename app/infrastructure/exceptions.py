class RepositoryError(Exception):
    pass


class EntityNotFoundError(RepositoryError):
    def __init__(self, entity_type: str, entity_id: str):
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(f"{entity_type} {entity_id} not found.")


class EntityAlreadyExistsError(RepositoryError):
    def __init__(self, entity_type: str):
        self.entity_type = entity_type
        super().__init__(f"{entity_type} already exists.")


class DatabaseError(RepositoryError):
    def __init__(self, operation: str, details: str):
        self.operation = operation
        self.details = details
        super().__init__(f"Database {operation} failed: {details}.")
