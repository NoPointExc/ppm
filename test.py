#!/usr/bin/python

import unittest
import sys
from player import *

class TestPlayer(unittest.TestCase):
    # [four-bits][next-random][code-digit]
        
    def setUp(self):
        self.monkey = Player(0, "monkey")

    def test_make_decision(self):        
        A,B,C,D,E,F = 10, 11, 12, 13, 14,15
        skip, rep, add = self.monkey.skip, self.monkey.replace, self.monkey.add
        fun_str={skip:'skip', rep:'replace', add:'add'}
        make_dec = self.monkey.make_decision
        cases = [
            ([F,F,F,F], [1,2,3], [8,E], (skip,0) ),
            ([F,F,F,F], [1,2,3], [8,E],(skip,1))
        ]
        
        i = 0
        for four_bits, next_rand, code_digits, expected_out in cases:
            print '\n' 
            print '=====[CASE {0}]====='.format(i)
            i = i + 1
            op, sel = expected_out
            rst_msg = '{0} | {1} | {2}  ==> {3} {4}'.format(four_bits, next_rand, code_digits, fun_str[op], sel)
            print '[Expect]:' + rst_msg
            try:
                actual_out = make_dec(four_bits,next_rand,code_digits) 
                actual_op, actual_sel = actual_out
                self.assertEqual(actual_out, expected_out,msg = '\n[Wrong Result]: {0} {1}'.format(fun_str[actual_op], actual_sel))
            except self.failureException:
                print 'Oop!'
                print'[Wrong Result]: {0} {1}'.format(fun_str[op], sel) 
            except:
                print 'Oop!'
                print("Unexpected error:", sys.exc_info()[0])
                print '=====FAILED=====' 
            else:
                print '=====PASS=====' 

if __name__=="__main__":
    unittest.main(argv=sys.argv + ['--verbose'])
