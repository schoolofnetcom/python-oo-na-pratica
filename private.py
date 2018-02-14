class Test:
    __variavel_static = 'variavel static'

    def __init__(self):
        self.__variavel = 'variavel'

    def __method(self):
        print('method private')

    @staticmethod
    def __method_static():
        print('method static private')
