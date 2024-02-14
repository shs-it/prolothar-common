from prolothar_common.models.eventlog.event cimport Event

cdef class ComplexEvent(Event):
    """a complex event that exists of a list of subevents or children
    """
    def __init__(self, activity_name, list children,
                 dict attributes = None, str transition_id = None):
        super().__init__(activity_name, attributes=attributes, transition_id=transition_id)
        if not children:
            raise ValueError('children must not be empty')
        self.children = children

    def __eq__(self, other):
        return (self.activity_name == other.activity_name and
                self.children == other.children and
                self.attributes == other.attributes)

    def __hash__(self):
        return hash(self.activity_name)