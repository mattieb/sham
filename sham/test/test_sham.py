# Copyright (c) 2013 Matt Behrens.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import unittest

import sham; Sham = sham.Sham


"""tests for sham"""


class ShamTestCase(unittest.TestCase):
    """test case for sham"""


    def test_getattr(self):
        """getattr is working correctly"""

        s = Sham()
        foo = s.foo
        self.assertIs(foo, s.foo)
        self.assertIs(foo, getattr(s, 'foo'))
        gets = sham.filterLog(s, sham.GetAttrLogEntry)
        self.assertEqual(len(gets), 3)
        get = gets[0][1]
        self.assertEqual(get, sham.GetAttrLogEntry('foo'))
        self.assertEqual(repr(get), "<GetAttrLogEntry 'foo'>")


    def test_callLog(self):
        """calls appear in the log"""

        s = Sham()
        s(True, foo='bar')
        calls = sham.filterLog(s, sham.CallLogEntry)
        self.assertEqual(len(calls), 1)
        call = calls[0][1]
        self.assertEqual(call, sham.CallLogEntry((True,), {'foo': 'bar'}))
        self.assertEqual(repr(call), "<CallLogEntry True, foo='bar'>")


    def test_callCount(self):
        """number of times called"""

        s = Sham()
        sham.assertCallCount(s, 0)
        self.assertRaises(AssertionError, sham.assertCallCount, s, 1)

        s()
        sham.assertCallCount(s, 1)
        self.assertRaises(AssertionError, sham.assertCallCount, s, 2)

        s.foo()
        sham.assertCallCount(s, 1)
        self.assertRaises(AssertionError, sham.assertCallCount, s, 2)
        sham.assertCallCount(s.foo, 1)
        self.assertRaises(AssertionError, sham.assertCallCount, s.foo, 2)


    def test_callArgs(self):
        """assert call arguments"""

        s = Sham()

        s(True, foo='bar')
        sham.assertCalledWith(s, True, foo='bar')
        self.assertRaises(AssertionError, sham.assertCalledWith, s, 42, a='b')

        s(False, baz='quux')
        sham.assertCalledWith(s, True, foo='bar')
        sham.assertCalledWith(s, False, baz='quux')
        self.assertRaises(AssertionError, sham.assertCalledWith, s, 42, a='b')


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
