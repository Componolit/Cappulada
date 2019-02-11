#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
if __name__ == '__main__':
    sys.path.append (".")

import unittest
from capdpa import *
from capdpa_test import *

class IR_Test(Capdpa_Test):

    def test_root(self):
        const = Constant(name="K", value=1)
        tree = Namespace(name="N", children=[
            Class(name="C", children=[
                Enum(name="E", children=[const])])])
        self.check(const.GetRoot(), tree)
        self.check(id(const.GetRoot()), id(tree))

    def test_getitem(self):
        const = Constant(name="K", value=1)
        tree = Namespace(name="N", children=[
            Class(name="C", children=[
                Enum(name="E", children=[const])])])
        self.check(tree["C"]["E"]["K"], const)
        self.check(id(tree["C"]["E"]["K"]), id(const))

    def test_getitem_tuple(self):
        const = Constant(name="K", value=1)
        tree = Namespace(name="N", children=[
            Class(name="C", children=[
                Enum(name="E", children=[const])])])
        self.check(tree["C"]["E"]["K"], const)
        self.check(id(tree["C", "E", "K"]), id(const))

    def test_getitem_list(self):
        const = Constant(name="K", value=1)
        tree = Namespace(name="N", children=[
            Class(name="C", children=[
                Enum(name="E", children=[const])])])
        self.check(tree["C"]["E"]["K"], const)
        self.check(id(tree[["C", "E", "K"]]), id(const))

    def test_getitem_keyerror(self):
        tree = Namespace(name="X");
        def get(var):
            return tree[var]
        self.assertRaises(KeyError, get, (1,2))

    def test_fqn(self):
        const = Constant(name="K", value=1)
        tree = Namespace(name="N", children=[
            Class(name="C", children=[
                Enum(name="E", children=[const])])])
        self.check(const.FullyQualifiedName(), ["N", "C", "E", "K"])

    def test_contains(self):
        const = Constant(name="K", value=1)
        tree = Namespace(name="N", children=[
            Class(name="C", children=[
                Enum(name="E", children=[const])])])
        self.check("K" in tree, False)
        self.check("C" in tree, True)

    def test_contains_list(self):
        const = Constant(name="K", value=1)
        tree = Namespace(name="N", children=[
            Class(name="C", children=[
                Enum(name="E", children=[const])])])
        self.check(["C", "E", "K"] in tree, True)
        self.check(["C"] in tree, True)
        self.check(["C", "F"] in tree, False)

    def test_contains_tuple(self):
        const = Constant(name="K", value=1)
        tree = Namespace(name="N", children=[
            Class(name="C", children=[
                Enum(name="E", children=[const])])])
        self.check(("C", "E", "K") in tree, True)
        self.check(("C") in tree, True)
        self.check(("C", "F") in tree, False)

if __name__ == '__main__':
    unittest.main()
