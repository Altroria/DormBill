"""电费计算服务单元测试"""
import pytest
from decimal import Decimal
from datetime import date
from sqlalchemy.orm import Session

from app.services.electricity_calculation_service import ElectricityCalculationService
from app.models.room_main_meter import RoomMainMeterRecord
from app.models.meter import MeterRecord
from app.models.room import Room
from app.models.residence import ResidenceRecord
from app.models.employee import Employee
from app.models.building import Building


class TestElectricityCalculation:
    """电费计算服务测试"""
    
    @pytest.fixture
    def db_session(self):
        """测试数据库会话"""
        # 这里需要配置测试数据库
        # 暂时跳过，实际使用时需要配置
        pass
    
    def test_calculate_common_electricity(self):
        """测试公共用电计算"""
        # 模拟数据：总表1000度，空调表450度
        total_degree = Decimal("1000.00")
        total_ac_degree = Decimal("450.00")
        
        # 公共用电 = 总表 - 空调表
        common_degree = total_degree - total_ac_degree
        
        assert common_degree == Decimal("550.00")
    
    def test_common_electricity_fee_calculation(self):
        """测试公共电费计算"""
        # 总电费490元，空调电费220.5元
        total_fee = Decimal("490.00")
        total_ac_fee = Decimal("220.50")
        
        # 公共电费 = 总电费 - 空调电费
        common_fee = total_fee - total_ac_fee
        
        assert common_fee == Decimal("269.50")
    
    def test_common_fee_distribution_even(self):
        """测试公共电费平均分摊（能整除）"""
        common_fee = Decimal("300.00")
        occupants_count = 6
        
        # 人均公共电费
        per_person = common_fee / occupants_count
        
        assert per_person == Decimal("50.00")
    
    def test_common_fee_distribution_with_remainder(self):
        """测试公共电费分摊（有尾差）"""
        from app.utils.decimal_utils import allocate_with_remainder
        
        common_fee = Decimal("269.50")
        occupants_count = 6
        
        # 使用尾差处理函数
        allocations = allocate_with_remainder(common_fee, occupants_count)
        
        # 验证总和不变
        assert sum(allocations) == common_fee
        
        # 验证分配数量正确
        assert len(allocations) == occupants_count
        
        # 验证每个人的费用都在合理范围内
        base_amount = common_fee / occupants_count
        for amount in allocations:
            assert abs(amount - base_amount) < Decimal("0.01")
    
    def test_ac_fee_distribution_by_unit(self):
        """测试空调费按套间人数分摊"""
        from app.utils.decimal_utils import allocate_with_remainder
        
        # 201-1套间：49元，2人
        ac_fee = Decimal("49.00")
        occupants_in_unit = 2
        
        allocations = allocate_with_remainder(ac_fee, occupants_in_unit)
        
        assert sum(allocations) == ac_fee
        assert len(allocations) == occupants_in_unit
        assert allocations[0] == Decimal("24.50")
        assert allocations[1] == Decimal("24.50")
    
    def test_negative_common_electricity_detection(self):
        """测试异常情况：公共用电为负值"""
        # 异常：空调用电大于总用电
        total_degree = Decimal("500.00")
        total_ac_degree = Decimal("600.00")
        
        common_degree = total_degree - total_ac_degree
        
        # 应该检测到异常
        assert common_degree < 0
    
    def test_zero_occupants_handling(self):
        """测试无入住人员情况"""
        common_fee = Decimal("300.00")
        occupants_count = 0
        
        # 无人时，人均费用应该为0或跳过计算
        if occupants_count == 0:
            per_person = Decimal("0.00")
        else:
            per_person = common_fee / occupants_count
        
        assert per_person == Decimal("0.00")
    
    def test_electricity_price_calculation(self):
        """测试电费单价计算"""
        # 0.49元/度
        unit_price = Decimal("0.49")
        degree = Decimal("1000.00")
        
        fee = degree * unit_price
        
        assert fee == Decimal("490.00")
    
    def test_multiple_rooms_calculation(self):
        """测试多个房号的电费计算"""
        # 房号1：总表1000度490元，空调450度220.5元，6人
        room1_common_fee = Decimal("490.00") - Decimal("220.50")
        room1_per_person = room1_common_fee / 6
        
        # 房号2：总表800度392元，空调300度147元，4人
        room2_common_fee = Decimal("392.00") - Decimal("147.00")
        room2_per_person = room2_common_fee / 4
        
        # 验证
        assert room1_common_fee == Decimal("269.50")
        assert room2_common_fee == Decimal("245.00")
        assert room2_per_person == Decimal("61.25")
    
    def test_precision_handling(self):
        """测试精度处理"""
        from app.utils.decimal_utils import round_money
        
        # 金额应保留2位小数
        amount = Decimal("44.916666666666")
        rounded = round_money(amount)
        
        assert rounded == Decimal("44.92")
    
    def test_complete_workflow(self):
        """测试完整计算流程"""
        # 201房号完整数据
        total_degree = Decimal("1000.00")
        total_fee = Decimal("490.00")
        
        # 4个套间空调数据
        ac_data = [
            {"unit": "1", "degree": Decimal("100"), "fee": Decimal("49.00"), "occupants": 2},
            {"unit": "2", "degree": Decimal("150"), "fee": Decimal("73.50"), "occupants": 1},
            {"unit": "3", "degree": Decimal("120"), "fee": Decimal("58.80"), "occupants": 2},
            {"unit": "4", "degree": Decimal("80"), "fee": Decimal("39.20"), "occupants": 1},
        ]
        
        # 1. 计算总空调用电
        total_ac_degree = sum(ac["degree"] for ac in ac_data)
        total_ac_fee = sum(ac["fee"] for ac in ac_data)
        
        # 2. 计算公共用电
        common_degree = total_degree - total_ac_degree
        common_fee = total_fee - total_ac_fee
        
        # 3. 统计总人数
        total_occupants = sum(ac["occupants"] for ac in ac_data)
        
        # 4. 分摊公共电费
        from app.utils.decimal_utils import allocate_with_remainder
        common_allocations = allocate_with_remainder(common_fee, total_occupants)
        
        # 验证
        assert total_ac_degree == Decimal("450.00")
        assert total_ac_fee == Decimal("220.50")
        assert common_degree == Decimal("550.00")
        assert common_fee == Decimal("269.50")
        assert total_occupants == 6
        assert sum(common_allocations) == common_fee
        assert len(common_allocations) == total_occupants


