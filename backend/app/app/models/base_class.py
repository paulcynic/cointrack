import typing as t

from sqlalchemy.ext.declarative import as_declarative, declared_attr


class_registry: t.Dict = {}


@as_declarative(class_registry=class_registry)
class Base:
    id: t.Any
    __name__: str

    # Generate __tablename__ automatically from classname
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

# Usually you may have seen Base = declarative_base()
# but in that case you should add __tablename__ every new class
