""" Graphql Game Schema Module """
from graphene import (String, Boolean, ID, InputObjectType, Node,
                      Field, Mutation, Connection)
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.filters import FilterConnectionField

from app import (DB)
from app.database import (Game as GameModel, Address)
from .helpers import (TotalCount, Address as AddressField, input_to_dictionary)


class GameNode(SQLAlchemyObjectType):
    """ Game Node """
    class Meta:
        """ Game Node """
        model = GameModel
        interfaces = (Node,)
        connection_field_factory = FilterConnectionField.factory

    address = Field(AddressField)

    def resolve_address(self, info):
        ''' address resolver '''
        address = {
            'id': None, 'address1': None, 'address2': None,
            'city': None, 'state': None, 'zip_code': None
        }
        result = DB.session.query(GameModel).join(Address).filter(
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


class GameConnection(Connection):
    """Game Graphql Query output"""
    class Meta:
        """Game Graphql Query output"""
        node = GameNode
        interfaces = (TotalCount,)


class GameAttribute:
    """Game Input Template """
    first_name = String()
    last_name = String()
    address1 = String()
    address2 = String()
    city = String()
    state = String()
    zip_code = String()
    active = Boolean()


class CreateGameInput(InputObjectType, GameAttribute):
    """Create Game Input fields derived from GameAttribute"""


class CreateGame(Mutation):
    """Create Game Graphql"""
    Game = Field(lambda: GameNode,
                  description="Game created by this mutation.")

    class Arguments:
        """Arguments for Create Game"""
        Game_data = CreateGameInput(required=True)

    def mutate(self, info, Game_data=None):
        """Create Game Graphql"""
        data = input_to_dictionary(Game_data)

        Game = GameModel(**data)
        Game_db = DB.session.query(GameModel).filter_by(
            description=data['description']).first()
        if Game_db:
            print('need to update')
            Game_db = Game
        else:
            DB.session.add(Game)
        DB.session.commit()

        return CreateGame(Game=Game)


class UpdateGameInput(InputObjectType, GameAttribute):
    """Update Game Input fields derived from GameAttribute"""
    id = ID(required=True, description="Global Id of the Game.")


class UpdateGame(Mutation):
    """Update Game Graphql"""
    Game = Field(lambda: GameNode,
                  description="Game updated by this mutation.")

    class Arguments:
        """Arguments for Update Game"""
        Game_data = UpdateGameInput(required=True)

    def mutate(self, info, Game_data):
        """Update Game Graphql"""
        data = input_to_dictionary(Game_data)

        Game = DB.session.query(GameModel).filter_by(id=data['id']).first()
        Game.update(data)
        DB.session.commit()
        Game = DB.session.query(GameModel).filter_by(id=data['id']).first()

        return UpdateGame(Game=Game)