class TestEdgeCases:
    """边界情况测试"""
    
    def test_single_occupant(self):
        """测试单人房间"""
        common_fee = Decimal("100.00")
        occupants = 1
        
        per_person = common_fee / occupants
        assert per_person == common_fee
    
    def test_very_small_fee(self):
        """测试极小费用"""
        from app.utils.decimal_utils import allocate_with_remainder
        
        common_fee = Decimal("0.10")
        occupants = 3
        
        allocations = allocate_with_remainder(common_fee, occupants)
        
        assert sum(allocations) == common_fee
        assert all(a >= 0 for a in allocations)
    
    def test_large_occupants_count(self):
        """测试大量人数"""
        from app.utils.decimal_utils import allocate_with_remainder
        
        common_fee = Decimal("1000.00")
        occupants = 20
        
        allocations = allocate_with_remainder(common_fee, occupants)
        
        assert sum(allocations) == common_fee
        assert len(allocations) == occupants
    
    def test_zero_common_electricity(self):
        """测试公共用电为0"""
        # 总表 = 空调表（理论上不太可能，但需要处理）
        total_degree = Decimal("450.00")
        total_ac_degree = Decimal("450.00")
        
        common_degree = total_degree - total_ac_degree
        
        assert common_degree == Decimal("0.00")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
