import os

# Global variable for inventory file path
INVENTORY_FILE = "shoes_inventory.txt"

def load_inventory():
	"""Load shoes inventory from text file and return shoes data list"""
	shoes_data = []
	try:
		if os.path.exists(INVENTORY_FILE):
			with open(INVENTORY_FILE, 'r') as file:
				for line_number, line in enumerate(file, start=1):
					try:
						if not line.strip():
							continue
						parts = [p.strip() for p in line.strip().split(',')]
						if len(parts) != 5:
							print(f"Skipping malformed line {line_number}: expected 5 fields, got {len(parts)}")
							continue
						quantity = int(parts[2])
						price = float(parts[3])
						shoe = {
							'type': parts[0],
							'brand': parts[1],
							'quantity': quantity,
							'price': price,
							'origin': parts[4]
						}
						shoes_data.append(shoe)
					except ValueError as ve:
						print(f"Skipping invalid numeric value at line {line_number}: {ve}")
					except Exception as line_error:
						print(f"Skipping line {line_number} due to error: {line_error}")
		else:
			print("Inventory file not found. Starting with empty inventory.")
	except Exception as e:
		print(f"Error loading inventory: {e}")
	
	return shoes_data

def save_inventory(shoes_data):
	"""Save current inventory to text file atomically"""
	temp_file = INVENTORY_FILE + ".tmp"
	try:
		with open(temp_file, 'w') as file:
			for shoe in shoes_data or []:
				try:
					shoe_type = str(shoe.get('type', '')).strip()
					brand = str(shoe.get('brand', '')).strip()
					quantity = int(shoe.get('quantity', 0))
					price = float(shoe.get('price', 0.0))
					origin = str(shoe.get('origin', '')).strip()
					if not all([shoe_type, brand, origin]):
						print("Skipping item with missing required fields during save.")
						continue
					file.write(f"{shoe_type},{brand},{quantity},{price:.2f},{origin}\n")
				except (ValueError, TypeError) as ve:
					print(f"Skipping item with invalid data during save: {ve}")
		# Replace original file atomically
		os.replace(temp_file, INVENTORY_FILE)
	except Exception as e:
		print(f"Error saving inventory: {e}")
		# Clean up temp file if replace failed
		try:
			if os.path.exists(temp_file):
				os.remove(temp_file)
		except Exception:
			pass


