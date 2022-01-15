from sqlalchemy import (
    Table,
    Column,
    Float,
    Numeric,
    Integer,
    String,
    ForeignKey,
    Boolean,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(150), nullable=False)
    imie = Column(String, nullable=True)
    nazwisko = Column(String, nullable=True)

    def __repr__(self):
        return f"User {self.id}, {self.username}, {self.email}"


class Friend(Base):
    __tablename__ = "friends"

    id = Column(Integer, primary_key=True)
    friend1 = Column(String(30))
    friend2 = Column(String(30))

    def __repr__(self):
        return f"friend1 {self.friend1}, friend2 {self.friend2}"


locations_mushrooms = Table(
    "locations_mushrooms",
    Base.metadata,
    Column(
        "id_location", ForeignKey("locations.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "id_mushroom", ForeignKey("mushrooms.id", ondelete="CASCADE"), primary_key=True
    ),
)


shared_locations = Table(
    "shared_locations",
    Base.metadata,
    Column(
        "id_location", ForeignKey("locations.id", ondelete="CASCADE"), primary_key=True
    ),
    Column("friend_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
)

User.loc_shared_with_me = relationship(
    "Location", secondary=shared_locations, backref="user"
)


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    nazwa = Column(String(150))
    opis = Column(String(3000))
    center_lat = Column(Float(precision=10))
    center_lon = Column(Float(precision=10))
    radius_in_meters = Column(Numeric(10))
    owner_id = Column(Integer, ForeignKey("users.id"))
    czy_publiczna = Column(Boolean(create_constraint=True))

    owner = relationship("User", backref="locations")
    loc_mushrooms = relationship(
        "Mushroom",
        secondary=locations_mushrooms,
        backref="locations",
        cascade="all, delete",
    )
    shared_with = relationship(
        "User", secondary=shared_locations, backref="locations2", cascade="all, delete"
    )

    def __repr__(self):
        return f"Location {self.id}, name {self.nazwa}"


User.my_locations = relationship("Location", order_by=Location.id, backref="users")


class Mushroom(Base):
    __tablename__ = "mushrooms"

    id = Column(Integer, primary_key=True)
    nazwa_formalna = Column(String(150), unique=True)
    nazwa_nieformalna = Column(String(150), unique=True)
    photos_json = Column(String(3000))
    opis_cech_json = Column(String(3000))
    warunki_wystepowania_json = Column(String(3000))
    opis_objawow_zatrucia_json = Column(String(3000))
    wystepuje_miesiac_01 = Column(Boolean(create_constraint=True))
    wystepuje_miesiac_02 = Column(Boolean(create_constraint=True))
    wystepuje_miesiac_03 = Column(Boolean(create_constraint=True))
    wystepuje_miesiac_04 = Column(Boolean(create_constraint=True))
    wystepuje_miesiac_05 = Column(Boolean(create_constraint=True))
    wystepuje_miesiac_06 = Column(Boolean(create_constraint=True))
    wystepuje_miesiac_07 = Column(Boolean(create_constraint=True))
    wystepuje_miesiac_08 = Column(Boolean(create_constraint=True))
    wystepuje_miesiac_09 = Column(Boolean(create_constraint=True))
    wystepuje_miesiac_10 = Column(Boolean(create_constraint=True))
    wystepuje_miesiac_11 = Column(Boolean(create_constraint=True))
    wystepuje_miesiac_12 = Column(Boolean(create_constraint=True))
    czy_trujacy = Column(Boolean(create_constraint=True))
    czy_jadalny = Column(Boolean(create_constraint=True))
    czy_chroniony = Column(Boolean(create_constraint=True))

    mush_locations = relationship(
        "Location",
        secondary=locations_mushrooms,
        backref="mushrooms",
        passive_deletes=True,
    )

    def __repr__(self):
        return f"Mushroom {self.id}, name {self.nazwa_formalna}"


def main():
    from sqlalchemy import create_engine
    from config import get_db_uri

    engine = create_engine(get_db_uri(), echo=True)

    Base.metadata.create_all(engine)

    return "Database created with success"


if __name__ == "__main__":
    main()
