#!/usr/bin/python3
#  -*- coding: utf-8 -*-

from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork

import signify_base as base


def create_training_set():
    dataset = SupervisedDataSet(25, 1)
    test_sample_file = open('test.txt').readlines()
    for i in range(0, 50):
        dataset.addSample(tuple(base.get_from_base(test_sample_file[i])['res']), tuple(i)) # на выход даем ему индекс слова
    return dataset


if __name__ == "__main__":
    net = buildNetwork(25, 5, 1)
    dataset = create_training_set()
    trainer = BackpropTrainer(net, dataset)
    print(trainer.trainUntilConvergence())
