#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 31 09:57:56 2018

@author: mathias
"""

import unittest
import robel_parser as rp

class TestParser(unittest.TestCase):
    
    def test_parsex(self):
        self.assertEquals(rp.parsex('a'), 'a')
        
    def test_parsex_concatenate(self):
        self.assertEquals(rp.parsex('(& a b)'), 'a b')
    
    def test_parsex_union(self):
        self.assertTrue(rp.parsex('(+ a b c d)') in ['a', 'b', 'c', 'd'])
        
    def test_parsex_repetition(self):
        for i in range(10):
            rep = rp.parsex('(* a 2.5)')
            self.assertTrue(len(rep.split()) >= 2)
        
    def test_parsex_concurrent(self):
        self.assertEquals(rp.parsex('(| a b c)'), 'a | b | c ;')
        
if __name__ == "__main__":
#    rp.DEBUG = True
    unittest.main()