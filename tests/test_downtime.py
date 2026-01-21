import unittest

from schedules.conveyor_schedule import ConveyorSchedule
from schedules.staged_task import StagedTask
from schedules.errors import ScheduleArgumentError, ErrorMessages


class TestScheduleDowntime(unittest.TestCase):
    def test_single_task_no_downtime(self):
        """Проверяет, что для конвейерного расписания простой исполнителей положителен."""
        task = StagedTask("a", [2, 3])
        schedule = ConveyorSchedule([task])

        self.assertGreater(schedule.get_downtime_for_executor(0), 0)
        self.assertGreater(schedule.get_downtime_for_executor(1), 0)
        self.assertGreater(schedule.get_total_downtime(), 0)


    def test_double_task_with_downtime(self):
        """Проверяет корректность расчёта простоя для двух задач."""
        task_a = StagedTask("a", [2, 1])
        task_b = StagedTask("b", [1, 2])
        schedule = ConveyorSchedule([task_a, task_b])

 
        self.assertEqual(1, schedule.get_downtime_for_executor(0))

        self.assertEqual(1, schedule.get_downtime_for_executor(1))

        self.assertEqual(2, schedule.get_total_downtime())

    def test_triple_mixed_downtime(self):
        """Проверяет простой при смешанном наборе задач."""
        task_a = StagedTask("a", [2, 1])
        task_b = StagedTask("b", [3, 4])
        task_c = StagedTask("c", [6, 5])
        schedule = ConveyorSchedule([task_a, task_b, task_c])

        self.assertEqual(4, schedule.get_downtime_for_executor(0))
        self.assertEqual(4, schedule.get_downtime_for_executor(1))
        self.assertEqual(8, schedule.get_total_downtime())

    def test_invalid_executor_index(self):
        """Проверяет выброс исключения при некорректном индексе исполнителя."""
        task = StagedTask("a", [1, 1])
        schedule = ConveyorSchedule([task])

        incorrect_idx = [-1, 1, None, "str", []]
        for idx in incorrect_idx:
            with self.subTest(idx=idx):
                with self.assertRaises(ScheduleArgumentError) as error:
                    schedule.get_downtime_for_executor(idx)
                self.assertEqual(
                    ErrorMessages.EXECUTOR_NOT_INT,
                    str(error.exception),
                )

    def test_out_of_range_executor_index(self):
        """Проверяет выброс исключения при выходе за диапазон исполнителей."""
        task = StagedTask("a", [1, 1])
        schedule = ConveyorSchedule([task])

        with self.assertRaises(ScheduleArgumentError) as error:
            schedule.get_downtime_for_executor(2)

        self.assertEqual(
            ErrorMessages.EXECUTOR_OUT_OF_RANGE,
            str(error.exception),
        )


if __name__ == "__main__":
    unittest.main()
