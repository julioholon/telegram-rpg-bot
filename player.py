from google.cloud import datastore
import config

# CONSTANTS
STATE_CHAT = 0
STATE_CREATE_CHAR = 10

class Player:
    id = 0
    name = ""
    state = STATE_CHAT

    def __init__(self, id):
        ds = datastore.Client(config.PROJECT_ID)
        key = ds.key(self.__class__.__name__, int(id))
        results = ds.get(key)
        if len(results):
            ent = results.pop()
            ent['id'] = id

            self.id = id
            self.name = ent['name']
            self.state = ent['state']

    def __init__(self, id=None, name, state)
        ds = datastore.Client(config.PROJECT_ID)
        key = ds.key(self.__class__.__name__ , int(id))
        if id:
            key = ds.key(self.__class__.__name__, int(id))
        else:
            key = ds.key(self.__class__.__name__)

        entity = datastore.Entity(key=key)
        entity.update({
                'name': name,
                'state': state
                })
        ds.put(entity)

        self.id = id
        self.name = name
        self.state = state

    def message_from_self(self, message):
        return u"You say: \"{}\"".format(message)

    def message_from(self, message):
        return u"{} says: \"{}\"".format(self.name, message)
