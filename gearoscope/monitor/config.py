from ConfigParser import ConfigParser

class Rewriter(object):
    def __init__(self, path):
        self.path = path

    def rebuild(self, section=None, values=None):
        self.config = ConfigParser(allow_no_value=True).read(path)

        # Remove all editable section from configuration
        if section not in self.config.sections():
            self.config.add_section(section)

        # Set new values for each configuration item
        for item, value in values.iteritems():
            self.config.set(section, item, value, 1)

        return self

