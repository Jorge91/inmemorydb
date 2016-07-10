import sys

END_COMMAND = 'END'
SET_COMMAND = 'SET'
GET_COMMAND = 'GET'
UNSET_COMMAND = 'UNSET'
NUMEQUALTO_COMMAND = 'NUMEQUALTO'
BEGIN_COMMAND = 'BEGIN'
ROLLBACK_COMMAND = 'ROLLBACK'
COMMIT_COMMAND = 'COMMIT'

KEYBOARD_INPUT = 'KB'
FILE_INPUT = 'FL'

NULL_VALUE = 'NULL'
NO_TRANSACTION = 'NO TRANSACTION'


class Database(object):

    def __init__(self):
        self.actual_data = {}
        self.rollback_data = []

    def _set_command(self, name, value):
        if len(self.rollback_data) > 0:
            self.rollback_data[-1][name] = self.actual_data.get(name)
        self.actual_data[name] = value

    def _unset_command(self, name):
        if len(self.rollback_data) > 0:
            self.rollback_data[-1][name] = self.actual_data[name]
        del self.actual_data[name]

    def _get_command(self, name):
        return self.actual_data.get(name, NULL_VALUE)

    def _numequalto_command(self, value):
        return sum(1 for x in self.actual_data.values() if x == value)

    def _begin_command(self):
        self.rollback_data.append({})

    def _rollback_command(self):
        if len(self.rollback_data) == 0:
            return NO_TRANSACTION
        else:
            for k, v in self.rollback_data.pop().iteritems():
                if v is None and k in self.actual_data:
                    del self.actual_data[k]
                else:
                    self.actual_data[k] = v

    def _commit_command(self):
        if len(self.rollback_data) == 0:
            return NO_TRANSACTION
        else:
            self.rollback_data = []

    def perform_command(self, command):
        command = command.split(' ')
        command_name = command[0]
        if command_name == SET_COMMAND:
            return self._set_command(command[1], command[2])
        if command_name == UNSET_COMMAND:
            return self._unset_command(command[1])
        elif command_name == GET_COMMAND:
            return self._get_command(command[1])
        elif command_name == NUMEQUALTO_COMMAND:
            return self._numequalto_command(command[1])
        elif command_name == BEGIN_COMMAND:
            return self._begin_command()
        elif command_name == ROLLBACK_COMMAND:
            return self._rollback_command()
        elif command_name == COMMIT_COMMAND:
            return self._commit_command()


class InputOutputHandler(object):

    def __init__(self, mode):
        self.mode = mode
        self.lines = []

    def _get_keyboard_input(self):
        return raw_input()

    def _get_file_input(self):
        return self.lines.pop(0)

    def add_file(self, file):
        self.lines = open(file).read().split('\n')

    def get_command(self):
        if self.mode == KEYBOARD_INPUT:
            return self._get_keyboard_input()
        elif self.mode == FILE_INPUT:
            return self._get_file_input()

    def paint_result(self, result):
        print str(result)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = FILE_INPUT
    else:
        mode = KEYBOARD_INPUT

    interface = InputOutputHandler(mode)
    if mode == FILE_INPUT:
        interface.add_file(sys.argv[1])

    db = Database()

    command = ''
    while command != END_COMMAND:
        command = interface.get_command()
        result = db.perform_command(command)
        if result is not None:
            interface.paint_result(result)
