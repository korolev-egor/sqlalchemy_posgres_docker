from sqlalchemy import Table, Column, Integer, String,  DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base


MAXIMUM_BIO_LENGTH = 2500
Base = declarative_base()


association_table = Table('association', Base.metadata,
    Column('heroes_id', ForeignKey('heroes.id'), primary_key=True),
    Column('fights_id', ForeignKey('fights.id'), primary_key=True)
)


class Heroes(Base):
    __tablename__ = 'heroes'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    side = Column(String(30))
    name = Column(String(30))
    birthday = Column(DateTime(timezone=True))
    attribute = Column(String(15))
    power = Column(Integer)

    mottos = relationship('Mottos', backref='heroes', cascade='all, delete-orphan')
    stories = relationship('HeroStories', backref='heroes', cascade='all, delete-orphan', uselist=False)
    fights = relationship('Fights', secondary=association_table, back_populates='heroes')
    
    def __repr__(self):
        return f'{self.id}: {self.name}'


class Fights(Base):
    __tablename__ = 'fights'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    hero_1_id = Column(Integer)
    hero_2_id = Column(Integer)
    hero_1_motto_id = Column(Integer)
    hero_2_motto_id = Column(Integer)
    heroes = relationship(
        'Heroes', 
        secondary=association_table,
        back_populates='fights'
    )
    winner = Column(Integer)

    def __repr__(self):
        return f'{self.id}: {self.hero_1_id} vs {self.hero_2_id}. Winner = {self.winner}'


class Mottos(Base):
    __tablename__ = 'mottos'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    hero_id = Column(Integer, ForeignKey('heroes.id'))
    motto_id = Column(Integer)
    motto = Column(String(50))

    def __repr__(self):
        return f'{self.id}: hero_id = {self.hero_id}, motto_id = {self.motto_id}'


class HeroStories(Base):
    __tablename__ = 'herostories'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    hero_id = Column(Integer, ForeignKey('heroes.id'))
    story = Column(String(MAXIMUM_BIO_LENGTH))

    def repr(self):
        return f'{self.id}: hero_id = {self.hero_id}'
