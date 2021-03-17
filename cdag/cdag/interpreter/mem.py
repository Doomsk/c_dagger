

#mem1 = {}
#count_mem1 = 0
#pointer1 = {}
#code_info = {}


class CountMem1:
    def __init__(self, val=0):
        self._q = int(val)

    def __iadd__(self, val):
        self._q += val
        return self

    def __add__(self, val):
        if isinstance(val, CountMem1):
            return CountMem1(self._q + val._q)
        return self._q + val

    def __str__(self):
        return str(self._q)

    def inc(self):
        self._q += 1
        return self


class CodeInfo(dict):
    __slots__ = ()


class Pointer(dict):
    __slots__ = ()


class Mem1(dict):
    __slots__ = ()

