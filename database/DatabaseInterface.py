import json

from itertools import zip_longest

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import eagerload
from database.setup_db import User, Friend, Location, Mushroom

from typing import List, Dict

from werkzeug.security import generate_password_hash, check_password_hash


class DatabaseSessionManager:
    def __init__(self, db_engine):
        self.session = sessionmaker(bind=db_engine)

    def add_new_objects(self, objects: List):
        with self.session() as s:
            for t in objects:
                s.add(t)
            s.commit()
        return True

    def remove_objects(self, objects: List):
        with self.session() as s:
            for t in objects:
                s.delete(t)
            s.commit()
        return True

    def update_object(self, item_id, item_class, **kwargs):
        with self.session() as s:
            s.query(item_class).filter_by(id=item_id).update(dict(kwargs))
            s.commit()
        return True

    def fetch_objects(self, class_def, filters: Dict):
        with self.session() as s:
            if filters:
                results = s.query(class_def).filter_by(**filters).all()
            else:
                results = s.query(class_def).all()

        return results

    def fetch_objects_data(self, class_def, filters: Dict):
        with self.session() as s:
            if filters:
                results = s.query(class_def).options(eagerload('*')).filter_by(**filters).all()
            else:
                results = s.query(class_def).options(eagerload('*')).all()

        return results


class LocationsManager:
    """Class to interact with Database to manage Locations"""
    def __init__(self, session_manager: DatabaseSessionManager):
        self.session = session_manager
        self._loc_class = Location

    @property
    def this_class(self):
        return self._loc_class

    def fetch_all_locations(self, filters=None):
        if filters is None:
            filters = {}
        return self.session.fetch_objects_data(class_def=self._loc_class, filters=filters)

    def add_location(self, **kwargs):
        """
        nazwa = Column(String(150))
        opis = Column(String(3000))
        owner_id = Column(Integer, ForeignKey('users.id'))
        czy_publiczna = Column(Boolean(create_constraint=True))

        owner = relationship('User', backref='locations')
        loc_mushrooms = relationship('Mushroom', secondary=locations_mushrooms, backref='locations')
        """
        new_location = self._loc_class(**kwargs)
        self.session.add_new_objects(objects=[new_location])
        return True

    def remove_location(self, object_id):
        obj_to_remove = self.session.fetch_objects(class_def=self._loc_class, filters={"id": object_id})
        self.session.remove_objects(objects=obj_to_remove)
        return True

    def update_location(self, object_id, **kwargs):
        self.session.update_object(item_id=object_id, item_class=self._loc_class, **kwargs)
        return True


class UsersManager:
    """Class to interact with Database to manage Users"""
    def __init__(self, session_manager: DatabaseSessionManager):
        self.session = session_manager
        self._user_class = User

    @property
    def this_class(self):
        return self._user_class

    def fetch_all_users(self, filters=None):
        if filters is None:
            filters = {}
        return self.session.fetch_objects(class_def=self._user_class, filters=filters)

    def register_new_user(self, username: str, password: str, email: str):
        hashed_pass = generate_password_hash(password, method='sha256')
        user = self._user_class(username=username, password=hashed_pass, email=email)
        self.session.add_new_objects(objects=[user])
        return True


class MushroomsManager:
    """Class to interact with Database to manage Mushrooms"""
    def __init__(self, session_manager: DatabaseSessionManager):
        self.session = session_manager
        self._ms_class = Mushroom

    @property
    def this_class(self):
        return self._ms_class

    def fetch_all_mushrooms(self, filters=None):
        if filters is None:
            filters = {}
        return self.session.fetch_objects_data(class_def=self._ms_class, filters=filters)

    def add_new_mushroom(self, **kwargs):
        """
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
        """
        new_ms = self._ms_class(**kwargs)
        self.session.add_new_objects(objects=[new_ms])
        return True

    def remove_mushroom(self, object_id):
        obj_to_remove = self.session.fetch_objects(class_def=self._ms_class, filters={'id': object_id})
        self.session.remove_objects(objects=obj_to_remove)
        return True


class FriendsManager:
    """Class to interact with Database to manage Friendships"""
    def __init__(self, session_manager: DatabaseSessionManager):
        self.session = session_manager
        self._fr_class = Friend

    def fetch_friends(self, filters: Dict):
        if filters is None:
            filters = {}
        return self.session.fetch_objects_data(class_def=self._fr_class, filters=filters)

    def add_friend(self, **kwargs):
        new_friendship = self._fr_class(**kwargs)
        self.session.add_new_objects(objects=[new_friendship])
        return True

    def remove_friend(self, object_id):
        friendship_to_remove = self.session.fetch_objects(class_def=self._fr_class, filters={'id': object_id})
        self.session.remove_objects(objects=friendship_to_remove)
        return True


