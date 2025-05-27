import os
from tabulate import tabulate

"""
Nike Warehouse Management System
This program manages shoe inventory including:
- Adding new shoes
- Viewing/editing existing stock
- Calculating inventory values
- Generating reports by country
"""

class Shoe:
    """Class to represent each shoe product in inventory"""
    def __init__(self, country, code, product, cost, quantity):
        """Initialize shoe attributes"""
        self.country = country        # Origin country
        self.code = code              # Product code/SKU
        self.product = product        # Product name
        self.cost = float(cost)       # Cost per unit (converted to float)
        self.quantity = int(quantity) # Stock quantity (converted to integer)
    
    def get_cost(self):
        """Return the cost of the shoe"""
        return self.cost
    
    def get_quantity(self):
        """Return the quantity of the shoe"""
        return self.quantity
    
    def __str__(self):
        """String representation of shoe for file storage"""
        return f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}"

# Global list to store all shoe objects
shoe_list = []

# ========== FILE OPERATIONS ========== #
def read_shoes_data():
    """
    Load shoe data from inventory.txt
    Creates file if it doesn't exist
    Returns True if data loaded successfully, False otherwise
    """
    shoe_list.clear()  # Clear existing data before loading
    try:
        # Create file if it doesn't exist
        if not os.path.exists('inventory.txt'):
            with open('inventory.txt', 'w') as file:
                file.write("country,code,product,cost,quantity")
            print("Created new inventory file")
            return False
        
        # Read existing file
        with open('inventory.txt', 'r') as file:
            next(file)  # Skip header line
            for line in file:
                data = line.strip().split(',')
                if len(data) == 5:  # Ensure proper formatting
                    shoe = Shoe(data[0], data[1], data[2], data[3], data[4])
                    shoe_list.append(shoe)
        return True
    except Exception as e:
        print(f"Error loading inventory: {e}")
        return False

# ========== INVENTORY OPERATIONS ========== #
def capture_shoes():
    """Add new shoe to inventory through user input"""
    print("\n=== Add New Shoe ===")
    
    # Get shoe details from user
    country = input("Country: ")
    code = input("Code: ").upper()  # Convert to uppercase for consistency.
    product = input("Product: ")
    
    # Validate cost input
    while True:
        try:
            cost = float(input("Cost (R): "))
            if cost > 0: 
                break
            print("Cost must be positive")
        except ValueError:
            print("Please enter a valid number")
    
    # Validate quantity input
    while True:
        try:
            quantity = int(input("Quantity: "))
            if quantity >= 0: 
                break
            print("Quantity can't be negative")
        except ValueError:
            print("Please enter a whole number")
    
    # Create and store new shoe
    shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(shoe)
    
    # Append to file
    try:
        with open('inventory.txt', 'a') as file:
            file.write(f"\n{country},{code},{product},{cost},{quantity}")
        print("Shoe added successfully!")
    except Exception as e:
        print(f"Error saving shoe: {e}")

def view_all():
    """Display all shoes in a formatted table"""
    if not shoe_list:
        print("No shoes in inventory")
        return
    
    # Prepare table data
    headers = ["Country", "Code", "Product", "Cost", "Quantity"]
    table = [
        [s.country, s.code, s.product, f"R{s.cost:.2f}", s.quantity] 
        for s in shoe_list
    ]
    
    print("\n=== Current Inventory ===")
    print(tabulate(table, headers=headers, tablefmt="grid"))

# ========== STOCK MANAGEMENT ========== #
def re_stock():
    """Identify and restock item with lowest quantity"""
    if not shoe_list:
        print("No shoes in inventory")
        return
    
    # Find shoe with minimum stock
    lowest = min(shoe_list, key=lambda x: x.quantity)
    
    # Display current stock info
    print(f"\nShoe needing restock:")
    print(f"Country: {lowest.country}")
    print(f"Code: {lowest.code}")
    print(f"Product: {lowest.product}")
    print(f"Cost: R{lowest.cost:.2f}")
    print(f"Current Quantity: {lowest.quantity}")
    
    # Handle restock process
    if input("Restock? (yes/no): ").lower() == 'yes':
        try:
            add = int(input("Quantity to add: "))
            if add > 0:
                # Update quantity
                lowest.quantity += add
                
                # Rewrite entire file with updated data
                with open('inventory.txt', 'w') as file:
                    file.write("country,code,product,cost,quantity")  # Header
                    for shoe in shoe_list:
                        file.write(f"\n{shoe}")
                print("Restock successful!")
            else:
                print("Quantity must be positive")
        except ValueError:
            print("Invalid quantity")

