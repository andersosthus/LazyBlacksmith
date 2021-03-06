# -*- encoding: utf-8 -*-
from flask_login import LoginManager
from flask_login import AnonymousUserMixin
from lazyblacksmith.models import User
from lazyblacksmith.models import UserPreference


class LazyAnonymous(AnonymousUserMixin):
    """ extends anonymous user mixin to define default values used everywhere
    such as userpreferences, without persisting anything """
    
    def __init__(self):
        # set default values to preferences (as we need to do it)
        self.pref = UserPreference()
        self.pref.invention_facility = 0
        self.pref.invention_invention_rig = 0
        self.pref.invention_copy_rig = 0
        self.pref.invention_security = 'h'
        self.pref.invention_system = 'Jita'
        self.pref.invention_price_region = 10000002    
        self.pref.invention_price_type = 'buy'     
        self.pref.research_facility = 0
        self.pref.research_me_rig = 0
        self.pref.research_te_rig = 0
        self.pref.research_copy_rig = 0
        self.pref.research_security = 'h'
        self.pref.research_system = 'Jita'
        self.pref.prod_facility = 0
        self.pref.prod_me_rig = 0
        self.pref.prod_te_rig = 0
        self.pref.prod_security = 'h'
        self.pref.prod_system = 'Jita'
        self.pref.prod_sub_facility = 0
        self.pref.prod_sub_me_rig = 0
        self.pref.prod_sub_te_rig = 0
        self.pref.prod_sub_security = 'h'
        self.pref.prod_sub_system = 'Jita'
        self.pref.prod_price_region_minerals = 10000002
        self.pref.prod_price_region_pi = 10000002    
        self.pref.prod_price_region_moongoo = 10000002    
        self.pref.prod_price_region_others = 10000002     
        self.pref.prod_price_type_minerals = 'buy'    
        self.pref.prod_price_type_pi = 'buy'    
        self.pref.prod_price_type_moongoo = 'buy'    
        self.pref.prod_price_type_others = 'buy'


login_manager = LoginManager()
login_manager.anonymous_user = LazyAnonymous
login_manager.login_view = 'sso.login'


@login_manager.user_loader
def load_user(character_id):
    return User.query.get(character_id)

    
    