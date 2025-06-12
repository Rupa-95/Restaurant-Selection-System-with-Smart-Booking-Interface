import tkinter as tk

# Custom message popup
def custom_message(title, message, bg_color="#FFF5E1", fg_color="#4B2E2E"):
    popup = tk.Toplevel()
    popup.title(title)
    popup.configure(bg=bg_color)
    popup.geometry("320x160")
    popup.resizable(False, False)

    msg_label = tk.Label(popup, text=message, bg=bg_color, fg=fg_color, wraplength=280, justify="center",
                         font=("Helvetica", 11))
    msg_label.pack(pady=20, padx=10)

    def close_popup():
        popup.destroy()

    btn = tk.Button(popup, text="OK", command=close_popup, bg="#CD853F", fg="white", width=10)
    btn.pack(pady=10)

    popup.grab_set()
    popup.focus_set()
    popup.wait_window()

# Sample restaurant data
restaurants = {
    "JH Family Feast": {"location": "Jubilee Hills", "ambience": "Family", "menu": {
        "Paneer Butter Masala": 180.00, "Butter Naan": 40.00, "Veg Biryani": 160.00}},
    "JH Rooftop Dhaba": {"location": "Jubilee Hills", "ambience": "Rooftop", "menu": {
        "Tandoori Chicken": 250.00, "Rumali Roti": 30.00, "Masala Papad": 50.00}},
    "JH Garden Dine": {"location": "Jubilee Hills", "ambience": "Garden View", "menu": {
        "Dal Makhani": 140.00, "Jeera Rice": 90.00, "Kheer": 60.00}},
    "HTC Family Kitchen": {"location": "Hitech City", "ambience": "Family", "menu": {
        "Chicken Curry": 200.00, "Chapati": 20.00, "Sweet Lassi": 40.00}},
    "HTC Rooftop Lounge": {"location": "Hitech City", "ambience": "Rooftop", "menu": {
        "Fish Fry": 280.00, "Tandoori Roti": 25.00, "Cold Coffee": 60.00}},
    "HTC Garden Bistro": {"location": "Hitech City", "ambience": "Garden View", "menu": {
        "Mixed Veg Curry": 150.00, "Naan": 40.00, "Falooda": 70.00}},
    "Sec Family Spot": {"location": "Secunderabad", "ambience": "Family", "menu": {
        "Chicken Biryani": 260.00, "Salad": 30.00, "Fruit Punch": 50.00}},
    "Sec Rooftop Resto": {"location": "Secunderabad", "ambience": "Rooftop", "menu": {
        "Grilled Paneer": 220.00, "Garlic Naan": 45.00, "Jaljeera": 30.00}},
    "Sec Garden Treat": {"location": "Secunderabad", "ambience": "Garden View", "menu": {
        "Rajma Chawal": 130.00, "Papad": 20.00, "Rabri": 60.00}}
}

# First window: preference selection
class PreferenceWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Select Preferences")
        self.root.configure(bg='#FFF5E1')

        tk.Label(root, text="Select Location and Ambience", font=("Helvetica", 14, "bold"),
                 fg='#8B0000', bg='#FFF5E1').pack(pady=5)

        tk.Label(root, text="Preferred Location:", fg='#4B2E2E', bg='#FFF5E1').pack(anchor='w', padx=10)
        self.location_var = tk.StringVar()
        for loc in ["Jubilee Hills", "Hitech City", "Secunderabad"]:
            tk.Radiobutton(root, text=loc, variable=self.location_var, value=loc,
                           bg='#FFF5E1', fg='#4B2E2E', selectcolor='#D2B48C').pack(anchor='w', padx=20)

        tk.Label(root, text="Preferred Ambience:", fg='#4B2E2E', bg='#FFF5E1').pack(anchor='w', padx=10)
        self.ambience_var = tk.StringVar()
        for amb in ["Family", "Rooftop", "Garden View"]:
            tk.Radiobutton(root, text=amb, variable=self.ambience_var, value=amb,
                           bg='#FFF5E1', fg='#4B2E2E', selectcolor='#D2B48C').pack(anchor='w', padx=20)

        tk.Button(root, text="Find Restaurant", bg="#CD853F", fg="white",
                  command=self.find_restaurant).pack(pady=10)

    def find_restaurant(self):
        loc = self.location_var.get()
        amb = self.ambience_var.get()

        if not loc or not amb:
            custom_message("Error", "Please select one location and one ambience.", bg_color="#FFCCCC", fg_color="#800000")
            return

        for name, data in restaurants.items():
            if data["location"] == loc and data["ambience"] == amb:
                self.root.destroy()
                root2 = tk.Tk()
                RestaurantChatbot(root2, name, data["menu"])
                root2.mainloop()
                return

        custom_message("Not Found", "No matching restaurant found.", bg_color="#FFCCCC", fg_color="#800000")

