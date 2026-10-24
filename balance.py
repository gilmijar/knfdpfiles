"""
Contains classes needed for building up the balance sheet and P&L
objects for the DP1 report
"""

class ReportField:
    def __init__(self, field_type, field_size=None, field_decimals=None):
        if field_type == 'N' and field_size is None:
            raise ValueError("Numeric fields must have length specified")
        self.type = field_type
        self.size = field_size
        self.decimals = field_decimals

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, obj, obtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        # TODO add the actual validation - probably need to make subtypes of ReportField
        setattr(obj, self.private_name, value)


class Record:
    """
    Represents a record in the report file
    Knows its contents (can render its payload to text)
    Knows its position in the file
    Can calculate its own checksum
    """
    CHECKSUM_ENCODING = 'ascii'

    def __init__(self, order, payload):
        # TODO move validation to descriptors
        if order > 9999:
            raise ValueError("order (line number) can have at most 4 digits")
        self.payload = payload
        self.order = order

    @property
    def checksum(self):
        """
        Return the checksum of the record contents.
        The checksum is the sum of the character's position in a string and its ordinal number in ASCII 
        (although the file is supposed to be encoded in cp1250)
        """
        rendered = self.render()
        as_values = tuple(map(int, rendered.encode(self.CHECKSUM_ENCODING)))
        sum_of_values = sum(as_values)
        sum_of_positions = ( (len(rendered)+1) * len(rendered) ) // 2
        return sum_of_positions + sum_of_values

    def render(self):
        """Return the string representation of the whole record"""
        return f"{self.order}|{self.payload.render()}"

    def __str__(self):
        return self.render()


class Position:
    """Represent a single position in the report"""
    def __init__(self, code, name, value_old=None, value_now=None):
        """Initialize the position

            Parameters:
                code: alphanumeric position code as defined in the KNF document
                name: textual name/description of the osition as defined in the KNF document
                value_old: alphanumeric, integer or decimal value of the position in previous quarter. Omit to leave unspecified (None)
                value_now: alphanumeric, integer or decimal value of the position in current quarter. Omit to leave unspecified (None)
        """
        self.code = code
        self.name = name
        self.value_old = value_old
        self.value_now = value_now
    
    def render(self):
        # TODO implement render method for Position class
        raise NotImplementedError("need to implement this")
