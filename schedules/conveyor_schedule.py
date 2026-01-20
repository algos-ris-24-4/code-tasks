from schedules.abstract_schedule import AbstractSchedule
from schedules.errors import (
    ScheduleArgumentError,
    ErrorMessages,
    ErrorTemplates,
)
from schedules.staged_task import StagedTask
from schedules.schedule_item import ScheduleItem


class ConveyorSchedule(AbstractSchedule):
    """Класс представляет оптимальное расписание для списка задач, состоящих
     из двух этапов и двух исполнителей. Для построения расписания используется
     алгоритм Джонсона.

    Properties
    ----------
    tasks(self) -> tuple[Task]:
        Возвращает исходный список задач для составления расписания.

    task_count(self) -> int:
        Возвращает количество задач для составления расписания.

    executor_count(self) -> int:
        Возвращает количество исполнителей.

    duration(self) -> float:
        Возвращает общую продолжительность расписания.

    Methods
    -------
    get_schedule_for_executor(self, executor_idx: int) -> tuple[ScheduleRow]:
        Возвращает расписание для указанного исполнителя.
    """

    def __init__(self, tasks: list[StagedTask]):
        """Конструктор для инициализации объекта расписания.

        :param tasks: Список задач для составления расписания.
        :raise ScheduleArgumentError: Если список задач предоставлен в
        некорректном формате или количество этапов для какой-либо задачи не
        равно двум.
        """
        ConveyorSchedule.__validate_params(tasks)
        super().__init__(tasks, 2)

        # Процедура заполняет пустую заготовку расписания для каждого
        # исполнителя объектами ScheduleItem.
        self.__fill_schedule(ConveyorSchedule.__sort_tasks(tasks))

    @property
    def duration(self) -> float:
        """Возвращает общую продолжительность расписания."""
        return self._executor_schedule[0][-1].end

    def __fill_schedule(self, tasks: list[StagedTask]) -> None:
        """Процедура составляет расписание из элементов ScheduleItem для каждого
        исполнителя, согласно алгоритму Джонсона."""

        self._executor_schedule[0] = []
        self._executor_schedule[1] = []
        
        time_executor1 = 0
        time_executor2 = 0

        for task in tasks:
            item1 = ScheduleItem(task, time_executor1, task.stage_durations[0])
            self._executor_schedule[0].append(item1)

            actual_start_stage2 = max(time_executor1 + task.stage_durations[0], time_executor2)

            if actual_start_stage2 > time_executor2:
                downtime_duration = actual_start_stage2 - time_executor2
                downtime_item = ScheduleItem(None, time_executor2, downtime_duration)
                self._executor_schedule[1].append(downtime_item)

            item2 = ScheduleItem(task, actual_start_stage2, task.stage_durations[1])
            self._executor_schedule[1].append(item2)

            time_executor1 += task.stage_durations[0]
            time_executor2 = actual_start_stage2 + task.stage_durations[1]

        if time_executor1 < time_executor2:
            downtime_duration = time_executor2 - time_executor1
            downtime_item = ScheduleItem(None, time_executor1, downtime_duration)
            self._executor_schedule[0].append(downtime_item)


    @staticmethod
    def __sort_tasks(tasks: list[StagedTask]) -> list[StagedTask]:
        """Возвращает отсортированный список задач для применения
        алгоритма Джонсона."""
        group1 = []
        group2 = []
        
        for task in tasks:
            if task.stage_duration(0) <= task.stage_duration(1):
                group1.append(task)
            else:
                group2.append(task)

        length_group1 = len(group1)
        for i in range(length_group1):
            for j in range(0, length_group1 - i - 1):
                if group1[j].stage_durations[0] > group1[j + 1].stage_durations[0]:
                    group1[j], group1[j + 1] = group1[j + 1], group1[j]
    
        length_group2 = len(group2)
        for i in range(length_group2):
            for j in range(0, length_group2 - i - 1):
                if group2[j].stage_durations[1] < group2[j + 1].stage_durations[1]:
                    group2[j], group2[j + 1] = group2[j + 1], group2[j]

        return group1 + group2

    @staticmethod
    def __validate_params(tasks: list[StagedTask]) -> None:
        """Проводит валидацию входящих параметров для инициализации объекта
        класса ConveyorSchedule."""
        if not isinstance(tasks, list):
            raise ScheduleArgumentError(ErrorMessages.TASKS_NOT_LIST)
        if len(tasks) < 1:
            raise ScheduleArgumentError(ErrorMessages.TASKS_EMPTY_LIST)
        for idx, value in enumerate(tasks):
            if not isinstance(value, StagedTask):
                raise ScheduleArgumentError(ErrorTemplates.INVALID_TASK.format(idx))
            if value.stage_count != 2:
                raise ScheduleArgumentError(
                    ErrorTemplates.INVALID_STAGE_CNT.format(idx)
                )


if __name__ == "__main__":
    print("Пример использования класса ConveyorSchedule")

    # Инициализируем входные данные для составления расписания
    tasks = [
        StagedTask("a", [7, 2]),
        StagedTask("b", [3, 4]),
        StagedTask("c", [2, 5]),
        StagedTask("d", [4, 1]),
        StagedTask("e", [6, 6]),
        StagedTask("f", [5, 3]),
        StagedTask("g", [4, 5]),
    ]

    # Инициализируем экземпляр класса Schedule
    # при этом будет рассчитано расписание для каждого исполнителя
    schedule = ConveyorSchedule(tasks)

    # Выведем в консоль полученное расписание
    print(schedule)
    for i in range(schedule.executor_count):
        print(f"\nРасписание для исполнителя # {i + 1}:")
        for schedule_item in schedule.get_schedule_for_executor(i):
            print(schedule_item)
