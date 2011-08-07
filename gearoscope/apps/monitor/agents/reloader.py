from sonar.loop import Sonar
from monitor.models import Revision

class RevisionCheckerAgent(object):
    '''
    Check database modification between daemon start moment and current

    If some information in database chande, we will get new revision ID.
    In this case we should send STOP signal to sonar object and all
    agent will be stoped in soft mode and sonar object will be
    rebuild with using new database configuration
    '''
    revision = None

    def __init__(self):
        self.revision = Revision.last.get()

    def work(self):
        '''Check last revision ID, if not equals reload sonar'''
        Revision.last.get()['id'] != self.revision['id']:
            Sonar.stop()