# Second window: booking screen
class RestaurantChatbot:
    def __init__(self, root, restaurant_name, menu):
        self.root = root
        self.menu = menu
        self.restaurant_name = restaurant_name
        self.root.title(restaurant_name)
        self.root.configure(bg='#FFF5E1')

        tk.Label(root, text=f"{restaurant_name}", font=("Helvetica", 14, "bold"),
                 fg="#8B0000", bg='#FFF5E1').pack(pady=5)

        self._create_label("Your Name:")
        self.name_entry = self._create_entry()

        self._create_label("Booking Time:")
        self.time_entry = self._create_entry()

        self._create_label("No. of Members:")
        self.members_entry = self._create_entry()

        self._create_label("Food Items:")
        self.food_vars = {}
        for item in self.menu:
            var = tk.IntVar()
            tk.Checkbutton(root, text=f"{item} (₹{self.menu[item]:.2f})", variable=var,
                           bg='#FFF5E1', fg="#4B2E2E", selectcolor='#D2B48C').pack(anchor='w', padx=20)
            self.food_vars[item] = var

        btn_frame = tk.Frame(root, bg='#FFF5E1')
        btn_frame.pack(pady=8)

        tk.Button(btn_frame, text="Book Table", bg="#CD853F", fg="white",
                  command=self.book_table).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Back", bg="#D2B48C", command=self.go_back).pack(side='left', padx=5)

    def _create_label(self, text):
        tk.Label(self.root, text=text, fg='#4B2E2E', bg='#FFF5E1').pack(anchor='w', padx=10)

    def _create_entry(self):
        entry = tk.Entry(self.root)
        entry.pack(padx=10, fill='x', pady=2)
        return entry

    def book_table(self):
        name = self.name_entry.get().strip()
        time = self.time_entry.get().strip()
        members = self.members_entry.get().strip()
        selected_food = [item for item, var in self.food_vars.items() if var.get()]
        total = sum(self.menu[item] for item in selected_food)

        if not name or not time or not members:
            custom_message("Error", "Please enter all details.", bg_color="#FFCCCC", fg_color="#800000")
            return

        try:
            members_int = int(members)
            if members_int <= 0:
                raise ValueError
        except ValueError:
            custom_message("Error", "Enter a valid number of members.", bg_color="#FFCCCC", fg_color="#800000")
            return

        message = (
            f"Thank you, {name}!\n"
            f"Your table for {members_int} is booked at {self.restaurant_name} for {time}.\n"
            f"Items Ordered: {', '.join(selected_food) if selected_food else 'None'}\n"
            f"Total: ₹{total:.2f}"
        )
        custom_message("Booking Confirmed", message, bg_color="#CCFFCC", fg_color="#006400")

    def go_back(self):
        self.root.destroy()
        root = tk.Tk()
        PreferenceWindow(root)
        root.mainloop()

# Entry point
if __name__ == "__main__":
    root = tk.Tk()
    PreferenceWindow(root)
    root.mainloop()
