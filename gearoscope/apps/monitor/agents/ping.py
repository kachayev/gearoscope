"""
Imlementation of sonar agent for pinging remove servers
and logging information about running status

Each of this agent will act in scope of general "ping" pooll,
in order to provide some trafeoff between fast responsein
multi-threading model, and using system resources for hanling
many separate threads.
"""

