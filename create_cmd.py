#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python3.6


__date__ = '14:41 Dec 4 2019'
_doc__ = 'create dataset and cmd for VF3'


import sys
sys.path.insert(0, '../motif_adjacency/')

from datetime import datetime

from py3.graph.dataset import Dataset
from py3.graph.exampleloader import ExampleLoader

import networkx as nx, os


DATA_DIR = 'data/'
DATA_GRAPH = DATA_DIR + '/datagraph/'
QUERY_GRAPH = DATA_DIR + '/querygraph/'


def create_directory(dirpath):
    if not os.path.isdir(dirpath):
        print('create directory:', dirpath)
        os.makedirs(dirpath, exist_ok=True)


def save_graph(fpath, edgedict):
    nodeset = set(edgedict)
    for to_node in edgedict.values():
        for item in to_node:
            nodeset.add(item)
    nodelist = sorted(nodeset)
    bias = nodelist[0]
    create_directory(os.path.dirname(fpath))
    print('save graph:', fpath)
    with open(fpath, 'w', encoding='utf-8', newline='') as w:
        w.write('%s\n' % (len(nodelist)))
        for head in nodelist:
            w.write('%s %s\n' % (head - bias, 1))
        for head in nodelist:
            successors = sorted(edgedict.get(head, list()))
            w.write('%s\n' % (len(successors)))
            for tail in successors:
                w.write('%s %s\n' % (head - bias, tail - bias))


def datapath(name):
    return '%s/%s.grf' % (DATA_GRAPH, name)


def create_datagraph():
    # datagraph
    ds = Dataset()
    for name in ds:
        fpath = datapath(name)
        edgelist = ds.name2edgelist(name)
        edgedict = dict()
        for head, tail in edgelist:
            if head not in edgedict:
                edgedict[head] = set()
            edgedict[head].add(tail)
        save_graph(fpath, edgedict)


def querypath(querysize, label):
    return '%s/%s-%s.grf' % (QUERY_GRAPH, querysize, label)


def create_querygraph():
    # undirected querygraph
    fpath = querypath(3, 'path')
    edgedict = {
        0: [1],
        1: [0, 2],
        2: [1]
    }
    save_graph(fpath, edgedict)
    fpath = querypath(3, 'triangle')
    edgedict = {
        0: [1, 2],
        1: [0, 2],
        2: [0, 1]
    }
    save_graph(fpath, edgedict)
    # directed querygraph
    exampleloader = ExampleLoader()
    for querysize, label2graph in exampleloader.auto_example([3, 4]):
        for label, graph in label2graph.items():
            nodelist = sorted(graph.nodes)
            bias = nodelist[0]
            graph = graph.to_directed()
            fpath = querypath(querysize, label)
            create_directory(os.path.dirname(fpath))
            with open(fpath, 'w', encoding='utf-8', newline='') as w:
                w.write('%s\n' % (graph.number_of_nodes()))
                for head in nodelist:
                    w.write('%d %d\n' % (head - bias, 1))
                for head in nodelist:
                    successors = sorted(graph.successors(head))
                    w.write('%d\n' % (len(successors)))
                    for tail in successors:
                        w.write('%d %d\n' % (head - bias, tail - bias))


def write_cmd(w, dpath, querysize, label):
    qpath = '../%s' % (querypath(querysize, label))
    dpath = '../%s' % (dpath)
    w.write('${vf3lib} %s %s 0;\n' % (qpath, dpath))


def create_cmd():
    fpath = 'Debug/%s' % ('run_motif.sh')
    create_directory(os.path.dirname(fpath))
    exampleloader = ExampleLoader()
    with open(fpath, 'w', encoding='utf-8', newline='') as w:
        w.write('#!/bin/sh\n')
        w.write('# auto created: %s\n\n' % (datetime.now()))
        w.write('echo "running $BASH_SOURCE";\n\n')
        w.write('make clean && make;\n')
        w.write('vf3lib="./vf3lib.exe";\n')
        ds = Dataset()
        for name in ds:
            dpath = datapath(name)
            if ds.is_directed(name):
                for querysize, label2graph in exampleloader.auto_example([3]):
                    for label in label2graph:
                        write_cmd(w, dpath, querysize, label)
            else:
                for querysize, label in [(3, 'path'), (3, 'triangle')]:
                    write_cmd(w, dpath, querysize, label)
        for name in ds:
            dpath = datapath(name)
            if ds.is_directed(name):
                for querysize, label2graph in exampleloader.auto_example([4]):
                    for label in label2graph:
                        write_cmd(w, dpath, querysize, label)


def main():
    create_directory(DATA_DIR)
    create_datagraph()
    create_querygraph()
    create_cmd()


if __name__ == '__main__':
    main()
