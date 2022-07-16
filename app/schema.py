""" Graphql Schema Module """
from graphene import (ObjectType, Field, relay, Schema, Argument,
                      Mutation)

from .filters import (FilterConnectionField)
from .schemas.coach import (CoachNode, CoachConnection, CreateCoach,
                            UpdateCoach)
from .schemas.address import (AddressNode, AddressConnection)
from .schemas.field import (FieldNode, FieldConnection)
from .schemas.game import (GameNode, GameConnection)
from .schemas.version import (VersionNode, resolve_version)


class Query(ObjectType):
    """Create Query object list"""
    node = relay.Node.Field()

    coach = relay.Node.Field(CoachNode)
    address = relay.Node.Field(AddressNode)
    field = relay.Node.Field(FieldNode)
    game = relay.Node.Field(GameNode)

    all_coaches = FilterConnectionField(CoachConnection)
    all_addresses = FilterConnectionField(AddressConnection)
    all_fields = FilterConnectionField(FieldConnection)
    all_games = FilterConnectionField(GameConnection)

    version = Field(
        VersionNode,
        resolver=resolve_version
    )


class Mutation(ObjectType):
    """Create Mutation object list"""
    createCoach = CreateCoach.Field()

    updateCoach = UpdateCoach.Field()


SCHEMA = Schema(query=Query, mutation=Mutation)
