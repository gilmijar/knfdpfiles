"""
Contains classes needed for building up the balance sheet and P&L
objects for the DP1 report
"""

class record:
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
        rendered = f"{self.order}|{self.payload.render()}"
        as_values = tuple(map(int, rendered.encode(self.CHECKSUM_ENCODING)))
        sum_of_values = sum(as_values)
        sum_of_positions = (len(rendered)+1) * (len(rendered)) // 2
        return sum_of_positions+sum_of_values

class position:
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
    

