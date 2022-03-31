import sys
import os
import logging
import random

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

import model
from database import create_postgre_connection_string


def add_hero(name, side=None, attribute=None, power=None, birthday=None):
    if side is None:
        side = random.choice(['dire', 'radiant'])
        logging.warning('Side was not specificated, randomly chosen %s', side)
    if attribute is None:
        attribute = random.choice(['Strength', 'Agility', 'Intelligence'])
        logging.warning('Attribute was not specificated, randomly chosen %s', attribute)
    if power is None:
        power = random.randint(1, 100)
        logging.warning('Power was not specificated, randomly chosen %s', power)
    
    with Session() as session:
        session.add(model.Heroes(side=side, birthday=birthday, name=name, attribute=attribute, power=power))
        session.commit()
    logging.info('Hero %s has been added for %s side', name, side)


def add_motto(hero_id, *motto):
    motto = ' '.join(motto)
    hero_has_motto = Session().query(model.Mottos).filter_by(hero_id=hero_id).count()
    if hero_has_motto:
        try:
            result = Session().execute(select(model.Mottos).where(model.Mottos.hero_id == hero_id).order_by(model.Mottos.motto_id.desc()))
            result = result.fetchone().Mottos.motto_id
        except AttributeError:
            logging.exception('There\'s no hero_id == %s in Heroes table', hero_id, exc_info=False)
            return
    else:
        result = 0
    motto_id = result + 1
    with Session() as session:
        session.add(model.Mottos(hero_id=hero_id, motto_id=motto_id, motto=motto))
        session.commit()
    logging.info('Motto for hero with id %s has been added', hero_id[0])


def print_row(table_name, id_):
    row = Session().query(getattr(model, table_name)).get(id_)
    print(row)


def add_fight():
    radiant_heroes = Session().execute(select(model.Heroes.id).where(model.Heroes.side == 'radiant')).fetchall()
    dire_heroes = Session().execute(select(model.Heroes.id).where(model.Heroes.side == 'dire')).fetchall()
    hero_1_id = random.choice(radiant_heroes)[0]
    hero_2_id = random.choice(dire_heroes)[0]
    try:
        hero_1_motto_id = random.choice(Session().execute(select(model.Mottos).where(model.Mottos.hero_id == hero_1_id)).fetchall()).Mottos.motto_id
    except IndexError:
        hero_1_motto_id = None
        logging.exception('Hero with id %i has no motto', hero_1_id, exc_info=False)
    try:
        hero_2_motto_id = random.choice(Session().execute(select(model.Mottos).where(model.Mottos.hero_id == hero_2_id)).fetchall()).Mottos.motto_id
    except IndexError:
        hero_2_motto_id = None
        logging.exception('Hero with id %i has no motto', hero_2_id, exc_info=False)

    power1 = Session().execute(select(model.Heroes.power).where(model.Heroes.id == hero_1_id)).fetchone().power
    power2 = Session().execute(select(model.Heroes.power).where(model.Heroes.id == hero_2_id)).fetchone().power
    power_difference = power2 - power1
    score = random.random() + power_difference / 100
    if score > 0.6:
        winner = 2
    elif score < 0.4:
        winner = 1
    else:
        winner = 0

    with Session() as session:
        session.add(model.Fights(
            hero_1_id = hero_1_id, 
            hero_2_id=hero_2_id, 
            hero_1_motto_id=hero_1_motto_id, 
            hero_2_motto_id=hero_2_motto_id, 
            winner=winner
        ))
        session.commit()
    logging.info('Fight between %i and %i took place. %i hero won.', hero_1_id, hero_2_id, winner)


def add_story(hero_id, *story):
    story = ' '.join(story)
    with Session() as session:
        session.add(model.HeroStories(hero_id=hero_id, story=story))
        session.commit() 
    logging.info('Story for hero with id %s added.', hero_id)


def delete_hero(hero_id):
    with Session() as session:
        hero = session.get(model.Heroes, hero_id)
        session.delete(hero)
        session.commit()
    logging.info('Hero with id %s deleted.', hero_id)


def setup_logging():
    def filter_draws(log_record):
        if log_record.funcName == 'add_fight' and log_record.args[-1] == 0:
            return 0
        return 1
        
    handler_to_console = logging.StreamHandler()
    handler_to_console.setLevel(logging.WARNING)
    logging.basicConfig(
        filename='logs.txt', 
        encoding='utf-8', 
        level=logging.DEBUG,
        format = '%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    root = logging.getLogger()
    root.addHandler(handler_to_console)
    root.addFilter(filter_draws)


def main():
    setup_logging()
    global Session
    engine = create_engine(url=create_postgre_connection_string())
    Session = sessionmaker(bind=engine)
    try:
        globals()[sys.argv[1]](*sys.argv[2:])
    except NameError:
        logging.exception('Function %s doesn\'t exist', sys.argv[1])
    except TypeError:
        logging.exception('Wrong number of arguments')
    except Exception:
        logging.exception('Base exception raised')


if __name__ == '__main__':
    main()
    