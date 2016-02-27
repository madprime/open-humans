from activities.app_configs import UserSocialAuthAppConfig


class FitbitConfig(UserSocialAuthAppConfig):
    """
    Configure the Fitbit activity application.
    """
    name = __package__
    verbose_name = 'Fitbit'

    data_description = {
        'name': 'Health and activity data',
        'description': '',
    }
