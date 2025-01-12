# GUI Application Class
class DecisionTreeApp:
    def __init__(self, root_node):
        self.root_node = root_node
        self.current_node = root_node

        # Initialize the main window
        self.window = tk.Tk()
        self.window.title("Expert System Recommendation")
        self.window.geometry("600x200")

        # Question label
        self.question_label = tk.Label(
            self.window,
            text=self.current_node.question,
            wraplength=550,
            font=("Times New Roman", 18)
        )
        self.question_label.pack(pady=20)

        # Frame to hold option buttons
        self.buttons_frame = tk.Frame(self.window)
        self.buttons_frame.pack()

        # Create buttons for the current options
        self.create_option_buttons()

    def create_option_buttons(self):
        # Clear existing buttons
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        # Create a button for each option
        for option in self.current_node.options:
            button = tk.Button(
                self.buttons_frame,
                text=option,
                width=20,
                command=lambda opt=option: self.select_option(opt)
            )
            button.pack(side=tk.LEFT, padx=10, pady=10)

    def select_option(self, option):
        # Move to the next node based on the selected option
        if option in self.current_node.children:
            self.current_node = self.current_node.children[option]
            if self.current_node.result:
                # If it's a leaf node, show the result
                messagebox.showinfo("Result", self.current_node.result)
                self.window.destroy()
            else:
                # Update the question and options for the next node
                self.question_label.config(text=self.current_node.question)
                self.create_option_buttons()
        else:
            messagebox.showerror("Error", "Invalid option selected.")

    def run(self):
        # Start the GUI event loop
        self.window.mainloop()

# Main execution
if __name__ == "__main__":
    app = DecisionTreeApp(root)
    app.run()