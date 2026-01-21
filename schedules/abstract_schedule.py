from abc import ABC, abstractmethod

from schedules.constants import SCHEDULE_STR_TEMPL
from schedules.errors import ErrorMessages, ErrorTemplates, ScheduleArgumentError
from schedules.schedule_item import ScheduleItem
from schedules.task import Task


class AbstractSchedule(ABC):
    """Абстрактный класс представляет оптимальное расписание для списка задач
    и количества исполнителей.

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

    def __init__(self, tasks: list[Task], executor_count: int):
        """Конструктор для инициализации объекта расписания.

        :param tasks: Список задач для составления расписания.
        :param executor_count: Количество исполнителей.
        :raise ScheduleArgumentError: Если список задач предоставлен в
        некорректном формате или количество исполнителей не является целым
        положительным числом.
        """
        AbstractSchedule.__validate_params(tasks)

        # Сохраняем исходный список задач в защищенном поле класса
        self._tasks = tasks

        # Для каждого исполнителя создаем пустую заготовку для расписания
        self._executor_schedule: list[list[ScheduleItem]] = [
            [] for _ in range(executor_count)
        ]

    def __str__(self):
        return SCHEDULE_STR_TEMPL.format(
            self.duration, self.task_count, self.executor_count
        )

    @property
    def tasks(self) -> tuple[Task]:
        """Возвращает исходный список задач для составления расписания."""
        return tuple(self._tasks)

    @property
    def task_count(self) -> int:
        """Возвращает количество задач для составления расписания."""
        return len(self._tasks)

    @property
    def executor_count(self) -> int:
        """Возвращает количество исполнителей."""
        return len(self._executor_schedule)

    @property
    @abstractmethod
    def duration(self) -> float:
        """Возвращает общую продолжительность расписания."""
        pass

    def get_schedule_for_executor(self, executor_idx: int) -> tuple[ScheduleItem]:
        """Возвращает расписание для указанного исполнителя.

        :param executor_idx: Индекс исполнителя.
        :raise ScheduleArgumentError: Если индекс исполнителя не является целым
         положительным числом или превышает количество исполнителей.
        :return: Расписание для указанного исполнителя.
        """
        self.__validate_executor_idx(executor_idx)
        return tuple(self._executor_schedule[executor_idx])

    @staticmethod
    def __validate_params(tasks: list[Task]) -> None:
        """Проводит валидацию входящих параметров для инициализации объекта
        класса Schedule."""
        if not isinstance(tasks, list):
            raise ScheduleArgumentError(ErrorMessages.TASKS_NOT_LIST)
        if len(tasks) < 1:
            raise ScheduleArgumentError(ErrorMessages.TASKS_EMPTY_LIST)
        for idx, value in enumerate(tasks):
            if not isinstance(value, Task):
                raise ScheduleArgumentError(ErrorTemplates.INVALID_TASK.format(idx))

    def __validate_executor_idx(self, executor_idx: int) -> None:
        """Проводит валидацию индекса исполнителя."""
        if not isinstance(executor_idx, int) or executor_idx < 0:
            raise ScheduleArgumentError(ErrorMessages.EXECUTOR_NOT_INT)
        if executor_idx >= self.executor_count:
            raise ScheduleArgumentError(ErrorMessages.EXECUTOR_OUT_OF_RANGE)

    def create_mermaid_code_for_gant_diagramm(self, title: str = "Диграмма Ганта"): 
        """Строит код mermaid для диаграммы Ганта"""
        # Инициализация диграммы
        mermaid_code = ["```mermaid", f"gantt", f"    title{title}"]
        mermaid_code.append(f"    dateFormat X") 
        mermaid_code.append(f"    axisFormat %d") 
        
        # Проходимся по всем исполнителям 
        for executor_idx in range(self.executor_count):
            section_name = f"Конвейер {executor_idx + 1}"
            mermaid_code.append(f"    section {section_name}")
            
            # Получаем задачи для исполнителя
            schedule_items = self.get_schedule_for_executor(executor_idx)
            prev_task_id = None
            
            # Обработка задач
            for i in range(len(schedule_items)):
                item = schedule_items[i]  
                task_id = f"e{executor_idx}_t{i}"
                start_num = item.start  # начало
                duration_num = item.duration  # продолжительность 
                
                # Зависимости от предыдущих задач
                if prev_task_id is None:
                    dependency = str(start_num) # для первой задачи 
                else:
                    dependency = f"after {prev_task_id}"
                    
                    # Зависимость от первой станции для второй
                    if executor_idx == 1 and self.executor_count == 2:
                        if i < len(self._executor_schedule[0]):
                            prev_task_id_executor0 = f"e0_t{i}"
                            dependency = f"after {prev_task_id_executor0} {prev_task_id}"
                
                task_name = item.task_name
                if task_name == "downtime":
                    task_name = f"Простой {i+1}"
                
                # Формирование строки
                mermaid_code.append(f"    {task_name:10} :{task_id}, {dependency}, {duration_num}")
                prev_task_id = task_id
        # Конец диаграммы
        mermaid_code.append("```")
        # Вывод
        return "\n".join(mermaid_code)