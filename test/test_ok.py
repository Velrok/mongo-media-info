from nose.tools import *
from mongo_media_info import *


def test_ok():
    eq_(a(), 1)
