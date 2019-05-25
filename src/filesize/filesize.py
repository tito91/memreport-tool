class FileSize:

    KILO = 1024.
    MEGA = 1024.*1024
    GIGA = 1024.*1024*1024

    units = ['', 'kb', 'mb', 'gb']

    units_reversed = units.copy()
    units_reversed.reverse()

    multipliers_to_byte = {'': 1, 'kb': KILO, 'mb': MEGA, 'gb': GIGA}

    def __init__(self, bytes):
        self.bytes = bytes

    def get_in_unit(self, unit):
        return self.bytes / FileSize.multipliers_to_byte[unit.lower()]

    def get_display_name(self):
        number = self.bytes
        unit = ''

        for u in FileSize.units_reversed:
            if self.bytes >= FileSize.multipliers_to_byte[u] and u:
                number /= FileSize.multipliers_to_byte[u]
                number = round(number, 2)
                unit = u
                break

        if not unit:
            unit = 'b'
        else:
            number = int(number) if number.is_integer() else number

        return '{}{}'.format(number, unit.upper())

    @staticmethod
    def from_string(size_string, separator=''):
        size_string = size_string.lower()

        if separator:
            size_string = ''.join(size_string.split(separator))

        for unit in FileSize.units:
            if unit and unit in size_string:
                size_number, size_unit = size_string.split(unit)[0], unit
                break
        else:
            size_number, size_unit = size_string, ''

        size = int(size_number)

        size_bytes = size * FileSize.multipliers_to_byte[size_unit]

        return FileSize(size_bytes)

    @staticmethod
    def from_int(integer, unit=''):
        return FileSize(integer * FileSize.multipliers_to_byte[unit.lower()])

    def __str__(self):
        return self.get_display_name()
