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
            ([F,D,7,D], [2,9,0], [9,F], (add,1) ),
            ([9,3,1,9], [9,0,7], [9,F],(rep,2)),
            ([F,F,E,F], [0,7,5], [9,F],(add,1)),
            ([6,F,6,6], [7,5,0], [9,F],(add,1)),
            ([5,3,5,A], [5,0,0], [9,F],(rep,3))
        ]
        
        total_case = 0
        pass_case = 0
        wrong_rst_case = 0
        error_case = 0 
        for four_bits, next_rand, code_digits, expected_out in cases:
            print '\n'
            print '=====[CASE {0}]====='.format(total_case)
            total_case = total_case + 1
            op, sel = expected_out
            rst_msg = '{0} | {1} | {2}  ==> {3} {4}'.format(four_bits, next_rand, code_digits, fun_str[op], sel)
            print '[Expect]:' + rst_msg
            try:
                actual_out = make_dec(four_bits,next_rand,code_digits) 
                actual_op, actual_sel = actual_out
                self.assertEqual(actual_out, expected_out,msg = '\n[Wrong Result]: {0} {1}'.format(fun_str[actual_op], actual_sel))
            except self.failureException:
                wrong_rst_case = wrong_rst_case + 1
                print 'Oop!'
                print'[Wrong Result]: {0} {1}'.format(fun_str[actual_op], actual_sel) 
                print '=====FAILED=====' 
            except:
                error_case = error + 1
                print 'Oop!'
                print("Unexpected error:", sys.exc_info()[0])
                print '=====FAILED=====' 
            else:
                pass_case = pass_case + 1
                print '=====PASS=====' 
        print '\n'
        print '----------------------------------------------------------------------'
        print 'TOTAL CASE:{0} | PASS:{1} WRONG RESULT:{2} UNEXPECTED ERROR:{3}'.format(total_case, pass_case, wrong_rst_case, error_case)

if __name__=="__main__":
    unittest.main(argv=sys.argv + ['--verbose'])
