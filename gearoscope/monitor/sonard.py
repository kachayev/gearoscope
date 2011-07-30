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

from sonar.agents.process import ProcessStatAgent
from sonar.agents.supervisor import SupervisorAgent, Supervisor

def sonar_factory():
    def make(options):
        import ConfigParser

        # Iterate throw all configuration file in order to create
        # pool of servers and configurate all supervisor objects
        for section in options.config.sections():
            if section.find(':') != -1:
                block, name = section.split(':')

                # Add server objects to server pool
                if block.lower() == 'server':
                    params = {'name': name, 'password': None, 'user': 'root'}
                    params.update(dict(options.config.items(section)))

                    if 'is_default' in params.keys():
                        del(params['is_default'])

                    try:
                        is_default = options.config.getboolean(section, 'is_default')
                    except ConfigParser.NoOptionError:
                        is_default = False

                    ServerPool.add(Server(**params), is_default=is_default)

        s = loop.Sonar(options)
        s.add_pool('stat', AgentPool(prototype=ProcessStatAgent, count=3, timeout=0))
        s.add_agent(SupervisorAgent(Supervisor(server=ServerPool.get('local'), port=9001),
                                    names=['gearman', 'multiple', 'reverse', 'sum']))

        return s
    return make

if __name__ == '__main__':
    loop.main(factory=sonar_factory())

