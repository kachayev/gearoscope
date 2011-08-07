from sonar.loop import Sonar

class RevisionCheckerAgent(object):
    '''
    Check database modification between daemon start moment and current

    If some information in database chande, we will get new revision ID.
    In this case we should send STOP signal to sonar object and all
    agent will be stoped in soft mode and sonar object will be
    rebuild with using new database configuration
    '''
    # Initial revision ID
    revision = None

    # Manager for working with revision objects
    manager = None

    def __init__(self, manager=None):
        '''Initialize manager object and retriew current revision ID'''
        self.manager  = manager
        self.revision = manager.get()['id']

    def work(self):
        '''Check last revision ID, if not equals reload sonar'''
        self.manager.get()['id'] != self.revision:
            Sonar.stop()

