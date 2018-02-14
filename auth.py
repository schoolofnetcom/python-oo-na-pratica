from cash_machine import accounts_list
from file import BankAccountFileReader


class AuthBankAccount:
    bank_account_authenticated = None

    @staticmethod
    def authenticate(account_number, password):
        bank_account_fr = BankAccountFileReader()
        bank_account = bank_account_fr.get_account(account_number)
        if bank_account and AuthBankAccount.__has_bank_account_valid(bank_account, account_number, password):
            AuthBankAccount.bank_account_authenticated = bank_account
            return bank_account
        return False

    @staticmethod
    def __has_bank_account_valid(bank_account, account_number, password):
        return bank_account.check_account_number(account_number) and \
               bank_account.check_password(password)