def search_shoe():
    """Search for shoe by product code"""
    if not shoe_list:
        print("No shoes in inventory")
        return
    
    code = input("Enter shoe code: ").upper()  # Case-insensitive search
    
    # Linear search through inventory
    for shoe in shoe_list:
        if shoe.code == code:
            print("\n=== Shoe Found ===")
            print(f"Country: {shoe.country}")
            print(f"Code: {shoe.code}")
            print(f"Product: {shoe.product}")
            print(f"Cost: R{shoe.cost:.2f}")
            print(f"Quantity: {shoe.quantity}")
            return
    
    print("Shoe not found")

# ========== REPORTING ========== #
def value_per_item():
    """Calculate and display value for each product (cost * quantity)"""
    if not shoe_list:
        print("No shoes in inventory")
        return
    
    headers = ["Product", "Code", "Total Value"]
    table = [
        [s.product, s.code, f"R{s.cost * s.quantity:.2f}"] 
        for s in shoe_list
    ]
    
    print("\n=== Product Values ===")
    print(tabulate(table, headers=headers, tablefmt="grid"))

def highest_qty():
    """Identify product with highest stock quantity (mark for sale)"""
    if not shoe_list:
        print("No shoes in inventory")
        return
    
    # Find shoe with maximum quantity
    highest = max(shoe_list, key=lambda x: x.quantity)
    
    print("\n=== Shoe For Sale ===")
    print(f"Product: {highest.product}")
    print(f"Code: {highest.code}")
    print(f"Quantity: {highest.quantity}")
    print(f"Cost: R{highest.cost:.2f}")
    print("\nThis shoe should be marked for sale!")

def stock_by_country():
    """Generate report of inventory grouped by country"""
    if not shoe_list:
        print("No shoes in inventory")
        return
    
    # Dictionary to aggregate country data
    country_stats = {}
    
    # Calculate totals per country
    for shoe in shoe_list:
        if shoe.country not in country_stats:
            country_stats[shoe.country] = {
                'total_value': 0,
                'total_quantity': 0,
                'products': 0
            }
        
        # Update country totals
        country_stats[shoe.country]['total_value'] += shoe.cost * shoe.quantity
        country_stats[shoe.country]['total_quantity'] += shoe.quantity
        country_stats[shoe.country]['products'] += 1
    
    # Prepare table data
    headers = ["Country", "Products", "Total Quantity", "Total Value"]
    table = []
    for country, stats in country_stats.items():
        table.append([
            country,
            stats['products'],
            stats['total_quantity'],
            f"R{stats['total_value']:.2f}"
        ])
    
    # Sort by total value (descending)
    table.sort(key=lambda x: float(x[3][1:]), reverse=True)
    
    print("\n=== STOCK BY COUNTRY ===")
    print(tabulate(table, headers=headers, tablefmt="grid"))

def total_warehouse_value():
    """Calculate total monetary value of all inventory"""
    if not shoe_list:
        print("No shoes in inventory")
        return
    
    # Sum of (cost * quantity) for all shoes
    total = sum(shoe.cost * shoe.quantity for shoe in shoe_list)
    print(f"\n=== TOTAL WAREHOUSE VALUE ===")
    print(f"R{total:.2f}")

# ========== MAIN PROGRAM ========== #
def main():
    """Main program loop with menu interface"""
    
    # Load initial data
    if read_shoes_data():
        print(f"\nLoaded {len(shoe_list)} shoes from inventory")
    else:
        print("\nStarting with empty inventory")
    
    # Main menu loop
    while True:
        print("\n===== Nike Warehouse Management =====")
        print("1. Add new shoe")
        print("2. View all shoes")
        print("3. Restock shoes")
        print("4. Search shoe")
        print("5. Product values")
        print("6. Highest quantity (mark for sale)")
        print("7. Stock by country")
        print("8. Total warehouse value")
        print("9. Exit")
        
        choice = input("\nEnter choice (1-9): ").strip()
        
        # Menu options
        if choice == '1':
            capture_shoes()
        elif choice == '2':
            view_all()
        elif choice == '3':
            re_stock()
        elif choice == '4':
            search_shoe()
        elif choice == '5':
            value_per_item()
        elif choice == '6':
            highest_qty()
        elif choice == '7':
            stock_by_country()
        elif choice == '8':
            total_warehouse_value()
        elif choice == '9':
            print("\nThank you for using Nike Warehouse Management!")
            break
        else:
            print("Invalid choice, please try again")

# Start program execution
main()