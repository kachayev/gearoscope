#!/usr/bin/env python

"""
Works in infinity loop and periodicly generate
stupid tasks and push it to gearman server

Usage: ./client [options]

List of generated tasks:
1. `reverse` - push word of random length to workload
2. `sum` - push to workload string representation of add operator (for example, `34+15+12`)
3. `multiple` - push to workload string representation of multiple operator (for example, `34*15*2`)

To prevent situation when all queues will have the same load
and give user oppurtunities to see on monitor different graphics for each queue,
generator will add each task randomly.

Gearman node for test runner and frequency of tasks generation
can be set via general settings.py
"""

