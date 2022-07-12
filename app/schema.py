""" Graphql Schema Module """
from graphene import (ObjectType, String, Field, relay, Schema, Argument,
                      Mutation)

from .filters import (FilterConnectionField)
from .schemas.coach import (CoachNode, CoachConnection, CreateCoach,
                            UpdateCoach)
from .schemas.address import (AddressNode, AddressConnection)


class Query(ObjectType):
    """Create Query object list"""
    node = relay.Node.Field()

    coach = relay.Node.Field(CoachNode)
    address = relay.Node.Field(AddressNode)

    all_coach = FilterConnectionField(CoachConnection)
    all_address = FilterConnectionField(AddressConnection)


class Mutation(ObjectType):
    """Create Mutation object list"""
    createCoach = CreateCoach.Field()

    updateCoach = UpdateCoach.Field()


SCHEMA = Schema(query=Query, mutation=Mutation)
