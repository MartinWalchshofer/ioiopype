import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

from ioiopype.common.utilities.overriding_buffer import OverridingBuffer
import numpy as np

import unittest

class TestUpsample(unittest.TestCase):
    def test_upsample(self):
        cnt = 0
        vals = [5, 10, 5]
        prevVal = 0
        valstmp = []
        for val in vals:
            if cnt> 0:
                valstmp.append(np.array([np.linspace(prevVal, val, num=round(val+1))]).transpose()[1:,:])
            cnt += val
            prevVal = val
        valsUs = np.concatenate(valstmp, axis=0)
        self.assertEqual(valsUs.shape[0], 15)

if __name__ == "__main__":
    unittest.main()