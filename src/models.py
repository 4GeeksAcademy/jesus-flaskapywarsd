from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column, Mapped,relationship
from sqlalchemy import Integer, String, ForeignKey

db = SQLAlchemy()

# model user  unico
class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    password: Mapped[str] = mapped_column(String(80))
    is_active: Mapped[bool]


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }
    

    # model charactesrs  unico
class Characters(db.Model):
    __tablename__ = 'characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    race: Mapped[str] = mapped_column(nullable=True)
    age: Mapped[str] = mapped_column(nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "race": self.race,
            "age" : self.age
            # do not serialize the password, its a security breach
        }


# model planets  unico
class Planets(db.Model):
    __tablename__ = 'planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    climate: Mapped[str]
    url: Mapped[str] = mapped_column(nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "url" : self.url
            # do not serialize the password, its a security breach
        }

# model favoritos charac  
class Favorite_characters(db.Model):
    __tablename__ = 'favorite_characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    character_id: Mapped[int] = mapped_column(ForeignKey('characters.id'))

    def serialize(self):
        return {
            "id": self.id
        }
    
# model favplanets  
class Favorite_planets(db.Model):
    __tablename__ = 'favorite_planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    planets_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))

    def serialize(self):
        planets= db.session.execute(db.select(Planets).filter.by(id=self.planets_id)).scalar.one()
        return {
            "id": self.id,
            "planets" : planets.serialize()
        }