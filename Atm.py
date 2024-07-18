class Atm:
    def __init__(self, conn):
        self.__card_no: int
        self.__card_holder: str
        self.__pin: int
        self.__balance: int = 0
        self.__conn = conn


    def fetch_curser(self):
        self.__curser = self.__conn.cursor()
        return self.__curser


    def card_numbers(self, card_no):
        cur = self.fetch_curser()
        cur.execute("SELECT Card_no FROM users")
        cards = cur.fetchall()

        card_numbers = [card[0] for card in cards]
        if card_no in card_numbers:
            self.__card_no = card_no
        else:
            self.__card_no = None
        
        return self.__card_no


    def pin_number(self, card_no):
        cur = self.fetch_curser()
        cur.execute("SELECT Pin FROM users WHERE Card_no = %s", (card_no,))
        pin = cur.fetchone()
        pin = pin[0]

        return pin


    def balance(self, card_no, pin):
        cur = self.fetch_curser()
        cur.execute("SELECT Balance FROM users WHERE Card_no = %s and Pin = %s", (card_no, pin))
        balance = cur.fetchone()
        if balance[0] == None:
            balance = 0
        else:
            balance = balance[0]

        return balance



    def new_user(self, card_no: int, name: str):
        if len(str(card_no)) != 8:
            return {'status': False, 'value': 'Card number must be 8 digit!'}
        if name == '':
            return {'status': False, 'value': 'Name should not be empty!'}

        if len(str(card_no)) == 8 and name != '':
            cur = self.fetch_curser()

            self.__card_no = self.card_numbers(card_no)
            if self.__card_no == card_no:
                return {'status': False, 'value': 'Card number already exists!'}
            else:
                self.__card_no = card_no
                self.__card_holder = name
                cur.execute("""INSERT INTO users (Card_no, Name)
                            VALUES (%s, %s)""", 
                            (self.__card_no, self.__card_holder))
                self.__conn.commit()
                return {'status': True, 'value': 'Account created successfully!'}
        else:
            return {'status': False, 'value': 'Invalid details!'}



    def create_pin(self, card_no: int, pin: int):
        cur = self.fetch_curser()
        self.__card_no = self.card_numbers(card_no)

        if self.__card_no is None and len(str(card_no)) == 8:
            return {'status': False, 'value': 'Account is not Created!'}
        if self.__card_no == card_no:
            self.__pin  = self.pin_number(card_no)

            if self.__pin is None:
                cur.execute("UPDATE users SET Pin = %s WHERE Card_no = %s", (pin, card_no))
                self.__conn.commit()
                return {'status': True, 'value': 'Pin created successfully!'}
            else:
                return {'status': False, 'value': 'Pin already created!'}
        else:
            {'status': False, 'value': 'Invalid card!'}



    def update_pin(self, card_no: int, pin: int):
        cur = self.fetch_curser()
        self.__card_no = self.card_numbers(card_no)
        
        if self.__card_no is None and len(str(card_no)) == 8:
            return {'status': False, 'value': 'Account is not Created!'}
        if self.__card_no == card_no:
            self.__pin  = self.pin_number(card_no)

            if self.__pin is None:
                return {'status': False, 'value': 'Pin is not created!'}
            if self.__pin == pin:
                return {'status': False, 'value': 'New pin should be different!'}
            else:
                cur.execute("UPDATE users SET Pin = %s WHERE Card_no = %s", (pin, card_no))
                self.__conn.commit()
                return {'status': True, 'value': 'Pin updated successfully!'}
        else:
            return {'status': False, 'value': 'Invalid card!'}



    def check_balance(self, card_no: int, pin: int):
        self.__card_no = self.card_numbers(card_no)

        if self.__card_no is None and len(str(card_no)) == 8:
            return {'status': False, 'value': 'Account is not Created!'}
        if self.__card_no == card_no:
            self.__pin  = self.pin_number(card_no)

            if self.__pin is None:
                return {'status': False, 'value': 'Pin is not created!'}
            if self.__pin == pin:
                self.__balance = self.balance(card_no, pin)
                return {'status': True, 'value': f"Your balance is: {self.__balance}"}
            else:
                return {'status': False, 'value': 'Invalid pin!'}
        else:
            return {'status': False, 'value': 'Invalid card!'}


    
    def check_details(self, card_no: int, pin: int):
        self.__card_no = self.card_numbers(card_no)

        if self.__card_no is None and len(str(card_no)) == 8:
            return {'status': False, 'value': 'Account is not Created!'}
        if self.__card_no == card_no:
            self.__pin  = self.pin_number(card_no)

            if self.__pin is None:
                return {'status': False, 'value': 'Pin is not created!'}
            if self.__pin == pin:
                return {'status': True, 'value': "Card and PIN verified successfully!"}
            else:
                return {'status': False, 'value': 'Invalid pin!'}
        else:
            return {'status': False, 'value': 'Invalid card!'}



    def add_money(self, card_no: int, pin: int, amount: float):
        cur = self.fetch_curser()
        self.__balance = self.balance(card_no, pin)

        if amount < 0:
             return {'status': False, 'value': 'Amount cannot be negative!'}
        if amount >= 100000:
            return {'status': False, 'value': 'Amount should be less than 100000'}
        else:
            self.__balance += amount
            cur.execute("UPDATE users SET Balance = %s WHERE Card_no = %s and Pin = %s", (self.__balance, card_no, pin))
            self.__conn.commit()
            return {'status': True, 'value': f'Your balance is {self.__balance}'}



    def withdraw(self, card_no: int, pin: int, amount: float):
        cur = self.fetch_curser()
        self.__balance = self.balance(card_no, pin)

        if amount > self.__balance:
            return {'status': False, 'value': 'Insufficient balance!'}
        if amount < 0:
            return {'status': False, 'value': 'Amount cannot be negative!'}
        if amount >= 100000:
            return {'status': False, 'value': 'Amount should be less than 100000'}
        else:
            self.__balance -= amount
            cur.execute("UPDATE users SET Balance = %s WHERE Card_no = %s and Pin = %s", (self.__balance, card_no, pin))
            self.__conn.commit()
            return {'status': True, 'value': f'You have withdrawn {amount}. Your current balance is {self.__balance}'}



    def card_details(self,card_no):
        cur = self.fetch_curser()
        self.__card_no = self.card_numbers(card_no)

        if self.__card_no is None:
            return {'status': False, 'value': 'Account is not Created!'}
        if self.__card_no == card_no:
            cur.execute("SELECT * FROM users WHERE Card_no = %s", (card_no,))
            details = cur.fetchone()
            details = {'card no' : details[1], 'Holder name' : details[2]}
            return {'status': True, 'value': f'Card no: {details["card no"]}\nHolder name: {details["Holder name"]}'}
        else:
            return {'status': False, 'value': 'Invalid card!'}
