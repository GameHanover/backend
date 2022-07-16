""" Graphql Version Schema Module """
from graphene import (String, ObjectType, Connection)


def resolve_version(parent, info):
    with open('VERSION') as v:
        version = v.read().replace('\n', '')

    return VersionNode(
        version=version
    )


class VersionNode(ObjectType):
    """ Version Graphql Node output """
    version = String()


class VersionConnection(Connection):
    """ Version Connection """
    class Meta:
        """ Version Connection """
        node = VersionNode
