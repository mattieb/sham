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


import time
import weakref


"""test doubles"""


# data on all sham shenanigans goes here
_d = weakref.WeakKeyDictionary()


class LogEntry(object):
    """superclass for log entries"""

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class CallLogEntry(LogEntry):
    """log entry for a call"""

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        LogEntry.__init__(self)


    def reprArgs(self):
        return ', '.join([repr(arg) for arg in self.args])


    def reprKwArgs(self):
        return ', '.join(['%s=%r' % item
                          for item in sorted(self.kwargs.items())])


    def reprCallSignature(self):
        reprs = [r for r in [self.reprArgs(), self.reprKwArgs()] if r]
        return ', '.join(reprs)


    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.reprCallSignature())


class GetAttrLogEntry(LogEntry):
    """log entry for an attribute get"""

    def __init__(self, name):
        self.name = name
        LogEntry.__init__(self)


    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.name)


def _log(sham, entry):
    _d[sham]['log'].append((time.time(), entry))


class Sham(object):
    """test double"""


    def __init__(self):
        _d[self] = {'attr': {}, 'log': []}


    def __call__(self, *args, **kwargs):
        _log(self, CallLogEntry(*args, **kwargs))
        try:
            return _d[self]['return']
        except KeyError:
            retval = _d[self]['return'] = Sham()
            return retval


    def __getattr__(self, name):
        """attribute lookup"""

        _log(self, GetAttrLogEntry(name))
        attr = _d[self]['attr']
        try:
            return attr[name]
        except KeyError:
            sham = attr[name] = Sham()
            return sham


def getLog(sham):
    return _d[sham]['log']


def filterLog(sham, cls):
    return [entry for entry in getLog(sham) if isinstance(entry[1], cls)]


def assertCallCount(sham, count):
    """assert we were called exactly n times"""

    log_count = len(filterLog(sham, CallLogEntry))
    assert count == log_count, '%d == %d' % (count, log_count)


def assertCalledWith(sham, *args, **kwargs):
    """assert we were called at least once with these args"""

    match_entry = CallLogEntry(*args, **kwargs)
    # We could use any() in Python 2.5+, but this gives us 2.4 compat
    for call in filterLog(sham, CallLogEntry):
        if call[1] == match_entry:
            return
    raise AssertionError(repr(match_entry))


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
