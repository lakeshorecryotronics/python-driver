"""Implements functionality unique to settings profiles."""

import json


class SettingsProfiles:
    """Class for interaction with settings profiles."""

    def __init__(self, device):
        self.device = device

    def get_summary(self, name):
        """Returns a list containing a profile's description and module models.

        Args:
            name (str):
                Name of the profile to query.
        """

        response = self.device.query(f'PROFile:SUMMary? "{name}"')

        return [element.replace('"', '').strip() for element in response.split(',')]

    def create(self, name, description=''):
        """Create a new profile using the present instrument configuration.

        Args:
            name (str):
                Unique name to give the profile.
            description (str):
                Optional description of the profile.
        """

        self.device.command(f'PROFile:CREAte "{name}", "{description}"')

    def get_list(self):
        """Returns a list of the saved profile names."""

        response = self.device.query('PROFile:LIST?')
        if not response:
            return []

        return [profile.strip('"') for profile in response.split(',')]

    def get_description(self, name):
        """Returns a profile's description.

        Args:
            name (str):
                Name of the profile to get the description for.
        """

        return self.device.query(f'PROFile:DESCription? "{name}"').strip('"')

    def set_description(self, name, description):
        """Sets a profile's description. Any existing description will be overwritten.

        Args:
            name (str):
                Name of the profile to get the description for.
            description (str):
                The new description of the profile.
        """

        self.device.command(f'PROFile:DESCription "{name}","{description}"')

    def get_json(self, name):
        """Returns a JSON object of a given profile.

        Args:
            name (str):
                Name of the profile.
        """

        response = self.device.query(f'PROFile:JSON? "{name}"')
        json_string = response.strip('"').replace('""', '"')
        return json.loads(json_string)

    def rename(self, name, new_name):
        """Rename a profile. New name must be unique.

        Args:
            name (str):
                The name of the profile to rename.
            new_name (str):
                The new name of the profile.
        """

        self.device.command(f'PROFile:REName "{name}","{new_name}"')

    def update(self, name):
        """Update a profile with the present instrument configuration.

        Args:
            name (str):
                The name of the profile to update.
        """

        self.device.command(f'PROFile:UPDate "{name}"')

    def get_valid_for_restore(self, name):
        """Returns if a profile is valid to restore.

        Args:
            name (str):
                The name of the profile to validate.
        """

        response = self.device.query(f'PROFile:RESTore:VALid? "{name}"')
        return bool(response)

    def restore(self, name):
        """Restore a profile.

        Args:
            name (str):
                The name of the profile to restore.
        """

        self.device.command(f'PROFile:RESTore "{name}"')

    def delete(self, name):
        """Delete a profile.

        Args:
            name (str):
                The name of the profile to delete.
        """

        self.device.command(f'PROFile:DELete "{name}"')

    def delete_all(self):
        """Delete all profiles."""

        self.device.command('PROFile:DELete:ALL')
