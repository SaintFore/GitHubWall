import pytest
from datetime import date, timedelta
from src.core.scheduler import Scheduler, get_commit_count


def test_get_commit_count():
    """测试级别到提交次数的映射"""
    assert get_commit_count(0) == 0
    assert get_commit_count(1) == 1
    assert get_commit_count(2) == 3
    assert get_commit_count(3) == 5
    assert get_commit_count(4) == 10


def test_get_commit_count_invalid():
    """测试无效级别"""
    with pytest.raises(ValueError):
        get_commit_count(5)


def test_scheduler_creation():
    """测试调度器创建"""
    scheduler = Scheduler(start_date=date(2024, 1, 1), end_date=date(2024, 12, 31))
    assert scheduler.start_date == date(2024, 1, 1)
    assert scheduler.end_date == date(2024, 12, 31)


def test_scheduler_align_to_sunday():
    """测试日期对齐到周日"""
    from src.core.scheduler import align_to_sunday

    # 2024-01-01 是周一
    aligned = align_to_sunday(date(2024, 1, 1))
    assert aligned == date(2023, 12, 31)  # 对齐到前一个周日


def test_scheduler_generate_schedule():
    """测试生成提交计划"""
    from src.core.pattern import Pattern

    # 简单图案：只有 1 周
    pattern = Pattern(name="test", data=[[1, 0, 0, 0, 0, 0, 0]] * 7)
    scheduler = Scheduler(start_date=date(2024, 1, 1), end_date=date(2024, 1, 7))
    schedule = scheduler.generate_schedule(pattern)

    # 应该有 1 个日期有提交
    assert len(schedule) > 0
    # 所有日期都应该在范围内
    for d in schedule:
        assert date(2024, 1, 1) <= d <= date(2024, 1, 7)
