"""Implements functionality unique to settings profiles"""


class SettingsProfiles:
    """Class for interaction with settings profiles"""

    def __init__(self, device):
        self.device = device

    def create(self, name, description=''):
        """Create a new profile using the present instrument configuration.

        Args:
            name (str): Unique name to give the profile.
            description (str): Optional description of the profile.
        """

        self.device.command('PROFile:CREAte "{}", "{}"'.format(name, description))

    def get_list(self):
        """Returns a list of the saved profile names."""

        response = self.device.query('PROFile:LIST?')
        return [profile.strip('"') for profile in response.split(',')]

    def get_description(self, name):
        """Returns a profile's description.

        Args:
            name (str): Name of the profile to get the description for.
        """

        return self.device.query('PROFile:DESCription? "{}"'.format(name)).strip('"')

    def set_description(self, name, description):
        """Sets a profile's description. Any existing description will be overwritten.

        Args:
            name (str): Name of the profile to get the description for.
            description (str): The new description of the profile.
        """

        self.device.command('PROFile:DESCription "{}","{}"'.format(name, description))

    def get_json(self, name, pretty=False):
        """Returns a JSON string representation of a given profile.

        Args:
            name (str): Name of the profile.
            pretty (bool): True to format the JSON string with indentation and newlines, False for a single line
        """

        response = self.device.query('PROFile:JSON? "{}",{}'.format(name, str(int(pretty))))
        return response.strip('"').replace('""', '"')

    def rename(self, name, new_name):
        """Rename a profile. New name must be unique.

        Args:
            name (str): The name of the profile to rename.
            new_name (str): The new name of the profile.
        """

        self.device.command('PROFile:REName "{}","{}"'.format(name, new_name))

    def update(self, name):
        """Update a profile with the present instrument configuration.

        Args:
            name (str): The name of the profile to update.
        """

        self.device.command('PROFile:UPDate "{}"'.format(name))

    def get_restore_is_valid(self, name):
        """Returns if a profile is valid to restore.

        Args:
            name (str): The name of the profile to validate.
        """

        response = self.device.query('PROFile:RESTore:VALid? "{}"'.format(name))
        return bool(response)

    def restore(self, name):
        """Restore a profile.

        Args:
            name (str): The name of the profile to restore.
        """

        self.device.command('PROFile:RESTore "{}"'.format(name))

    def delete(self, name):
        """Delete a profile

        Args:
            name (str): The name of the profile to delete.
        """

        self.device.command('PROFile:DELete "{}"'.format(name))

    def delete_all(self):
        """Delete all profiles."""

        self.device.command('PROFile:DELete:ALL')
