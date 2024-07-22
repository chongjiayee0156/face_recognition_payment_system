from tkinter import messagebox

# Function to handle the payment confirmation
def confirm_payment(user, total_price=10):

    # Simulate transaction completion
    try:
        complete_transaction(user, total_price)
        messagebox.showinfo("Payment Confirmation", f"Payment has been completed. Your new balance is {user['balance']}")
    except Exception as e:
        messagebox.showerror("Payment Error", f'{e}')
        
    print("Payment has been confirmed!")
    
def complete_transaction(user, total_price=10):
    # Simulate a transaction completion
    if user['balance'] >= total_price:
        user['balance'] -= total_price
    else:
        raise Exception("Insufficient funds in account")

    

