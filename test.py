import importlib
import unittest

class TestPriceDatabase(unittest.TestCase):
    """价格相关功能测试"""
    
    def setUp(self) -> None:
        from main.database import GameData, CITIES
        from main.database.get_price import get_price_table
        self.GameData = GameData
        self.CITIES = CITIES
        self.get_price_table = get_price_table
        
    def test_load_price(self):
        """测试爬取价格表"""
        self.get_price_table()
        
    def test_faatigue_cost(self):
        """测试疲劳值计算"""
        for city in self.CITIES:
            for other_city in self.CITIES:
                if city == other_city:
                    continue
                fatigue_cost = city.travel_cost(other_city)
                print(f"{city} -> {other_city} 疲劳消耗: {fatigue_cost}")
    
    def tearDown(self) -> None:
        # importlib.reload(main.database)
        ...

if __name__ == '__main__':
    unittest.main()
