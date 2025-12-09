from banking_system import BankingSystem, Account

class BankingSystemImpl(BankingSystem):

    def __init__(self):
        self.accounts = {} # Make a set with the accounts
        self.spenders = {} # Make a dictionary with spenders

    # Level 1
    def create_account(self, timestamp: int, account_id: str) -> bool:
        if account_id in self.accounts:
          return False

        self.accounts[account_id] = Account(timestamp, account_id) # Add to the dictionary

        self.spenders[account_id] = 0 # Create new spenders index

        return True

    # Level 1
    def deposit(self, timestamp, account_id, amount):

        if account_id not in self.accounts: # If the account doesn't exist within the dictionary
          return None
        
        account = self.accounts[account_id]
        
        account.balance += amount

        # account.timestamp = timestamp # set the timestamp????
        # TODO : Potentially add timestamp implementation

        return account.balance
    
    # Level 
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

        # account.timestamp = timestamp # set the timestamp????
        # TODO : Potentially add timestamp implementation

        return source.balance


    # Level 2
    def top_spenders(self, timestamp: int, n_var: int) -> list[str]:
        # sort self.spenders to get top spenders
        sorted_spenders = sorted(self.spenders.items(), key = lambda item: (-item[1], item[0])) # returns keys in alphabetical order
        top_n = [] # List of strings
        breakpoint()
        for i in range(n_var):
            top_n.append(f"{sorted_spenders[i][0]}({sorted_spenders[i][1]})")
        
        # ["account1(50)"]
        return top_n


# system = BankingSystemImpl()
# system.create_account(1, 'account1')
# system.create_account(2, 'account2')
# system.create_account(3, 'account3')
# system.deposit(4, 'account1', 1000), 1000
# system.deposit(5, 'account2', 1000), 1000
# system.deposit(6, 'account3', 1000), 1000
# system.transfer(7, 'account2', 'account3', 100), 900
# system.transfer(8, 'account2', 'account1', 100), 800
# system.transfer(9, 'account3', 'account1', 100), 1000
# expected = ['account2(200)', 'account3(100)', 'account1(0)']
# print(system.top_spenders(10,3))









