# Author: Sebastian Merz
# Licence: GNU General Public License v3.0
# Description: Script for implementing testing functions to keep the testing code clean
# Example usage:
#   from expect import Expect
#   Expect(1).to_be(1, "Test1")
#   Expect(1).to_be_not(2, "Test2")
#   Expect([1,2,3]).to_include(2, "Test3")
#   Expect([1,2,3]).to_include_not(5, "Test4")

from colorama import init, Fore, Back, Style
init()

class expect:
    value = ''

    def __init__(self, value):
        self.value = value

    def to_be(self, value, description):
        return self.__to_be(value, description, True)

    def to_be_not(self, value, description):
        return self.__to_be(value, description, False)

    def __to_be(self, value, description, positive):
        status = (value == self.value) if positive else (value != self.value)
        if status:
            print(f'{ Fore.BLACK }{ Back.BLUE }TEST: { Back.GREEN }SUCCESS!: { description }{ Style.RESET_ALL }')
            return True
        else:
            print(f'{ Fore.BLACK }{ Back.BLUE }TEST: { Back.RED }FAILED!: { description }: Expected { self.value } to{ "" if positive else " not"} be { value }{ Style.RESET_ALL }')
            return False

    def to_include(self, value, description):
        return self.__to_include(value, description, True)

    def to_include_not(self, value, description):
        return self.__to_include(value, description, False)

    def __to_include(self, value, description, positive):
        status = (value in self.value) if positive else (value not in self.value)
        if status:
            print(f'{Fore.BLACK}{Back.BLUE}TEST: {Back.GREEN}SUCCESS!: {description}{Style.RESET_ALL}')
            return True
        else:
            print(f'{Fore.BLACK}{Back.BLUE}TEST: {Back.RED}FAILED!: {description}: Expected {self.value} to{"" if positive else " not"} include {value}{Style.RESET_ALL}')
            return False
