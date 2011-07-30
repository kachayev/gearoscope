#!/usr/bin/env python

"""
sonard -- daemon process which use Sonar library for launching several monitoring agents in separated threads

Usage: %s [options]

Options:
-n --no-daemon  Do not use process daemonizing
-c --config     Path to configuration file
-p --pid-file   Path to daemon pid file
-v --verbose    Logging (verbosity) level
"""

from sonar import loop

from sonar.options import options
from sonar.agent import AgentPool
from sonar.remote import Server, pool as ServerPool

from sonar.agents.supervisor import SupervisorAgent, Supervisor

def sonar_factory():
    def make(options):
        '''
        Fabric function
        Should return Sonar object full ready for processing agents in infinity loop
        Get as argument special Options object, which handle data from configuration file
        and console line options and arguments.

        Fabric function will be called in loop each time, when external configuration file is changed
        '''
        import ConfigParser

        # Create sonar object
        s = loop.Sonar(options)

        # Iterate throw all configuration file in order to create
        # pool of servers and configurate all supervisor objects
        for section in options.config.sections():
            if section.find(':') != -1:
                block, name = section.split(':')
                block = block.lower()

                if block == 'server':
                    # Add server objects to server pool
                    params = {'name': name, 'password': None, 'user': 'root'}
                    params.update(dict(options.config.items(section)))

                    if 'is_default' in params.keys():
                        del(params['is_default'])

                    try:
                        is_default = options.config.getboolean(section, 'is_default')
                    except ConfigParser.NoOptionError:
                        is_default = False

                    ServerPool.add(Server(**params), is_default=is_default)
                elif block == 'pool':
                    params = {'count':1, 'timeout': 0}
                    params.update(dict(options.config.items(section)))

                    # Against string value of full class name for prototype,
                    # we should use class type from imported related module
                    if params['prototype'].find('.') != -1:
                        parts  = params['prototype'].split('.')
                        module = __import__(parts[0])
                        params['prototype'] = reduce(lambda x,y: getattr(x,y), parts[1:], module)
                    else:
                        params['prototype'] = globals()[params['prototype']]

                    # Count should be integer in any case
                    params['count'] = int(params['count'])

                    # Create agent pool with given name, which will consist from
                    # given count of object, builded on as instance of prototype class
                    s.add_pool(name, AgentPool(**params))
                elif block == 'supervisor':
                    s.add_agent(SupervisorAgent(Supervisor(server=ServerPool.get('local'), port=9001),
                                                names=['multiple', 'reverse', 'sum']))

        return s
    return make

if __name__ == '__main__':
    loop.main(factory=sonar_factory())

