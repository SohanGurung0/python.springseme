from read import save_inventory
from write import generate_sales_invoice, generate_restock_invoice, list_invoices, read_invoice
from typing import List, Dict

def display_inventory(shoes_data: List[Dict]):
	"""Display current shoe inventory"""
	if not shoes_data:
		print("No shoes in inventory.")
		return
	
	print("\n" + "="*80)
	print("CURRENT SHOE INVENTORY")
	print("="*80)
	print(f"{'No.':<4} {'Shoe Type':<20} {'Brand':<15} {'Qty':<6} {'Price':<10} {'Origin':<12}")
	print("-"*80)
	
	for i, shoe in enumerate(shoes_data, 1):
		print(f"{i:<4} {shoe['type']:<20} {shoe['brand']:<15} {shoe['quantity']:<6} ${shoe['price']:<9.2f} {shoe['origin']:<12}")
	print("="*80)

def calculate_discount(quantity: int, price: float, origin: str):
	"""Calculate discount based on quantity and origin"""
	try:
		total = quantity * price
	except TypeError:
		return 0.0, 0.0, 0.0, 0.0
	discount_rate = 0
	
	if quantity > 10:
		if origin.lower() == 'domestic':
			discount_rate = 0.07  # 7% for domestic products
		else:
			discount_rate = 0.05  # 5% for international products
	
	discount_amount = total * discount_rate
	final_total = total - discount_amount
	
	return total, discount_amount, discount_rate, final_total

def process_sale(shoes_data: List[Dict]):
	"""Process a customer sale transaction and return updated shoes data"""
	print("\n" + "="*50)
	print("PROCESS SALE")
	print("="*50)
	
	display_inventory(shoes_data)
	
	try:
		# Get customer information
		customer_name = input("\nEnter customer name: ").strip()
		if not customer_name:
			print("Customer name cannot be empty.")
			return shoes_data
		
		# Select shoe
		shoe_index_input = input("Enter shoe number to sell: ").strip()
		if not shoe_index_input.isdigit():
			print("Invalid input. Please enter a number.")
			return shoes_data
		shoe_index = int(shoe_index_input) - 1
		if shoe_index < 0 or shoe_index >= len(shoes_data):
			print("Invalid shoe selection.")
			return shoes_data
		
		selected_shoe = shoes_data[shoe_index]
		
		# Get quantity
		quantity_input = input(f"Enter quantity to sell (Available: {selected_shoe['quantity']}): ").strip()
		if not quantity_input.isdigit():
			print("Invalid quantity. Please enter a whole number.")
			return shoes_data
		quantity = int(quantity_input)
		if quantity <= 0:
			print("Quantity must be positive.")
			return shoes_data
		if quantity > selected_shoe['quantity']:
			print("Not enough stock available.")
			return shoes_data
		
		# Calculate totals and discounts
		subtotal, discount_amount, discount_rate, final_total = calculate_discount(
			quantity, selected_shoe['price'], selected_shoe['origin']
		)
		
		# Update inventory
		selected_shoe['quantity'] -= quantity
		save_inventory(shoes_data)
		
		# Generate invoice and show it
		invoice_path = generate_sales_invoice(customer_name, selected_shoe, quantity, subtotal, discount_amount, discount_rate, final_total)
		
		print(f"\nSale completed successfully!")
		print(f"Remaining stock for {selected_shoe['type']}: {selected_shoe['quantity']}")
		if invoice_path:
			print("\n--- Sales Invoice ---")
			print(read_invoice(invoice_path))
		
	except (EOFError, KeyboardInterrupt):
		print("\nOperation cancelled.")
	except ValueError:
		print("Please enter valid numbers.")
	except Exception as e:
		print(f"Error processing sale: {e}")
	
	return shoes_data

def restock_inventory(shoes_data: List[Dict]):
	"""Add new stock from suppliers and return updated shoes data"""
	print("\n" + "="*50)
	print("RESTOCK INVENTORY")
	print("="*50)
	
	try:
		# Get supplier information
		supplier_name = input("Enter supplier name: ").strip()
		if not supplier_name:
			print("Supplier name cannot be empty.")
			return shoes_data
		
		# Get shoe details
		shoe_type = input("Enter shoe type: ").strip()
		brand = input("Enter brand: ").strip()
		quantity_input = input("Enter quantity to add: ").strip()
		price_input = input("Enter unit price: $").strip()
		origin = input("Enter origin (Domestic/International): ").strip()
		if not quantity_input.isdigit():
			print("Invalid quantity. Please enter a whole number.")
			return shoes_data
		quantity = int(quantity_input)
		try:
			price = float(price_input)
		except ValueError:
			print("Invalid price. Please enter a numeric value.")
			return shoes_data
		
		if not all([shoe_type, brand, origin]) or quantity <= 0 or price <= 0:
			print("All fields must be filled with valid values.")
			return shoes_data
		
		# Check if shoe already exists
		existing_shoe = None
		for shoe in shoes_data:
			if shoe['type'].lower() == shoe_type.lower() and shoe['brand'].lower() == brand.lower():
				existing_shoe = shoe
				break
		
		if existing_shoe:
			# Update existing shoe
			existing_shoe['quantity'] += quantity
			existing_shoe['price'] = price  # Update price
			existing_shoe['origin'] = origin  # Update origin
			print(f"Updated existing shoe: {shoe_type}")
		else:
			# Add new shoe
			new_shoe = {
				'type': shoe_type,
				'brand': brand,
				'quantity': quantity,
				'price': price,
				'origin': origin
			}
			shoes_data.append(new_shoe)
			print(f"Added new shoe: {shoe_type}")
		
		# Save inventory
		save_inventory(shoes_data)
		
		# Generate restock invoice and show it
		invoice_path = generate_restock_invoice(supplier_name, shoe_type, brand, quantity, price, origin)
		
		print("Restocking completed successfully!")
		if invoice_path:
			print("\n--- Restock Invoice ---")
			print(read_invoice(invoice_path))
	
	except (EOFError, KeyboardInterrupt):
		print("\nOperation cancelled.")
	except ValueError:
		print("Please enter valid numbers for quantity and price.")
	except Exception as e:
		print(f"Error during restocking: {e}")
	
	return shoes_data

def view_invoices_menu():
	"""Simple invoice viewer menu."""
	print("\n" + "="*50)
	print("INVOICE VIEWER")
	print("="*50)
	print("1. View latest invoices (all)")
	print("2. View sales invoices")
	print("3. View restock invoices")
	print("4. Back")
	print("-"*50)
	choice = input("Enter your choice (1-4): ").strip()
	if choice not in {'1','2','3','4'}:
		print("Invalid choice.")
		return
	if choice == '4':
		return
	invoice_type = None
	if choice == '2':
		invoice_type = 'sales'
	elif choice == '3':
		invoice_type = 'restock'
	files = list_invoices(invoice_type)
	if not files:
		print("No invoices found.")
		return
	print(f"Found {len(files)} invoice(s). Showing up to 5.")
	for path in files[:5]:
		print("\n--- " + path + " ---")
		print(read_invoice(path))


