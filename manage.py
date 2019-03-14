from flask_script import Manager
from project import app
manager = Manager(app)

import sys
print(sys.path)

if __name__ == '__main__':
    manager.run()