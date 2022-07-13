""" Graphql Field Schema Module """
from graphene import (String, Boolean, ID, InputObjectType, Node,
                      Field, Mutation, Connection)
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.filters import FilterConnectionField

from helpers.utils import (input_to_dictionary)
from app import (DB)
from app.database import (Field as FieldModel, Address)
from .helpers import (TotalCount, Address as AddressField)


class FieldNode(SQLAlchemyObjectType):
    """ Field Node """
    class Meta:
        """ Field Node """
        model = FieldModel
        interfaces = (Node,)
        connection_field_factory = FilterConnectionField.factory

    address = Field(AddressField)

    def resolve_address(self, info):
        ''' address resolver '''
        address = {
            'id': None, 'address1': None, 'address2': None,
            'city': None, 'state': None, 'zip_code': None
        }
        result = DB.session.query(FieldModel).join(Address).filter(
            Address.id == self.address_id)
        for row in result:
            address = {
                'id': self.address_id,
                'address1': row.address.address1,
                'address2': row.address.address2,
                'city': row.address.city,
                'state': row.address.state,
                'zip_code': row.address.zip_code
            }

        return address


class FieldConnection(Connection):
    """Field Graphql Query output"""
    class Meta:
        """Field Graphql Query output"""
        node = FieldNode
        interfaces = (TotalCount,)


class FieldAttribute:
    """Field Input Template """
    name = String()
    address = Field(AddressField)


class CreateFieldInput(InputObjectType, FieldAttribute):
    """Create Field Input fields derived from FieldAttribute"""


class CreateField(Mutation):
    """Create Field Graphql"""
    Field = Field(lambda: FieldNode,
                  description="Field created by this mutation.")

    class Arguments:
        """Arguments for Create Field"""
        Field_data = CreateFieldInput(required=True)

    def mutate(self, info, Field_data=None):
        """Create Field Graphql"""
        data = input_to_dictionary(Field_data)

        Field = FieldModel(**data)
        Field_db = DB.session.query(FieldModel).filter_by(
            description=data['description']).first()
        if Field_db:
            print('need to update')
            Field_db = Field
        else:
            DB.session.add(Field)
        DB.session.commit()

        return CreateField(Field=Field)


class UpdateFieldInput(InputObjectType, FieldAttribute):
    """Update Field Input fields derived from FieldAttribute"""
    id = ID(required=True, description="Global Id of the Field.")


class UpdateField(Mutation):
    """Update Field Graphql"""
    Field = Field(lambda: FieldNode,
                  description="Field updated by this mutation.")

    class Arguments:
        """Arguments for Update Field"""
        Field_data = UpdateFieldInput(required=True)

    def mutate(self, info, Field_data):
        """Update Field Graphql"""
        data = input_to_dictionary(Field_data)

        Field = DB.session.query(FieldModel).filter_by(id=data['id']).first()
        Field.update(data)
        DB.session.commit()
        Field = DB.session.query(FieldModel).filter_by(id=data['id']).first()

        return UpdateField(Field=Field)
