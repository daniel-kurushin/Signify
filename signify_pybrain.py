#!/usr/bin/python3
#  -*- coding: utf-8 -*-

# from pybrain.structure import TanhLayer
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.customxml.networkreader import NetworkReader
from pybrain.tools.customxml.networkwriter import NetworkWriter
from pybrain.tools.shortcuts import *

import signify_base as base


def create_training_set(word_count = 10):
    dataset = SupervisedDataSet(25, word_count)
    test_sample_file = open('test.txt').readlines()
    for i in range(0, word_count):
        print(test_sample_file[i][:-1])
        out = []
        for t in range(0, word_count):
            out.append(0)
        out[i] = 1
        inp = list(base.get_from_base(test_sample_file[i][:-1])['res'])
        # for f in range(0, len(inp)):
        #     inp[f] *= 0.24
        #     inp[f] -= 0.2
        dataset.addSample(tuple(inp), tuple(out))
        print(inp)
        print(out)
    print(dataset)
    return dataset


if __name__ == "__main__":
    net = buildNetwork(25, 5, 10)
    net.sortModules()
    while True:
        command = input('>').split(' ')
        if command[0] == 'save':
            NetworkWriter.writeToFile(net, 'signify_net_dump.xml')
        if command[0] == 'load':
            net = NetworkReader.readFrom('signify_net_dump.xml')
        if command[0] == 'train':
            if len(command) > 1:
                dataset = create_training_set(int(command[1]))
            else:
                dataset = create_training_set()
            trainer = BackpropTrainer(net, dataset)
            # epochs = 1000
            # if len(command) > 2:
            #     epochs = int(command[2])
            # for j in range(0, epochs):
            #     print(trainer.train())
            print(trainer.trainUntilConvergence())
        if command[0] == 'test':
            print(net.activate(base.get_from_base(command[1])['res']))
        if command[0] == 'exit':
            exit(0)




