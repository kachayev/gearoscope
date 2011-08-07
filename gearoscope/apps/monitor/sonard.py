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
from sonar.logger import Log

from sonar.agents.supervisor import SupervisorAgent, Supervisor
from agents.gearmand import GearmanNodeAgent
from agents.pingator import PingAgent

import scoper
from django.conf import settings

def sonar_factory():
    def make(options):
        '''
        Fabric function
        Should return Sonar object full ready for processing agents in infinity loop
        Get as argument special Options object, which handle data from configuration file
        and console line options and arguments.

        Fabric function will be called in loop each time, when external configuration file is changed
        '''

        # Create sonar object
        s = loop.Sonar(options)

        # Create server pool with using information stored in database
        for server in scoper.models.Server.objects.all():
            ServerPool.add(Server(**server.__dict__))

            # Add special Pingator agent, which will periodicaly ping
            # server with using subprocess PIPE and log information
            # both about server availability and average response time
            s.add_agent(PingAgent(ServerPool.get(server.name), settings.SONAR_PINGATOR_RETRIES))

        # Create Supervisor agents with using information from database
        for visor in scoper.models.Supervisor.objects.all():
            names = ','.join([worker.name for worker in scoper.models.Worker.objects.filter(supervisor=visor)])
            visor = Supervisor(server=ServerPool.get(visor.server.name), port=visor.port)

            # Add supervisor object and related to it supervisor agent,
            # which will periodicaly call supervisor XML-RPC in order to get informations
            # about running processes according to <names> or <groups> listings
            s.add_agent(SupervisorAgent(visor), names=names)

        # Create Gearman agents with using information from database
        for node in scoper.models.Gearman.objects.all():
            # Add gearman node object and related , which will
            # periodicaly call gearman-admin util via socket interface
            # in order to get informations about node status and queues
            s.add_agent(GearmanNodeAgent(server=ServerPool.get(node.server.name), port=node.port))

        # Create all pools disribed in setting.py module
        for name, pool in settings.SONAR_AGENT_POOLS.iteritems():
            # Against string value of full class name for prototype,
            # we should use class type from imported related module
            if pool['prototype'].find('.') != -1:
                parts = pool['prototype'].split('.')
                pool['prototype'] = reduce(lambda module,attr: getattr(module,attr),
                                            parts[1:], __import__(parts[0]))
            else:
                pool['prototype'] = globals()[pool['prototype']]

            # Create agent pool with given name, which will consist from
            # given count of object, builded on as instance of prototype class
            s.add_pool(name, AgentPool(**pool))

        return s
    return make

if __name__ == '__main__':
    Log.BUFFER_FILE = settings.SONAR_CONFIGURATION_FILE
    loop.main(factory=sonar_factory())

