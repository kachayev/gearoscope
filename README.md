### Introduction

Gearoscope is a gearman server monitoring and worker management system.

It provides both:

- monitoring daemon for loggging information about server nodes state, gearman server nodes, existen queues and running workers

- convenient visual interface for managing server nodes, supervisor daemons and worker process across servers cluster

Gearoscope is designed with ideas of scalability in our minds.


### Install

1. Download tar file
2. Run `pip install -e ./`
3. Add `include` directives to supervisor configuration and run supervisor daemon (or restart). This will launch two process: sonard.py monitoring system and django http server for dashboard viewing and servers configuration management.

### TODOs

- custom unique field for gearmand model

- install section in documentation

- do not repeat name in server string representation if host and name are the same

- make inline proxy model for adding gearman node to server dinamicly in server editing space

- custom validation for host in server's model
