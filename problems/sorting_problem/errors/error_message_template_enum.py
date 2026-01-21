from enum import StrEnum


class ErrorMessageTemplateEnum(StrEnum):
    """Перечисление шаблонов сообщений об ошибках."""

    ERR_INCOMPARABLE_EMBEDDED_TYPES = (
        "Переданы несравнимые экземпляры классов '{}' и '{}'"
    )  
    ERR_INPUT_IS_NONE = "Входной аргумент не может быть None"
    ERR_NOT_A_LIST = "Входной аргумент должен быть списком"

