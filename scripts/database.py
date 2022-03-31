import random
import json
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData, DropConstraint
from faker import Faker

import model


def drop_and_create_database():
    metadata = MetaData(engine)
    metadata.reflect()
    for table in metadata.tables.values():
        for fk in table.foreign_keys:
            engine.execute(DropConstraint(fk.constraint))
    metadata.drop_all()
    print('\nDATABASE DROPPED\n')
    model.Base.metadata.create_all(engine)


def fill_database():
    fake = Faker()
    Session = sessionmaker(bind=engine)
    id_counter = 1

    with open('../data/heroes.json', 'r') as f:
        heroes = json.load(f)

    with Session() as session:
        for hero_name, hero_attributes in heroes.items():
            session.add(model.Heroes(side=hero_attributes['side'], birthday=fake.date_object(), name=hero_name, attribute=hero_attributes['attribute'], power=hero_attributes['power']))
            session.add(model.Mottos(hero_id=id_counter, motto_id=1, motto=' '.join([hero_name, 'is the best'])))
            if random.random() < 0.3:
                session.add(model.Mottos(hero_id=id_counter, motto_id=2, motto=' '.join([hero_name, 'is the strongest'])))
            session.add(model.HeroStories(hero_id=id_counter, story=hero_attributes['bio']))
            id_counter += 1
        session.commit()


def main():
    drop_and_create_database()
    fill_database()


def create_postgre_connection_string():
    db_name = os.getenv('POSTGRES_DB')
    db_user = os.getenv('POSTGRES_USER')
    db_password = os.getenv('POSTGRES_PASSWORD')
    connection_string = ''.join(['postgresql://', db_user, ':', db_password, '@db:5432/', db_name])
    return connection_string


if __name__ == '__main__' and os.getenv('DATABASE_MODE') == 'dev':
    engine = create_engine(url=create_postgre_connection_string())
    main()
