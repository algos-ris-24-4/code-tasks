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
        if self._executor_schedule[1] and len(self._executor_schedule[1]) > 0:
            return self._executor_schedule[1][-1].end  # Последняя задача на станции 2
        elif self._executor_schedule[0] and len(self._executor_schedule[0]) > 0:
            return self._executor_schedule[0][-1].end  # Если только одна станция
        return 0.0
    
    def __fill_schedule(self, tasks: list[StagedTask]) -> None:

        startTimes = [0, 0]
        
        for task in tasks:
            
            duration1 = task.stage_duration(0)
            
            item1 = ScheduleItem(task, startTimes[0], duration1)
            self._executor_schedule[0].append(item1)

            startTime2 = max(startTimes[0] + duration1, startTimes[1])

            duration2 = task.stage_duration(1)

            item2 = ScheduleItem(task, startTime2, duration2)
            self._executor_schedule[1].append(item2)

            startTimes[0] += duration1
            startTimes[1] = startTime2 + duration2

    @staticmethod
    def __sort_tasks(tasks: list[StagedTask]) -> list[StagedTask]:
        
        remainingTasks = tasks.copy()
        list1 = []
        list2 = []
        
        while remainingTasks:
            min_time = 999999999
            min_task = None
            min_station = -1
            
            for task in remainingTasks:
                t1 = task.stage_duration(0)
                t2 = task.stage_duration(1)

                if t1 < min_time:
                    min_time = t1
                    min_task = task
                    min_station = 1 

                if t2 < min_time:
                    min_time = t2
                    min_task = task
                    min_station = 2 
            
            if min_station == 1:
                list1.append(min_task)  
                list2.insert(0, min_task) 
            remainingTasks.remove(min_task)
        return list1 + list2


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
