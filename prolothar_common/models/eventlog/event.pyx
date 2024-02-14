from frozendict import frozendict

cdef class Event():
    def __init__(self, activity_name, dict attributes = None,
                 str transition_id = None):
        self.activity_name = activity_name
        self.attributes = attributes if attributes is not None else {}
        self.transition_id = transition_id

    def __repr__(self):
        return '<Event, Activity: %s, transition: %s, attributes=%s>' % (
                self.activity_name, self.transition_id, self.attributes)

    def __eq__(self, other):
        return ((self.activity_name is None and other.activity_name is None or
                self.activity_name == other.activity_name) and
                self.transition_id == other.transition_id and
                self.attributes == other.attributes)

    def __hash__(self):
        return hash((self.activity_name, frozendict(self.attributes)))

    cpdef dict to_dict(self):
        """converts this event to a dictionary, e.g. helpful for json conversion"""
        return {
            'activity_name': self.activity_name,
            'attributes': self.attributes
        }

    @staticmethod
    def create_from_dict(d: dict) -> Event:
        """
        parses a dictionary. the format must be the same as in Event.to_dict
        """
        return Event(d['activity_name'], attributes=d['attributes'])