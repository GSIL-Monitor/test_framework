# encoding: utf-8

import os
import unittest

from utils import (log, extractor, config, file_reader, client, assertion,
                   support, generator, HTMLTestRunner, funny)


class TestLeader(object):

    def __init__(self, **kwargs):
        """initialize TestLeader.

        :param kwargs:
        """
        self.unittest_runner = unittest.TextTestRunner(**kwargs)
        self.test_loader = unittest.TestLoader()
        self.summary = None



