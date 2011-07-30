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
import time, string, random
import gearoscope.tests.settings as settings

from gearman import GearmanClient

def random_word(len):
    '''Generate sequence of random symbols of given length'''
    return ''.join([random.choice(string.letters) for x in range(len)])

def random_sum(elements, **kwargs):
    '''
    Generate string representation of add operations. For example, "33+14+22+80".

    You can use as many elements in sequence as you want.
    Great number of arithmetic operations will emulate CPU loading from worker side
    '''
    return random_sequence('+', elements, **kwargs)

def random_multiple(elements, **kwargs):
    '''
    Generate string representation of add operations. For example, "33*14*22*80".

    You can use as many elements in sequence as you want.
    Great number of arithmetic operations will emulate CPU loading from worker side,
    but don't fogget, that result should be lest than maximum int value, to
    prevent problems with long types processing
    '''
    return random_sequence('*', elements, **kwargs)

def random_sequence(delimiter, elements, randomizer=random.randrange, randomizer_args=[0,100], **kwargs):
    '''
    Generate sequence from random elements by given count of elements and delimiter

    Randomizer function can be changed from client code, for example in order
    to create pseudo-random sequence or something like this
    '''
    return str(delimiter).join([str(randomizer(*randomizer_args)) for x in range(elements)])


# Create object of gearman client for pushing to server node tasks
# Gearman node connection params is taken from general settings module
client = GearmanClient(settings.STUB_GEARMAN_NODES)

while True:
    if random.random() < settings.STUB_TASKS_PROBABILITY.get('reverse', 0.5):
        # Add task for random word reversing
        word = random_word(*settings.STUB_TASKS_ARGS.get('reverse', []))
        client.submit_job('reverse', word, background=True)
        # TODO: logging!
        print 'Add reverse task for <%s>' % word

    if random.random() < settings.STUB_TASKS_PROBABILITY.get('sum', 0.5):
        # Add task for calculating sum of 4 digits
        sum = random_sum(*settings.STUB_TASKS_ARGS.get('sum', []))
        client.submit_job('sum', sum, background=True)
        # TODO: logging!
        print 'Add sum calculation task for <%s>' % sum

    if random.random() < settings.STUB_TASKS_PROBABILITY.get('multiple', 0.5):
        # Add task for calculating multiple of 2 digits
        multiple = random_multiple(*settings.STUB_TASKS_ARGS.get('multiple', []))
        client.submit_job('multiple', multiple, background=True)
        # TODO: logging!
        print 'Add multiple calculation task for <%s>' % multiple

    time.sleep(settings.STUB_TASKS_FREQUENCY)

