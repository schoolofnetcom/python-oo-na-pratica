# dependência circular
# from file import MoneySlipsFileReader, MoneySlipsFileWriter
from file import BankAccountFileWriter


class BankAccount:
    def __init__(self, account_number, name, password, value, admin):
        self.account_number = account_number
        self.name = name
        self.password = password
        self.value = value
        self.admin = admin

    def check_account_number(self, account_number):
        return account_number == self.account_number

    def check_password(self, password):
        return password == self.password

    def balance_debit(self, value):
        self.value -= value


class CashMachineInsertMoneyBill:

    @staticmethod
    def insert_money_bill(money_bill, amount):
        cash_machine = CashMachineGetter().get()
        cash_machine.money_slips[money_bill] += amount
        from file import MoneySlipsFileWriter
        MoneySlipsFileWriter().write_money_slips(cash_machine.money_slips)
        return cash_machine


class CashMachineWithDraw:

    @staticmethod
    def withdraw(bank_account, value):
        cash_machine = CashMachineGetter().get()
        money_slips_user = cash_machine.withdraw(value)
        if money_slips_user:
            CashMachineWithDraw.__balance_debit(bank_account, value)
            from file import MoneySlipsFileWriter
            MoneySlipsFileWriter().write_money_slips(cash_machine.money_slips)
        return cash_machine

    @staticmethod
    def __balance_debit(bank_account, value):
        bank_account.balance_debit(value)
        BankAccountFileWriter().write_bank_account(bank_account)


class CashMachineGetter:  # design pattern - factory

    def get(self):
        from file import MoneySlipsFileReader
        money_slips = MoneySlipsFileReader().get_money_slips()
        return CashMachine(money_slips)


class CashMachine:

    def __init__(self, money_slips):
        self.money_slips = money_slips
        self.money_slips_user = {}
        self.value_remaining = 0

    def withdraw(self, value):
        self.value_remaining = value

        self.__calculate_money_slips_user('100')
        self.__calculate_money_slips_user('50')
        self.__calculate_money_slips_user('20')

        if self.value_remaining == 0:
            self.__decrease_money_slips()

        return False if self.value_remaining != 0 else self.money_slips

    def __calculate_money_slips_user(self, money_bill):
        money_bill_int = int(money_bill)
        if 0 < self.value_remaining // money_bill_int <= self.money_slips[money_bill]:
            self.money_slips_user[money_bill] = self.value_remaining // money_bill_int
            self.value_remaining = self.value_remaining - self.value_remaining // money_bill_int * money_bill_int

    def __decrease_money_slips(self):
        for money_bill in self.money_slips_user:
            self.money_slips[money_bill] -= self.money_slips_user[money_bill]


accounts_list = [
    BankAccount('0001-02', 'Fulano da Silva', '123456', 100, False),
    BankAccount('0002-02', 'Cicrano da Silva', '123456', 50, False),
    BankAccount('1111-11', 'Admin da Silva', '123456', 1000, True),
]
