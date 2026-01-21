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
        if not tasks:
            return  
        
        self._executor_schedule = [[], []]          
        # Временные переменные для отслеживания времени окончания последней задачи
        time_executor1 = 0
        
        #Заполненеи расписания для первого исполнителя
        for task in tasks:
            start_executor1 = time_executor1
            duration_executor1 = task.stage_duration(0)
            schedule_item1 = ScheduleItem(task, start_executor1, duration_executor1)
            self._executor_schedule[0].append(schedule_item1)
            time_executor1 += duration_executor1

        schedule_item2 = ScheduleItem(None, 0, self._executor_schedule[0][0].end)
        self._executor_schedule[1].append(schedule_item2)
        count_schedule_items= 1   
        count_tasks = 0
        #Заполнение расписания для второго исполнителя
        for task in tasks[0:]:            
            duration_executor2 = task.stage_duration(1)            
            start_executor2 = self._executor_schedule[1][count_schedule_items - 1].end
            empty_duration = self._executor_schedule[0][count_tasks].end - start_executor2
            if(empty_duration > 0):
                empty = ScheduleItem(None, start_executor2, empty_duration)
                self._executor_schedule[1].append(empty)
                start_executor2 = self._executor_schedule[1][count_schedule_items-1].end
                count_schedule_items+=1
            else:
                empty_duration = 0
            schedule_item2 = ScheduleItem(task, start_executor2 + empty_duration, duration_executor2)
            
            self._executor_schedule[1].append(schedule_item2)
            count_schedule_items+=1
            count_tasks += 1
        
        if(self._executor_schedule[1][-1].end > self._executor_schedule[0][-1].end):
            empty_duration = self._executor_schedule[1][-1].end - self._executor_schedule[0][-1].end
            schedule_item2 = ScheduleItem(None, self._executor_schedule[0][-1].end, empty_duration)
            self._executor_schedule[0].append(schedule_item2)


    @staticmethod
    def __sort_tasks(tasks: list[StagedTask]) -> list[StagedTask]:
        """Возвращает отсортированный список задач для применения
        алгоритма Джонсона."""
         # Разделяем задачи на две группы
        group1 = []  # Задачи, где время на первом этапе ≤ времени на втором
        group2 = []  # Задачи, где время на первом этапе > времени на втором
        
        for task in tasks:
            if task.stage_duration(0) <= task.stage_duration(1):
                group1.append(task)
            else:
                group2.append(task)
    
        # Сортируем group1 по возрастанию времени на первом этапе
        group1_sorted = sorted(group1, key=lambda t: t.stage_duration(0))
        
        # Сортируем group2 по убыванию времени на втором этапе
        group2_sorted = sorted(group2, key=lambda t: t.stage_duration(1), reverse=True)
    
        return group1_sorted + group2_sorted

    def add_task(self, task: StagedTask) -> None:
        """Добавляет задачу в расписание и пересчитывает его.
        
        :param task: Задача для добавления
        :raise ScheduleArgumentError: Если задача некорректна
        """
        self.__validate_params([task])
        
        if(not [i.name for i in self._tasks].__contains__(task.name)):
        # Добавляем задачу в список задач
            self._tasks.append(task)
        else:
            return
        
        # Пересчитываем расписание
        self.__recalculate_schedule()

    def remove_task(self, del_task: StagedTask) -> None:
        """Удаляет задачу из расписания по имени и пересчитывает его.
        
        :param task_name: Имя задачи для удаления
        :raise ScheduleArgumentError: Если задача с таким именем не найдена
        """
        task_to_remove = None
        for task in self._tasks:
            if task.name == del_task.name:
                task_to_remove = task
                break
        
        if task_to_remove is None:
            raise ScheduleArgumentError(
                ErrorTemplates.TASK_NOT_FOUND.format(del_task.name)
            )
        
        # Удаляем задачу
        self._tasks.remove(task_to_remove)
        
        # Проверяем, что остались задачи
        if len(self._tasks) == 0:
            self._executor_schedule = [[], []]
        else:
            # Пересчитываем расписание
            self.__recalculate_schedule()

    def __recalculate_schedule(self) -> None:
        """Пересчитывает расписание с текущим списком задач."""
        sorted_tasks = self.__sort_tasks(self._tasks)
        self.__fill_schedule(sorted_tasks)

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

