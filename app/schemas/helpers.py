""" Includes Row Count in Graphql Queries """
from graphene import (Interface, Int, String, ID, ObjectType)
from graphql_relay.node.node import from_global_id


def input_to_dictionary(input_value):
    """Method to convert Graphene inputs into dictionary"""
    dictionary = {}
    for key in input_value:
        # Convert GraphQL global id to database id
        if key[-2:] == 'id':
            input_value[key] = from_global_id(input_value[key])[1]
        dictionary[key] = input_value[key]
    return dictionary


def must_not_be_blank(data):
    """Customer validator to ensure data isn't blank """
    if not data:
        raise ValueError('Data not provided.')


class TotalCount(Interface):
    """ Return Row Count """
    total_count = Int()

    def resolve_total_count(self, info):
        """  Return Row Count """
        return self.length


class Address(ObjectType):
    """ Address Graphql Attributes for Fields and Coaches"""
    id = ID()
    address1 = String()
    address2 = String()
    city = String()
    state = String()
    zip_code = String()