class DatabaseFacade:

    def __init__(self, session_manager):
        self.session = session_manager
        self.locations = LocationsManager(session_manager=session_manager)
        self.users = UsersManager(session_manager=session_manager)
        self.mushrooms = MushroomsManager(session_manager=session_manager)
        self.friends = FriendsManager(session_manager=session_manager)

    def append_location_to_user(self, friend_id, location_id):
        with self.session.session() as s:
            location = s.query(self.locations.this_class).filter_by(id=location_id).one()
            user = s.query(self.users.this_class).filter_by(id=friend_id).one()
            user.loc_shared_with_me.append(location)
            s.add(user)
            s.commit()
        return True

    def delete_location_from_user(self, friend_id, location_id):
        with self.session.session() as s:
            location = s.query(self.locations.this_class).filter_by(id=location_id).one()
            user = s.query(self.users.this_class).filter_by(id=friend_id).one()
            if location in user.loc_shared_with_me:
                user.loc_shared_with_me.remove(location)
                s.add(user)
                s.commit()
        return True

    def fetch_locations_data(self,
                             owner_id: int = -999,
                             loc_fields_filters: dict = None,
                             shared_with_user_id: int = None):

        # TODO: optimize to not download the whole database
        # fetch all locations
        all_locations = self.locations.fetch_all_locations(filters=loc_fields_filters)

        # keep public locations + shared with me + owned by me
        public_locations = [x for x in all_locations if x.__dict__['czy_publiczna'] is True]

        # owned by the user
        owner_locations = [x for x in all_locations if x.owner_id == owner_id]

        # shared with user
        shared_locations = [x for x in all_locations
                            if shared_with_user_id in [_.__dict__['id'] for _ in x.__dict__['shared_with']]]

        # concatenate locations and reformat them
        i = public_locations[0]
        returned_locs = {}
        for privacy, i in list(zip_longest([], public_locations, fillvalue='public')) + \
                          list(zip_longest([], owner_locations, fillvalue='my_location')) + \
                          list(zip_longest([], shared_locations, fillvalue='shared_with_me')):
            loc_data = i.__dict__
            returned_locs[str(loc_data['id'])] = {
                'id': loc_data['id'],
                'location': {
                    'lng': loc_data['center_lon'],
                    'lat': loc_data['center_lat'],
                    'radius_in_meters': loc_data['radius_in_meters']
                },
                'Nazwa': loc_data['nazwa'],
                'Opis': loc_data['opis'],
                'Grzyby': [_.__dict__['nazwa_nieformalna'] for _ in loc_data['loc_mushrooms']],
                'Shared_by' : loc_data['owner'].__dict__['username'],
                "Shared_with": [{"id": _.__dict__['id'], "username": _.__dict__['username']} for _ in loc_data['shared_with']],
                'prywatnosc': privacy
            }
        return list(returned_locs.values())

    def fetch_mushrooms_data(self, imgs_folder_path: str = './static/images_mushrooms/', filters: dict = None):
        all_mushrooms = self.mushrooms.fetch_all_mushrooms(filters=filters)
        all_mushrooms_data = []
        for x in all_mushrooms:
            all_mushrooms_data.append({
                    'MushroomNameFormal'  : x.__dict__['nazwa_formalna'],
                    'MushroomNameInFormal': x.__dict__['nazwa_nieformalna'],
                    'MushroomInfo'        : json.loads(x.opis_cech_json),
                    # 'Dependencies'        : json.loads(x.warunki_wystepowania_json)
                    'Photos'              : ["".join([imgs_folder_path, x.strip()])
                                             for x in x.__dict__['photos_json'].split(',')],
                    'Toxic'               : x.__dict__['czy_trujacy'],
                    'Eatable'             : x.__dict__['czy_jadalny'],
                    'Protected' : x.__dict__['czy_chroniony'],
                    "MonthsAvailable"     : {
                        '1': x.__dict__['wystepuje_miesiac_01'],
                        '2': x.__dict__['wystepuje_miesiac_02'],
                        '3': x.__dict__['wystepuje_miesiac_03'],
                        '4': x.__dict__['wystepuje_miesiac_04'],
                        '5': x.__dict__['wystepuje_miesiac_05'],
                        '6': x.__dict__['wystepuje_miesiac_06'],
                        '7': x.__dict__['wystepuje_miesiac_07'],
                        '8': x.__dict__['wystepuje_miesiac_08'],
                        '9': x.__dict__['wystepuje_miesiac_09'],
                        '10': x.__dict__['wystepuje_miesiac_10'],
                        '11': x.__dict__['wystepuje_miesiac_11'],
                        '12': x.__dict__['wystepuje_miesiac_12']
                    }
            })
        return all_mushrooms_data

    def append_mushroom_to_location(self, location_id, mushroom_id):
        with self.session.session() as s:
            location = s.query(self.locations.this_class).filter_by(id=location_id).one()
            mushroom = s.query(self.mushrooms.this_class).filter_by(id=mushroom_id).one()
            location.loc_mushrooms.append(mushroom)
            s.add(location)
            s.commit()


