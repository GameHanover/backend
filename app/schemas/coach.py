""" Graphql Coach Schema Module """
from graphene import (String, Boolean, ID, InputObjectType, Node,
                      Field, Mutation, Connection)
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.filters import FilterConnectionField

from app import (DB)
from app.database import (Coach as CoachModel, Address)
from .helpers import (TotalCount, Address as AddressField, input_to_dictionary)


class CoachNode(SQLAlchemyObjectType):
    """ Coach Node """
    class Meta:
        """ Coach Node """
        model = CoachModel
        interfaces = (Node,)
        connection_field_factory = FilterConnectionField.factory

    address = Field(AddressField)

    def resolve_address(self, info):
        ''' address resolver '''
        address = {
            'id': None, 'address1': None, 'address2': None,
            'city': None, 'state': None, 'zip_code': None
        }
        result = DB.session.query(CoachModel).join(Address).filter(
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


class CoachConnection(Connection):
    """Coach Graphql Query output"""
    class Meta:
        """Coach Graphql Query output"""
        node = CoachNode
        interfaces = (TotalCount,)


class CoachAttribute:
    """Coach Input Template """
    first_name = String()
    last_name = String()
    address1 = String()
    address2 = String()
    city = String()
    state = String()
    zip_code = String()
    active = Boolean()


class CreateCoachInput(InputObjectType, CoachAttribute):
    """Create Coach Input fields derived from CoachAttribute"""


class CreateCoach(Mutation):
    """Create Coach Graphql"""
    coach = Field(lambda: CoachNode,
                  description="Coach created by this mutation.")

    class Arguments:
        """Arguments for Create Coach"""
        coach_data = CreateCoachInput(required=True)

    def mutate(self, info, coach_data=None):
        """Create Coach Graphql"""
        data = input_to_dictionary(coach_data)

        coach = CoachModel(**data)
        coach_db = DB.session.query(CoachModel).filter_by(
            description=data['description']).first()
        if coach_db:
            print('need to update')
            coach_db = coach
        else:
            DB.session.add(coach)
        DB.session.commit()

        return CreateCoach(coach=coach)


class UpdateCoachInput(InputObjectType, CoachAttribute):
    """Update Coach Input fields derived from CoachAttribute"""
    id = ID(required=True, description="Global Id of the Coach.")


class UpdateCoach(Mutation):
    """Update Coach Graphql"""
    coach = Field(lambda: CoachNode,
                  description="Coach updated by this mutation.")

    class Arguments:
        """Arguments for Update Coach"""
        coach_data = UpdateCoachInput(required=True)

    def mutate(self, info, coach_data):
        """Update Coach Graphql"""
        data = input_to_dictionary(coach_data)

        coach = DB.session.query(CoachModel).filter_by(id=data['id']).first()
        coach.update(data)
        DB.session.commit()
        coach = DB.session.query(CoachModel).filter_by(id=data['id']).first()

        return UpdateCoach(coach=coach)