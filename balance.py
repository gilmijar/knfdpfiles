"""
Contains classes needed for building up the balance sheet and P&L
objects for the DP1 report
"""

class ReportField:
    def __init__(self, field_size, field_decimals=None):
        if field_size is None:
            raise ValueError("Fields must have length specified")
        self.type = None
        self.size = field_size
        self.decimals = field_decimals

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, obj, obtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        raise NotImplementedError("Did you forget to implement the setter?")


class FieldAlphaNumeric(ReportField):
    def __set__(self, obj, value):
        if len(value) > self.size:
            raise ValueError(
                "Alphanumeric field's value too big. "
                f"{self.public_name} received a value of {len(value)} characters, "
                f"but only {self.size} is allowed."
            )
        setattr(obj, self.private_name, value)


class FieldNumeric(ReportField):
    def __set__(self, obj, value):
        if len(str(value)) > self.size:
            raise ValueError(
                "Numeric field's value too big. "
                f"Tried to put '{value}' in {self.public_name}, "
                f"which only allows {self.size} characters, including the sign."
            )
        setattr(obj, self.private_name, value)


class FieldDecimal(ReportField):
    DEC_SEP = ','

    def __init__(self, field_size, field_decimals):
        super().__init__(field_size, field_decimals)
    
    def __set__(self, obj, value):
        value_string = str(value)
        value_int, _, value_dec = value_string.partition(self.DEC_SEP)
        if len(value_dec) > self.decimals:
            raise ValueError(
                "Decimal field has too many decimals. "
                f"Tried to put '{value}' in {self.public_name}, "
                f"which only allows {self.decimals} decimal places."
            )
        if len(value_int) > ( self.size-1-self.decimals ):
            raise ValueError(
                "Decimal field is too long. "
                f"Tried to put '{value}' in {self.public_name}, "
                f"which only allows {self.size} characters in all, including the sign."
            )
        setattr(obj, self.private_name, value)


class Record:
    """
    Represents a record in the report file
    Knows its contents (can render its payload to text)
    Knows its position in the file
    Can calculate its own checksum
    """
    CHECKSUM_ENCODING = 'ascii'
    order = FieldNumeric(4)

    def __init__(self, order, payload):
        if not payload:
            raise ValueError("Record must have a value.")
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
        sum_of_values = sum(map(int, rendered.encode(self.CHECKSUM_ENCODING)))
        sum_of_positions = ( (len(rendered)+1) * len(rendered) ) // 2
        return sum_of_positions + sum_of_values

    def render(self):
        """Return the string representation of the whole record"""
        return f"{self.order}|{self.payload}"

    def __str__(self):
        return self.render()


class Position:
    """Represent a single position in the report"""
    def __init__(self, code, name, value_old=None, value_now=None):
        """
            Initialize the position

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
        return f"{self.code}|{self.value_old}|{self.value_now}|"

    def __str__(self):
        return self.render()
