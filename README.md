### Attention

This software currently is under active development. So, if you have idea to use it for production, please wait until first stable tag. Short roadmap:

- changing policy for more flexible monitoring daemon configuration

- working with servers in cluster (pings, stat information, notifications)

- searching gearman daemons on standard ports and installing it on remote machines

- normal processing of workers management

- facilities to view logs on special dashboard panel

- signal system for monitored queues

- many small enhancements


### Introduction

Gearoscope is a gearman server monitoring and worker management system.

It provides both:

- monitoring daemon for logging information about server nodes state, gearman server nodes, existing queues and running workers

- convenient visual interface for managing server nodes, supervisor daemons and worker process across servers cluster

Gearoscope is designed with ideas of scalability in our minds.

### Demo

View application [demo](http://codemehanika.org/gearoscope/)

To enter admin panel, you can use this credentials:

    user: gear
    pass: scope

Pls, do not change many params, cause monitoring logger would not show interesting information for unknown host, unresolved sockets etc :)

### License

See LICENSE.txt for more information

### Install

Prepate all necessary environments:

- install and run gearman nodes on necessary servers

- install supervisor daemons for workers handling

Install and run monitor daemon and visual interface for managing it:

    wget -O gearoscope.tar.gz https://github.com/kachayev/gearoscope/tarball/master
    tar xvzf gearoscope.tar.gz
    cd gearoscope
    pip install -e ./

More information will be available soon.

### TODOs

- custom unique field for gearman model

- install section in documentation

- do not repeat name in server string representation if host and name are the same

- make inline proxy model for adding gearman node to server dynamically in server editing space

- custom validation for host in server's model

- help text for most fields in Worker Model

