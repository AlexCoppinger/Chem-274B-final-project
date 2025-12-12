from banking_system import BankingSystem, Account
from bisect import bisect_right, insort

class BankingSystemImpl(BankingSystem):

    def __init__(self):
        self.accounts = {} # Make a set with the accounts. Key is account_id and it returns account value
        self.spenders = {} # Make a dictionary with spenders
        self.payments = {} # Make dictionary for payments where the key is the transaction string, and value is list of ['timestamp', 'account', 'payment_amount', 'whether_made']
        self.payment_timestamps = {} # Dictionary of dictionary where key is accounts, and second dictionary, key is timestamps. {account_id : { timestamp : [balance, account_open] }} 

    def check_payments(func):
        """
        Payment decorator that checks and updates cashback at every method call
        """
        def wrapper(*args, **kwargs):
            # Get self
            self = args[0]
            # [timestamp, account_id, amount, False]
            for payment in self.payments:
                # args[1] should be timestamp for all methods
                # If the time is larger than 24 hours later and the last element is false (a payment was not made)
                if args[1] >= (self.payments[payment][0] + 86400000) and self.payments[payment][-1] == False:
                    # We know the payment has been made
                    cashback = int(self.payments[payment][2] * 0.02)
                    self.payments[payment][-1] = True
                    self.deposit((self.payments[payment][0] + 86400000), self.payments[payment][1], cashback)
            return func(*args, **kwargs)
        return wrapper

    # Level 1
    @check_payments
    def create_account(self, timestamp: int, account_id: str) -> bool:
        if account_id in self.accounts:
          return False

        self.accounts[account_id] = Account(timestamp, account_id) # Add to the dictionary

        self.spenders[account_id] = 0 # Create new spenders index

        # If the account_id didn't exist before
        if account_id not in self.payment_timestamps:
            self.payment_timestamps[account_id] = {}

        self.update_time_stamps(timestamp, account_id, True)

        return True

    # Level 1
    @check_payments
    def deposit(self, timestamp, account_id, amount):

        if account_id not in self.accounts: # If the account doesn't exist within the dictionary
          return None
        
        account = self.accounts[account_id]
        
        account.balance += amount

        self.update_time_stamps(timestamp, account_id, True)

        return account.balance
    
    # Level 
    @check_payments
    def transfer(self, timestamp, source_account_id, target_account_id, amount):
        # Check if account keys exist:
        if source_account_id not in self.accounts: # If the account doesn't exist within the dictionary
            return None
        if target_account_id not in self.accounts: # If the account doesn't exist within the dictionary
            return None 

        source = self.accounts[source_account_id] # Get source account
        target = self.accounts[target_account_id] # Get target account

        # Checks:
        if source_account_id == target_account_id: # If accounts are the same
            return None
        if source.balance < amount: # Insufficient funds
            return None
        
        source.balance -= amount
        target.balance += amount

        if source_account_id not in self.spenders:
            self.spenders[source_account_id] = amount # Create new index
        else:
            self.spenders[source_account_id] += amount # Add to pre-existing index

        # Update time stamps
        self.update_time_stamps(timestamp, source_account_id, True)
        self.update_time_stamps(timestamp, target_account_id, True)

        return source.balance

    # Level 2
    @check_payments
    def top_spenders(self, timestamp: int, num: int) -> list[str]:
        # sort self.spenders to get top spenders
        sorted_spenders = sorted(self.spenders.items(), key = lambda item: (-item[1], item[0])) # returns keys in alphabetical order
        top_n = [] # List of strings
        
        # It's supposed to be able to go out of range 
        if num > len(sorted_spenders):
            num = len(sorted_spenders)

        for i in range(num):
            top_n.append(f"{sorted_spenders[i][0]}({sorted_spenders[i][1]})")
        
        return top_n
    
    # Level 3
    @check_payments
    def pay(self, timestamp: int, account_id: str, amount: int) -> str | None:
        count = 1 + len(self.payments) # Return the number of payments made in the system for the payment name
        pay_id = f"payment{count}"
        
        # Checks if the account exists or if the amount is too low
        if account_id not in self.accounts or self.accounts[account_id].balance < amount:
            return None
        
        # There is always an account (initialized with 0 in create_accounts)
        # Adding the amount withdrawn from self.spenders[]
        self.spenders[account_id] += amount
        
        # Subtracting amount withdrawn
        self.accounts[account_id].balance -= amount

        # self.payments is dictionary where the key is the 'payment string' with the timestamp, and account_id, and amount withdrawn, and make it false before the day has passed (turn to true when it has)
        self.payments[pay_id] = [timestamp, account_id, amount, False]
        
        # Update timestep balance
        self.update_time_stamps(timestamp, account_id, True)

        return pay_id
    
    # Level 3
    @check_payments
    def get_payment_status(self, timestamp: int, account_id: str, payment: str) -> str | None:
        # Check if payment even exists
        if payment not in self.payments:
            return None
        
        # This is the list of [timestamp, account_id]
        pay_id = self.payments[payment]

        # If it even returns something
        if not self.payments[payment]:
            return None

        # Checks if the account_id in the list even exists
        if pay_id[1] not in self.accounts:
            return None 
        # Checks if the account_id matches the one in the list from the dictionary
        if pay_id[1] != account_id:
            return None
        
        # Check if the payment is processed
        if timestamp < (pay_id[0] + 86400000):
            return "IN_PROGRESS"
        else:
            # Make the deposit at the 'correct time'
            return "CASHBACK_RECEIVED"

    # Level 4 
    @check_payments
    def merge_accounts(self, timestamp: int, account_id_1: str, account_id_2: str) -> bool:
        # Check whether the accounts exist
        if account_id_1 not in self.accounts or account_id_2 not in self.accounts:
            return False
        
        # Check whether account_id_1 is the same as account_id_2
        if self.accounts[account_id_1] == self.accounts[account_id_2]:
            return False
        
        # Merge the balances
        self.accounts[account_id_1].balance += self.accounts[account_id_2].balance
        
        # Merge spending
        self.spenders[account_id_1] += self.spenders[account_id_2]

        # Iterate through the payments dictionary for the account_id and change the account_id for each relevant payment
        for payment in self.payments:
            if self.payments[payment][1] == account_id_2:
                self.payments[payment][1] = account_id_1

        # Merge timestamp_balance
        self.update_time_stamps(timestamp, account_id_1, True)
        self.update_time_stamps(timestamp, account_id_2, False)

        # Delete the account_id_2 values from self.accounts and spending
        del self.accounts[account_id_2]
        del self.spenders[account_id_2]

        return True

    # Level 4
    @check_payments
    def get_balance(self, timestamp: int, account_id: str, time_at: int) -> int | None:
        # Check if account even exists
        if account_id not in self.payment_timestamps: # If the account doesn't exist within the dictionary
            return None

        # binary search implementation:
        times = list(self.payment_timestamps[account_id].keys())   # e.g. [3, 8, 10, 13, ...]
        if not times:
            return None
        
        # binary search part
        i = bisect_right(times, time_at) - 1
        if i < 0:
            return None  # all timestamps are after time_at

        ts = times[i]
        if self.payment_timestamps[account_id][ts][1] == False:
            return None
        else:
            return self.payment_timestamps[account_id][ts][0]

    def update_time_stamps(self, timestamp: int, account_id: str, account_open: bool):
        # Updates the time stamps
        self.payment_timestamps[account_id][timestamp] = [self.accounts[account_id].balance, account_open]