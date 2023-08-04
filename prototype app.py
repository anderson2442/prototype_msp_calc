import tkinter as tk


class Role:
    def __init__(self, name, rate_per_hour):
        self.name = name
        self.rate_per_hour = rate_per_hour


class ResourceTracker:
    def __init__(self):
        self.roles = {}
        self.next_role_number = 1

    def add_role(self, role, quantity):
        if role.name in self.roles:
            self.roles[role.name]['quantity'] += quantity
        else:
            self.roles[role.name] = {
                'role': role,
                'quantity': quantity,
            }

    def update_role_rate(self, role_name, new_rate):
        if role_name in self.roles:
            self.roles[role_name]['role'].rate_per_hour = new_rate

    def calculate_blended_rate(self):
        total_billable_amount = 0.0
        total_quantity = 0

        for role_data in self.roles.values():
            role = role_data['role']
            quantity = role_data['quantity']

            total_billable_amount += role.rate_per_hour * quantity
            total_quantity += quantity

        if total_quantity == 0:
            return 0.0, 0

        blended_rate = total_billable_amount / total_quantity
        return blended_rate, total_quantity

    def calculate_total_cost(self, num_hours):
        blended_rate, total_quantity = self.calculate_blended_rate()
        total_cost = num_hours * blended_rate
        return total_cost, total_quantity

    def add_new_role(self, name, rate_per_hour):
        role = Role(name, rate_per_hour)
        self.roles[name] = {'role': role, 'quantity': 0}
        print(f"{name} with rate ${rate_per_hour:.2f} per hour added as Role {self.next_role_number}")
        self.next_role_number += 1


class ResourceTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Resource Tracker")
        self.resource_tracker = ResourceTracker()

        self.available_roles = [
            # Role data...
        ]

        self.create_widgets()

    def create_widgets(self):
        # Available Roles
        available_roles_label = tk.Label(self, text="Available Roles:")
        available_roles_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.available_roles_listbox = tk.Listbox(self, selectmode=tk.SINGLE, height=12, width=35)
        self.available_roles_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        for role in self.available_roles:
            self.available_roles_listbox.insert(tk.END, f"{role['name']} (${role['rate_per_hour']:.2f} per hour)")

        # Add Role
        new_role_label = tk.Label(self, text="Add a New Role:")
        new_role_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        new_role_name_label = tk.Label(self, text="Name:")
        new_role_name_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)

        self.new_role_name_entry = tk.Entry(self)
        self.new_role_name_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

        new_role_rate_label = tk.Label(self, text="Rate per hour ($):")
        new_role_rate_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)

        self.new_role_rate_entry = tk.Entry(self)
        self.new_role_rate_entry.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)

        add_new_role_button = tk.Button(self, text="Add New Role", command=self.add_new_role)
        add_new_role_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        # Add Existing Role
        quantity_label = tk.Label(self, text="Enter the quantity:")
        quantity_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        self.quantity_entry = tk.Entry(self)
        self.quantity_entry.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

        add_existing_role_button = tk.Button(self, text="Add Role", command=self.add_existing_role)
        add_existing_role_button.grid(row=8, column=0, padx=5, pady=5)

        delete_role_button = tk.Button(self, text="Delete Role", command=self.delete_role)
        delete_role_button.grid(row=8, column=1, padx=5, pady=5)

        # Calculate Blended Rate
        blended_rate_label = tk.Label(self, text="")
        blended_rate_label.grid(row=9, column=0, columnspan=2, padx=10, pady=5)
        self.blended_rate_label = blended_rate_label

        people_per_role_label = tk.Label(self, text="People per Role:")
        people_per_role_label.grid(row=10, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)
        self.people_per_role_label = people_per_role_label

        calculate_blended_rate_button = tk.Button(self, text="Calculate Blended Rate", command=self.calculate_blended_rate)
        calculate_blended_rate_button.grid(row=11, column=0, columnspan=2, padx=10, pady=5)

        # Calculate Total Cost
        num_hours_label = tk.Label(self, text="Enter the number of hours:")
        num_hours_label.grid(row=12, column=0, columnspan=2, padx=10, pady=5)

        self.num_hours_entry = tk.Entry(self)
        self.num_hours_entry.grid(row=13, column=0, columnspan=2, padx=10, pady=5)

        calculate_total_cost_button = tk.Button(self, text="Calculate Total Cost", command=self.calculate_total_cost)
        calculate_total_cost_button.grid(row=14, column=0, columnspan=2, padx=10, pady=5)

        # Edit Pay
        edit_pay_label = tk.Label(self, text="Edit Pay:")
        edit_pay_label.grid(row=15, column=0, columnspan=2, padx=10, pady=5)

        self.edit_role_rate_entry = tk.Entry(self)
        self.edit_role_rate_entry.grid(row=16, column=0, padx=10, pady=5, sticky=tk.E)

        edit_pay_button = tk.Button(self, text="Edit Pay", command=self.edit_role_pay)
        edit_pay_button.grid(row=16, column=1, padx=10, pady=5, sticky=tk.W)

        # Restart Button
        restart_button = tk.Button(self, text="Reset and Start Over", command=self.restart)
        restart_button.grid(row=17, column=0, columnspan=2, padx=10, pady=5)

    def add_new_role(self):
        name = self.new_role_name_entry.get()
        rate_per_hour = float(self.new_role_rate_entry.get())
        self.resource_tracker.add_new_role(name, rate_per_hour)
        self.available_roles.append({"name": name, "rate_per_hour": rate_per_hour})
        self.update_available_roles()
        self.new_role_name_entry.delete(0, tk.END)
        self.new_role_rate_entry.delete(0, tk.END)

    def add_existing_role(self):
        choice = self.available_roles_listbox.curselection()
        if not choice:
            return

        index = choice[0]
        role_data = self.available_roles[index]
        role = Role(role_data['name'], role_data['rate_per_hour'])
        quantity = float(self.quantity_entry.get())
        self.resource_tracker.add_role(role, quantity)
        self.update_available_roles()
        self.quantity_entry.delete(0, tk.END)
        self.quantity_entry.focus_set()

    def delete_role(self):
        choice = self.available_roles_listbox.curselection()
        if not choice:
            return

        index = choice[0]
        role_data = self.available_roles.pop(index)
        self.update_available_roles()
        del self.resource_tracker.roles[role_data['name']]
        self.calculate_blended_rate()

    def update_available_roles(self):
        self.available_roles_listbox.delete(0, tk.END)
        for role in self.available_roles:
            self.available_roles_listbox.insert(tk.END, f"{role['name']} (${role['rate_per_hour']:.2f} per hour)")

    def calculate_blended_rate(self):
        blended_rate, total_quantity = self.resource_tracker.calculate_blended_rate()
        self.blended_rate_label.config(text=f"Blended billable rate: ${blended_rate:.2f} per hour")

        people_per_role_text = ""
        for role_data in self.resource_tracker.roles.values():
            role = role_data['role']
            quantity = role_data['quantity']
            people_per_role_text += f"{role.name}: {quantity}\n"

        self.people_per_role_label.config(text=people_per_role_text)

    def calculate_total_cost(self):
        num_hours = float(self.num_hours_entry.get())
        total_cost, total_quantity = self.resource_tracker.calculate_total_cost(num_hours)
        self.blended_rate_label.config(text=f"Total Cost for {num_hours} hours: ${total_cost:.2f}")

    def edit_role_pay(self):
        choice = self.available_roles_listbox.curselection()
        if not choice:
            return

        index = choice[0]
        role_data = self.available_roles[index]
        role_name = role_data['name']

        try:
            new_rate = float(self.edit_role_rate_entry.get())
            self.resource_tracker.update_role_rate(role_name, new_rate)
            self.update_available_roles()
            self.edit_role_rate_entry.delete(0, tk.END)
        except ValueError:
            print("Invalid rate. Please enter a valid numeric value.")

    def restart(self):
        self.resource_tracker.roles = {}
        self.update_available_roles()
        self.new_role_name_entry.delete(0, tk.END)
        self.new_role_rate_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.num_hours_entry.delete(0, tk.END)
        self.edit_role_rate_entry.delete(0, tk.END)
        self.calculate_blended_rate()


if __name__ == "__main__":
    app = ResourceTrackerApp()
    app.mainloop()
