from ConfigParser import ConfigParser
from django.conf import settings

class Rewriter(object):
    def __init__(self, path=None):
        self.path = path or settings.SONAR_CONFIGURATION_FILE

    def rebuild(self, section=None, values=None):
        self.config = ConfigParser(allow_no_value=True)
        self.config.read(self.path)

        # Remove all editable section from configuration
        if section not in self.config.sections():
            self.config.add_section(section)

        # Set new values for each configuration item
        for item, value in values.iteritems():
            self.config.set(section, item, value)

        return self

