__doc__ = """
Tests package includes:

1. Custom unittest scenarious for testing dashboard processing
   with implemented JSON API mock responses and notification queues

2. Stub environment for gearman servers cluster with:
   -  daemon which generate several tasks and push it to queues
      (from time to time). this daemon can emulate for use
      runnig environment and prepare jobs for workers
   -  worker scripts per each stub task. you have only run this
      workers under daemonizing tool and it will periodicly ask
      gearman about new tasks in queue.

You can use any of external daemonizing tool for running env stub scripts,
but our advice is supervisor (so, we will prepare configuration for all scripts,
and you will get facilities to run environment just with adding configuration includes)
"""

