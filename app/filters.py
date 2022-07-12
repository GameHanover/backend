""" Graphql Filter Module """
from graphene_sqlalchemy_filter import (FilterableConnectionField, FilterSet)
from .database import (Coach as CoachModel)


class CoachFilter(FilterSet):
    """Coach Graphql Filter"""
    class Meta:
        """Coach Graphql Query output"""
        model = CoachModel
        fields = {
            'last_name': ['eq', 'ilike'],
            'first_name': ['eq', 'ilike'],
            'address1': ['eq', 'ilike'],
            'address2': ['eq', 'ilike'],
            'city': ['eq', 'ilike'],
            'state': ['eq', 'ilike'],
            'zip_code': ['eq', 'ilike'],
            'active': ['eq']
        }


class FilterConnectionField(FilterableConnectionField):
    """ Consolidate the filters"""
    filters = {CoachModel: CoachFilter()}
