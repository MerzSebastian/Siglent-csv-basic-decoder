# Author: Sebastian Merz
# Licence: GNU General Public License v3.0
# Description: Script for implementing testing functions to keep the testing code clean
# Example usage:
#   from expect import Expect
#   Expect(1).to_be(1)


class Expect:
    value = ''

    def __init__(self, value):
        self.value = value

    def to_be(self, value):
        if value == self.value:
            print('SUCCESS!')
            return True
        else:
            raise ValueError('Expected', self.value, 'to be', value)
