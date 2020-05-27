from os import path
import json

# from leanda.api import nodes


class Session():
    path = '{}/.leanda.json'.format(path.expanduser('~'))

    token: str
    owner: str
    cwd: str
    user: {}

    def __getattribute__(self, name):
        if name in dir(Session):
            return super().__getattribute__(name)
        return self.load().get(name, None)

    def __setattr__(self, name, value):
        self.update({name: value})
        return super().__setattr__(name, value)

    def save(self, session):
        with open(self.path, 'w') as f:
            json.dump(session, f, indent=4)

    def update(self, session_params):
        if path.exists(self.path):
            session = self.load()
        else:
            session = {}
        session.update(session_params)
        self.save(session)

    def load(self):
        if path.exists(self.path):
            with open(self.path, 'r') as f:
                return json.load(f)
        else:
            print('The last session not found')
            return {'token': '', 'cwd': '', 'owner': '', }


session = Session()
