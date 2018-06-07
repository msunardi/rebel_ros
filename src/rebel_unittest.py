#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 31 09:57:56 2018

@author: mathias
"""

import unittest
import robel_parser as rp

import makana_jimmy_program as mjp

import rebel_server as rs

#vocab = mjp.position_library
#vocab['yes'] = '(& yes_1 yes_2 yes_3 stand)'
#vocab['wow'] = '(& wow_1 wow_2 wow_3 wow_4 stand)'
#vocab['alas2'] = '(& alas_2_0 alas_2_1 alas_2_2 alas_2_3 alas_2_4 alas_2_5 alas_2_6 stand)'
vocab = rs.vocab

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
        self.assertEquals(rp.parsex('(| a b c)'), 'a|b|c;')

    def test_parsex_merge(self):
        self.assertEquals(rp.parsex('(~ a b c)'), 'a~b~c;')
        
    def test_parsex_multiple_merge(self):
        self.assertEquals(rp.parsex('(& (~ a b) (~ c d))'), 'a~b; c~d;')
        
    def test_merge_processing(self):
        merge = rp.parsex('(& (~ a b) (~ c d))')
        print(merge)
        self.assertEquals(rp.merge_processing(merge, None), ['a~b', 'c~d'])
        
    def test_merge_processing_motion(self):
#        rp.DEBUG = True
        rp.ap.DEBUG = True
#        merge = rp.parsex('(~ alas2 wow yes)')
        merge = rp.parsex('(~ leila_dances muscle_combo_2)')
#        print(merge)
        merge_processed = rp.merge_processing(merge, vocab, joints=['HEAD_TILT'])
#        self.assertEquals(merge_processed, ['alas2~wow~yes'])
        self.assertTrue(len(merge_processed) > 0)

if __name__ == "__main__":
#    rp.DEBUG = True
    unittest.main()