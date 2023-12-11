import unittest
from mathfunc import *




class TestMathFunc(unittest.TestCase):

    # TestCase class方法,所有case執行前自動執行
    @classmethod
    def setUpClass(cls):
        print("這裡是所有測試案例前的準備工作")

    # TestCase class方法,所有case執行前自動執行
    @classmethod
    def tearDownClass(cls):
        print("這裡是所有測試案例後的清理工作")

    # TestCase class方法,所有case執行前自動執行
    def setUp(self):
        print("這裡是一個測試用例前的準備工作")

    # TestCase class方法,所有case執行前自動執行
    def tearDown(self):
        print("這裡是一個測試案例後的清理工作")

    @unittest.skip("我想暫時跳過這個測試案例.")
    def test_add(self):
        self.assertEqual(3, add(1, 2))
        self.assertNotEqual(3, add(2, 2))  # 測試業務方法add

    def test_minus(self):
        self.skipTest('跳過這個測試案例')
        self.assertEqual(1, minus(3, 2))  # 測試業務方法minus

    def test_multi(self):
        self.assertEqual(6, multi(2, 3))  # 測試業務方法multi

    def test_divide(self):
        self.assertEqual(2, divide(6, 3))  # 測試業務方法divide
        self.assertEqual(2.5, divide(5, 2))

if __name__ == '__main__':
    unittest.main(verbosity=2)