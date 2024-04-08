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

    @unittest.skip("暂时不需要")
    def test_load_price(self):
        """测试爬取价格表"""
        self.get_price_table()

    @unittest.skip("暂时不需要")
    def test_faatigue_cost(self):
        """测试疲劳值计算"""
        for city in self.CITIES:
            for other_city in self.CITIES:
                if city == other_city:
                    continue
                fatigue_cost = city.travel_cost(other_city)
                print(f"{city} -> {other_city} 疲劳消耗: {fatigue_cost}")

    @unittest.skip("暂时不需要")
    def test_get_product_stock(self):
        """测试获取商品库存"""
        test_city = self.CITIES[0]
        print(test_city.product_stock)

    # @unittest.skip("暂时不需要")
    def test_calc_profit_to_and_fro(self):
        """测试计算利润"""
        import itertools
        import numpy as np
        from main.database import GameData, Product
        from main.database.get_price import get_price_table

        get_price_table()

        res = []

        for route_loop in itertools.combinations(self.CITIES, 2):
            cityA, cityB = route_loop
            profit = 0
            _city_count, product_count = GameData.price.shape
            productA = np.array([cityA.product_stock.get(
                Product(i + 1), 0) for i in range(product_count)])
            productB = np.array([cityB.product_stock.get(
                Product(i + 1), 0) for i in range(product_count)])
            profitsA = np.dot(GameData.price, productA)
            profitsB = np.dot(GameData.price, productB)
            profit += profitsA[cityB.value - 1] - profitsA[cityA.value - 1]
            profit += profitsB[cityA.value - 1] - profitsB[cityB.value - 1]
            cost = cityA.travel_cost(cityB)
            # print(
            #     f"{cityA.name} <-> {cityB.name} 往返利润: {profit} \t 疲劳消耗: {cost} \t 利润/疲劳: {(profit / cost):.2f}")
            res.append((cityA, cityB, profit, cost, profit / cost))

        res.sort(key=lambda x: x[-1], reverse=True)
        res = res[:5]

        print("不使用书不砍价抬价且假定买完货的利润前五:")
        for cityA, cityB, profit, cost, ratio in res:
            print(
                f"{cityA.name} <-> {cityB.name} 利润: {round(profit):d}\t疲劳: {int(cost):d}\t利润/疲劳: {ratio:.2f}")

    def tearDown(self) -> None:
        # importlib.reload(main.database)
        ...


if __name__ == '__main__':
    unittest.main()
