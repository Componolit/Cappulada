# -*- coding: utf-8 -*-

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

    def test_fqn(self):
        const = Constant(name="K", value=1)
        tree = Namespace(name="N", children=[
            Class(name="C", children=[
                Enum(name="E", children=[const])])])
        self.check(const.FullyQualifiedName(), ["N", "C", "E", "K"])