def upload_to_database():
    import pandas as pd

    from sqlalchemy import create_engine
    from config import get_db_uri

    engine = create_engine(get_db_uri(), echo=True)

    db_manager = DatabaseSessionManager(db_engine=engine)
    db = DatabaseFacade(session_manager=db_manager)

    # Dodawanie uzytkownikow
    db.users.register_new_user(username='admin', password='admin', email='admin@e.pl')
    db.users.register_new_user(username='user1', password='user1', email='user1@e.pl')
    db.users.register_new_user(username='user2', password='user2', email='user2@e.pl')
    db.users.register_new_user(username='user_no_locations', password='alibaba', email='user_no_locations@e.pl')

    # Dodawanie znajomych
    db.friends.add_friend(**dict(friend1='admin', friend2='user2'))
    db.friends.add_friend(**dict(friend1='admin', friend2='user1'))
    db.friends.add_friend(**dict(friend1='user1', friend2='user3'))

    a = db.friends.fetch_friends(filters=dict(friend1='admin'))
    a = [{'id': x.__dict__['id'], 'username': x.__dict__['friend2']} for x in a]

    # Dodawanie grzybów
    grzyby = pd.read_excel('database/datafeed/datafeed.xlsx', keep_default_na=False, sheet_name='Grzyby')
    lokalizacje = pd.read_excel('database/datafeed/datafeed.xlsx', keep_default_na=False, sheet_name='Lokalizacje')
    lokalizacje = lokalizacje.loc[lokalizacje['nazwa'] != ""]

    cechy_grzybow = [
        "nazwa_formalna",
        "nazwa_nieformalna",
        "photos_json",
        "opis_cech_json",
        "warunki_wystepowania_json",
        "opis_objawow_zatrucia_json",
        "wystepuje_miesiac_01",
        "wystepuje_miesiac_02",
        "wystepuje_miesiac_03",
        "wystepuje_miesiac_04",
        "wystepuje_miesiac_05",
        "wystepuje_miesiac_06",
        "wystepuje_miesiac_07",
        "wystepuje_miesiac_08",
        "wystepuje_miesiac_09",
        "wystepuje_miesiac_10",
        "wystepuje_miesiac_11",
        "wystepuje_miesiac_12",
        "czy_trujacy",
        "czy_jadalny",
        "czy_chroniony"
    ]
    for i in ["nazwa_formalna",  "nazwa_nieformalna"]:
        grzyby[i] = grzyby[[i]].apply(lambda x: x.str.strip())

    for _, grzyb in grzyby.iterrows():
        db.mushrooms.add_new_mushroom(**grzyb.to_dict())

    # Sprawdzanie grzybów
    wszystkie_grzyby = db.fetch_mushrooms_data(imgs_folder_path='./static/images_mushrooms/')

    # Dodawanie lokalizacji
    for _, loc in lokalizacje.iterrows():

        # znajdujemy grzyby z danej lokalizacji
        grzyby_lokalizacji = []
        for grzyb in loc['grzyby'].strip().split(','):
            grzyb_obj = db.mushrooms.fetch_all_mushrooms(filters={'nazwa_nieformalna': grzyb.strip()})
            if grzyb_obj:
                grzyby_lokalizacji.append(grzyb_obj[0])

        loc = loc[['nazwa', 'opis', 'owner_id', 'czy_publiczna', 'center_lat', 'center_lon', 'radius_in_meters']]

        db.locations.add_location(**loc)
        curr_loc = db.locations.fetch_all_locations(filters={'nazwa': loc['nazwa']})
        curr_loc_id = curr_loc[0].__dict__['id']
        for i in grzyby_lokalizacji:
            db.append_mushroom_to_location(location_id=curr_loc_id, mushroom_id=i.__dict__['id'])

    # Wyswietlanie uzytkownikow
    db.users.fetch_all_users()

    # Wyswietlanie lokalizacje widoczne dla danego uzytkownika
    print(db.fetch_locations_data(owner_id=1))

    # Wyswietlanie wszystkich grzybow
    all_mushrooms_data = db.fetch_mushrooms_data()

    # ktore grzyby są obecnie w sezonie
    def fetch_mushrooms_availability(all_mushrooms_data):
        from datetime import date
        today_month = str(date.today().month)
        dataset = {}
        for x in all_mushrooms_data:
            dataset[x['MushroomNameInFormal']] = x['MonthsAvailable'][today_month]
        return dataset

    fetch_mushrooms_availability(all_mushrooms_data=all_mushrooms_data)

    # Sharowanie lokalizacji z innym uzytkownikiem
    friend1 = db.users.fetch_all_users(filters=dict(id=2))
    db.append_location_to_user(friend_id=2, location_id=1)

    db.fetch_locations_data(owner_id=2, shared_with_user_id=2)
    # db.delete_location_from_user(friend_id=2, location_id=1)

    # test usera
    db.users.fetch_all_users()


if __name__ == "__main__":
    upload_to_database()
