import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

from ioiopype.common.utilities.overriding_buffer import OverridingBuffer
import numpy as np

import unittest

class TestBuffer(unittest.TestCase):
    def test_buffer_aligned(self):
        buf = OverridingBuffer(10,1,OverridingBuffer.OutputMode.Aligned)
        buf.setData(np.array([[1,2,3]]).transpose())

        frame = buf.getFrame()
        self.assertEqual(frame[0,0], 0)
        self.assertEqual(frame[-1,-1], 3)
        self.assertEqual(frame[-2,-1], 2)
        self.assertEqual(frame[-3,-1], 1)
        buf.setData(np.array([[4,5,6]]).transpose())
        buf.setData(np.array([[7,8,9]]).transpose())

        frame = buf.getFrame()
        self.assertEqual(frame[0,0], 0)
        self.assertEqual(frame[-1,-1], 9)
        self.assertEqual(frame[-2,-1], 8)
        self.assertEqual(frame[-3,-1], 7)

        buf.setData(np.array([[10,11,12]]).transpose())
        frame = buf.getFrame()
        self.assertEqual(frame[0,0], 3)
        self.assertEqual(frame[-1,-1], 12)
        self.assertEqual(frame[-2,-1], 11)
        self.assertEqual(frame[-3,-1], 10)

    def test_buffer_not_aligned(self):
        buf = OverridingBuffer(10,1,OverridingBuffer.OutputMode.NotAligned)
        buf.setData(np.array([[1,2,3]]).transpose())

        frame = buf.getFrame()
        self.assertEqual(frame[0,-1], 1)
        self.assertEqual(frame[1,-1], 2)
        self.assertEqual(frame[2,-1], 3)
        self.assertEqual(frame[-1,-1], 0)
        buf.setData(np.array([[4,5,6]]).transpose())
        buf.setData(np.array([[7,8,9]]).transpose())

        frame = buf.getFrame()
        self.assertEqual(frame[0,-1], 1)
        self.assertEqual(frame[1,-1], 2)
        self.assertEqual(frame[2,-1], 3)
        self.assertEqual(frame[6,-1], 7)
        self.assertEqual(frame[7,-1], 8)
        self.assertEqual(frame[8,-1], 9)
        self.assertEqual(frame[-1,-1], 0)

        buf.setData(np.array([[10,11,12]]).transpose())
        frame = buf.getFrame()
        
        self.assertEqual(frame[0,-1], 11)
        self.assertEqual(frame[1,-1], 12)
        self.assertEqual(frame[2,-1], 3)
        self.assertEqual(frame[-1,-1], 10)

if __name__ == "__main__":
    unittest.main()