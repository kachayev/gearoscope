### Introduction

Gearoscope is a gearman server monitoring and worker management system.

It provides both:

- monitoring daemon for logging information about server nodes state, gearman server nodes, existing queues and running workers

- convenient visual interface for managing server nodes, supervisor daemons and worker process across servers cluster

Gearoscope is designed with ideas of scalability in our minds.


### Install

1. Prepate all necessary environments:

- install and run gearman nodes on necessary servers

- install supervisor daemons for workers handling

2. Install and run monitor daemon and visual interface for managing it:

    wget -O gearoscope.tar.gz https://github.com/kachayev/gearoscope/tarball/master	
    tar xvzf gearoscope.tar.gz
    cd gearoscope
    pip install -e ./


### TODOs

- custom unique field for gearman model

- install section in documentation

- do not repeat name in server string representation if host and name are the same

- make inline proxy model for adding gearman node to server dynamically in server editing space

- custom validation for host in server's model

- help text for most fields in Worker Model
