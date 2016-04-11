from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Catalog, Item, Base
engine = create_engine('sqlite:///catalogitemwithuser.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

catalog1 = Catalog(name="Soccer")

session.add(catalog1)
session.commit()

item1 = Item(title="Jersey", description="Jersey Description", catalog=catalog1)
session.add(item1)
session.commit()

catalog2 = Catalog(name="Basketball")

session.add(catalog2)
session.commit()

catalog3 = Catalog(name="Baseball")

session.add(catalog3)
session.commit()

catalog4 = Catalog(name="Frisee")

session.add(catalog4)
session.commit()

catalog5 = Catalog(name="Snowboarding")

session.add(catalog5)
session.commit()

catalog6 = Catalog(name="Rock Climbing")

session.add(catalog6)
session.commit()

catalog7 = Catalog(name="Foosball")

session.add(catalog7)
session.commit()


catalog8 = Catalog(name="Skating")

session.add(catalog8)
session.commit()

catalog9 = Catalog(name="Hockey")

session.add(catalog9)
session.commit()


print "added catalog items!"