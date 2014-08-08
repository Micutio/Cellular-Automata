__author__ = 'Michael Wagner'
__version__ = '1.0'


class Tribes:
    """
    Standard initializer
    """
    def __init__(self, num_tribes):
        self.num_tribes = num_tribes
        self.total_cells = 2500
        self.tribal_wealth = {}
        self.tribal_area = {}
        for i in range(-1, self.num_tribes):
            self.tribal_wealth[i] = 0
            self.tribal_area[i] = 0

    def can_conquer(self, tribe_id):
        """
        Determines whether the tribe 'tribe_id' has
        enough power (wealth) to conquer more territories.
        :param tribe_id: ID of tribe.
        :return: True or False
        """
        tribal_wealth = self.tribal_wealth[tribe_id]
        total_wealth = 0
        for _, w in self.tribal_wealth.items():
            total_wealth += w

        if total_wealth != 0:
            possible_area = tribal_wealth * self.total_cells / total_wealth
        else:
            possible_area = 0
        conquest_possible = possible_area > self.tribal_area[tribe_id]
        return conquest_possible

    def can_defend(self, tribe_id):
        """
        Determines whether the tribe 'tribe_id' has
        enough power (wealth) to defend its territories.
        Even though it basically is identical to can_conquer,
        it has been given a different name for clarity.
        :param tribe_id: ID of tribe.
        :return: True or False
        """
        result = self.can_conquer(tribe_id)
        return result