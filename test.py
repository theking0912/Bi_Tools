#! /usr/bin/env python
# -*- coding: utf-8 -*-
from getaddress.utils import hanadb

if __name__ == "__main__":
    print(hanadb.typeof('v'))
    if type('asdfasdf') == str:
        print('asdf')