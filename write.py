from datetime import datetime
import os


def _ensure_invoice_dir(path: str) -> None:
	"""Ensure the directory for the given path exists."""
	directory = os.path.dirname(path)
	if directory and not os.path.exists(directory):
		try:
			os.makedirs(directory, exist_ok=True)
		except Exception as e:
			raise RuntimeError(f"Cannot create invoice directory '{directory}': {e}")

def generate_sales_invoice(customer_name, shoe, quantity, subtotal, discount_amount, discount_rate, final_total):
	"""Generate sales invoice and save to file"""
	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	invoice_filename = f"scripts/sales_invoice_{timestamp}.txt"
	_ensure_invoice_dir(invoice_filename)
	
	try:
		with open(invoice_filename, 'w', encoding='utf-8') as file:
			file.write("="*60 + "\n")
			file.write("SHOES WHOLESALE SYSTEM - SALES INVOICE\n")
			file.write("="*60 + "\n")
			file.write(f"Invoice Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
			file.write(f"Customer Name: {customer_name}\n")
			file.write("-"*60 + "\n")
			file.write("ITEM DETAILS:\n")
			file.write(f"Shoe Type: {shoe['type']}\n")
			file.write(f"Brand: {shoe['brand']}\n")
			file.write(f"Origin: {shoe['origin']}\n")
			file.write(f"Unit Price: ${shoe['price']:.2f}\n")
			file.write(f"Quantity: {quantity}\n")
			file.write("-"*60 + "\n")
			file.write("PRICING BREAKDOWN:\n")
			file.write(f"Subtotal: ${subtotal:.2f}\n")
			if discount_amount > 0:
				file.write(f"Discount ({discount_rate*100:.0f}%): -${discount_amount:.2f}\n")
			file.write(f"TOTAL AMOUNT: ${final_total:.2f}\n")
			file.write("="*60 + "\n")
			file.write("Thank you for your business!\n")
		
		print(f"Sales invoice saved as: {invoice_filename}")
		return invoice_filename
	except Exception as e:
		print(f"Error generating invoice: {e}")
		return None

def generate_restock_invoice(supplier_name, shoe_type, brand, quantity, price, origin):
	"""Generate restock invoice and save to file"""
	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	invoice_filename = f"scripts/restock_invoice_{timestamp}.txt"
	_ensure_invoice_dir(invoice_filename)
	
	try:
		total_cost = quantity * price
		
		with open(invoice_filename, 'w', encoding='utf-8') as file:
			file.write("="*60 + "\n")
			file.write("SHOES WHOLESALE SYSTEM - RESTOCK INVOICE\n")
			file.write("="*60 + "\n")
			file.write(f"Restock Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
			file.write(f"Supplier Name: {supplier_name}\n")
			file.write("-"*60 + "\n")
			file.write("ITEM DETAILS:\n")
			file.write(f"Shoe Type: {shoe_type}\n")
			file.write(f"Brand: {brand}\n")
			file.write(f"Origin: {origin}\n")
			file.write(f"Unit Price: ${price:.2f}\n")
			file.write(f"Quantity Added: {quantity}\n")
			file.write("-"*60 + "\n")
			file.write(f"TOTAL COST: ${total_cost:.2f}\n")
			file.write("="*60 + "\n")
			file.write("Stock successfully added to inventory.\n")
		
		print(f"Restock invoice saved as: {invoice_filename}")
		return invoice_filename
	except Exception as e:
		print(f"Error generating restock invoice: {e}")
		return None

def list_invoices(invoice_type=None):
	"""Return a list of invoice file paths sorted by modified time (desc).

	invoice_type can be 'sales', 'restock', or None for all.
	"""
	scripts_dir = os.path.join(os.getcwd(), 'scripts')
	if not os.path.isdir(scripts_dir):
		return []
	try:
		all_files = [os.path.join(scripts_dir, f) for f in os.listdir(scripts_dir) if f.endswith('.txt')]
		if invoice_type == 'sales':
			filtered = [f for f in all_files if os.path.basename(f).startswith('sales_invoice_')]
		elif invoice_type == 'restock':
			filtered = [f for f in all_files if os.path.basename(f).startswith('restock_invoice_')]
		else:
			filtered = all_files
		filtered.sort(key=lambda p: os.path.getmtime(p), reverse=True)
		return filtered
	except Exception:
		return []

def read_invoice(file_path: str) -> str:
	"""Read and return the contents of an invoice file."""
	try:
		with open(file_path, 'r', encoding='utf-8') as f:
			return f.read()
	except Exception as e:
		return f"Error reading invoice '{file_path}': {e}"


