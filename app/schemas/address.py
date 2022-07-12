from graphene import (Node, Connection)
from app.database import (Address as AddressModel)
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.filters import FilterConnectionField
from .helpers import (TotalCount)


class AddressNode(SQLAlchemyObjectType):
    """ Address Node """
    class Meta:
        """ Address Node """
        model = AddressModel
        interfaces = (Node,)
        connection_field_factory = FilterConnectionField.factory


class AddressConnection(Connection):
    """Address Graphql Query output"""
    class Meta:
        """Address Graphql Query output"""
        node = AddressNode
        interfaces = (TotalCount,)

