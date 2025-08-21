from read import load_inventory
from operations import display_inventory, process_sale, restock_inventory, view_invoices_menu

def main_menu():
	"""Display main menu and handle user choices"""
	# Load inventory at startup
	shoes_data = load_inventory()
	
	while True:
		print("\n" + "="*50)
		print("SHOES WHOLESALE SYSTEM")
		print("="*50)
		print("1. Display Inventory")
		print("2. Process Sale")
		print("3. Restock Inventory")
		print("4. View Invoices")
		print("5. Exit")
		print("-"*50)
		
		try:
			choice = input("Enter your choice (1-5): ").strip()
			if choice == "":
				print("Please enter a choice.")
				continue
			
			if choice == '1':
				display_inventory(shoes_data)
			elif choice == '2':
				shoes_data = process_sale(shoes_data)
			elif choice == '3':
				shoes_data = restock_inventory(shoes_data)
			elif choice == '4':
				view_invoices_menu()
			elif choice == '5':
				print("Thank you for using Shoes Wholesale System!")
				break
			else:
				print("Invalid choice. Please enter 1-5.")
				
		except (EOFError, KeyboardInterrupt):
			print("\n\nExiting system...")
			break
		except Exception as e:
			print(f"An error occurred: {e}")

def main():
	"""Main function to run the Shoes Wholesale System"""
	print("Welcome to the Shoes Wholesale System!")
	main_menu()

if __name__ == "__main__":
	main()


