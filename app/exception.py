class UserNotFoundException(Exception):
    detail = 'User not found'


class UserNotCorrectPasswordException(Exception):
    detail = 'Password not correct'


class TokenExpiredException(Exception):
    detail = 'Token expired'


class TokenNotCorrectException(Exception):
    detail = 'Token not correct'


class TaskNotFound(Exception):
    detail = 'Task not found'
