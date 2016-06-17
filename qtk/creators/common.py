from qtk.common import FieldName, DataType


class CreatorBaseMeta(type):

    def __new__(meta, name, bases, dct):
        return super(CreatorBaseMeta, meta).__new__(meta, name, bases, dct)

    def __init__(self, name, bases, dct):
        templates = dct.get("_templates")
        if templates is not None:
            if isinstance(templates, list):
                for t in templates:
                    t._set_creator(self)
            else:
                raise ValueError("_template not of type list")
        elif name != "CreatorBase":
            raise AttributeError("Expected _templates class variable definition for creator ", self)

        req_fields = dct.get("_req_fields")
        if req_fields is not None:
            if isinstance(req_fields, list):
                pass
            else:
                raise ValueError("_req_fields not of type list")
        elif name != "CreatorBase":
            raise AttributeError("Expected _req_fields class variable definition for creator ", self)

        """
        opt_fields = dct.get("_opt_fields")
        if opt_fields is not None:
            if isinstance(opt_fields, list):
                t._set_opt_fields(opt_fields)
            else:
                raise ValueError("_opt_fields not of type list")
        """

        super(CreatorBaseMeta, self).__init__(name, bases, dct)


class CreatorBase(object):
    """
    Every creator must inherit this class. This class adds properties
    to link every template with a creator in an automated way. In order
    to do this, every class that inherits CreatorBase must define a variable
    "_templates" which is a list of all templates that it can instantiate.
    """
    __metaclass__ = CreatorBaseMeta

    def __init__(self, data, params=None):
        """

        :param data:
        :param params:
        :return:
        """

        self._data = data
        self._params = params or {}

    @classmethod
    def get_templates(cls):
        return cls._templates

    @classmethod
    def get_req_fields(cls):
        from qtk.fields import Field
        return [Field.TEMPLATE] + cls._req_fields

    @classmethod
    def _check_fields(cls, data):
        missing_fields = set(cls.get_req_fields(), set(data.keys()))
        if len(missing_fields):
            raise AttributeError("Missing fields in data " + ", ".join([mf.id for mf in missing_fields]))
        return True

    @classmethod
    def _check_convert_datatypes(cls, data):
        for field_id, val in data.iteritems():
            field = FieldName.lookup(field_id)
            cnvrt_val = field.data_type.convert(val)
            data[field_id] = cnvrt_val

            if field.data_type == DataType.LIST:
                data[field_id] = [cls._check_convert_datatypes(v) for v in cnvrt_val]

        return data

    def check(self):
        self._check_fields(self._data)
        self._check_convert_datatypes(self._data)



