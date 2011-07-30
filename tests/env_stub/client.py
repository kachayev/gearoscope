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
import gearman, time, string, random

def random_word(len):
    '''Generate sequence of random symbols of given length'''
    return ''.join([random.choice(string.letters) for x in range(len)])

def random_sum(elements, *args):
    '''
    Generate string representation of add operations. For example, "33+14+22+80".

    You can use as many elements in sequence as you want.
    Great number of arithmetic operations will emulate CPU loading from worker side
    '''
    return random_sequence('+', elements, *args)

def random_multiple(elements, *args):
    '''
    Generate string representation of add operations. For example, "33*14*22*80".

    You can use as many elements in sequence as you want.
    Great number of arithmetic operations will emulate CPU loading from worker side,
    but don't fogget, that result should be lest than maximum int value, to
    prevent problems with long types processing
    '''
    return random_sequence('*', elements, *args)

def random_sequence(delimiter, elements, *args):
    '''
    Generate sequence from random elements by given count of elements and delimiter
    '''
    return str(delimiter).join([str(random.randrange(*args)) for x in range(elements)])


# Create object of gearman client for pushing to server node tasks
# Gearman node connection params is taken from general settings module
# TODO: settings!
client = gearman.GearmanClient(['localhost:4730'])

while True:
    # TODO: settings!
    if random.random() > 0.5:
        # Add task for random word reversing
        # TODO: settings!
        word = random_word(30)
        client.submit_job('reverse', word, background=True)
        # TODO: logging!
        print 'Add reverse task for <%s>' % word

    # TODO: settings!
    if random.random() > 0.3:
        # Add task for calculating sum of 4 digits
        sum = random_sum(4, 0, 100)
        client.submit_job('sum', sum, background=True)
        # TODO: logging!
        print 'Add sum calculation task for <%s>' % sum

    # TODO: settings!
    if random.random() > 0.3:
        # Add task for calculating multiple of 2 digits
        # TODO: settings!
        multiple = random_multiple(2, 0, 100)
        client.submit_job('multiple', multiple, background=True)
        # TODO: logging!
        print 'Add multiple calculation task for <%s>' % multiple

    # TODO: settings!
    time.sleep(1.0)

