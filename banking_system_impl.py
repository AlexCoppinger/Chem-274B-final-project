from banking_system import BankingSystem, Account

class BankingSystemImpl(BankingSystem):

    def __init__(self):
        super().__init__()

    def create_account(self, timestamp: int, account_id: str) -> bool:
        if account_id in self.accounts:
          return False

        self.accounts[account_id] = Account(timestamp, account_id) # Add to the dictionary
        return True

    def deposit(self, timestamp, account_id, amount):

        if account_id not in self.accounts: # If the account doesn't exist within the dictionary
          return None
        
        account = self.accounts[account_id]
        
        account.balance += amount

        # account.timestamp = timestamp # set the timestamp????
        # TODO : Potentially add timestamp implementation

        return account.balance
    
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

        # account.timestamp = timestamp # set the timestamp????
        # TODO : Potentially add timestamp implementation

        return source.balance

