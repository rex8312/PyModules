# -*- coding: utf-8 -*-

__author__ = 'rex8312'

import numpy as np


class BaseSelector(object):
    def __init__(self):
        self.params = None
        self.values = None

    def set_params(self, params, values):
        if params is None or values is None:
            raise Exception("params or values are not set")
        self.params = np.array(params)
        self.values = np.array(values)

    def select(self, n=1):
        raise NotImplementedError()


if __name__ == '__main__':
    selector = BaseSelector()
    print selector.select()