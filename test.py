import importlib
import unittest

class TestPriceDatabase(unittest.TestCase):
    """价格相关功能测试"""
    
    def setUp(self) -> None:
        from main.database import GameData
        from main.database.get_price import get_price_table
        self.GameData = GameData
        self.get_price_table = get_price_table
        
    def test_load_price(self):
        """测试爬取价格表"""
        self.get_price_table()
    
    def tearDown(self) -> None:
        # importlib.reload(main.database)
        ...

if __name__ == '__main__':
    unittest.main()
