import tkinter as tk
from tkinter import messagebox

# Define the Node class for the decision tree
class Node:
    def __init__(self, question, options, children=None, result=None):
        """
        Initializes a node in the decision tree.

        Parameters:
        - question (str): The question to display at this node.
        - options (list): A list of option strings for the user to choose from.
        - children (dict): A mapping from option strings to child nodes.
        - result (str): The result to display if this is a leaf node.
        """
        self.question = question
        self.options = options
        self.children = children or {}
        self.result = result

# Leaf nodes with recommendations
leave_node = Node(
    question=None,
    options=[],
    result="Recommendation: Leave"
)

wait_node = Node(
    question=None,
    options=[],
    result="Recommendation: Wait"
)

# Build the decision tree by defining nodes and their relationships

# Level 1 (Root node)
root = Node(
    question="What is the restaurant's level of Patrons?",  # Question 1
    options=["Full", "Some", "None"]
)

# Level 2
# For "Full" path from root
node2_full = Node(
    question="What is the Wait Time (minutes)?",  # Question 2
    options=["0", "10", "30", "60"]
)

# For "Some" path from root
node2_some = wait_node  # Recommendation: Wait

# For "None" path from root
node2_none = leave_node  # Recommendation: Leave

# Level 3
# For node2_full path
node3_full_0 = wait_node  # Recommendation: Wait
node3_full_10 = Node(
    question="Is it Raining?",  # Question 3
    options=["Yes", "No"]
)

node3_full_30 = Node(
    question="Is there an Alternative?",  # Question 3
    options=["Yes", "No"]
)

node3_full_60 = leave_node  # Recommendation: Leave

# Level 4
# For node3_full_10 path
node4_full_10_yes = wait_node # Recommendation: Wait
node4_full_10_no = Node(
    question="Are people being Annoying?",  # Question 4
    options=["Yes", "No"]
)

# For node3_full_30 path
node4_full_30_yes = Node(
    question="Is it Friday or Saturday?",  # Question 4
    options=["Yes", "No"]
)

node4_full_30_no = Node(
    question="Is there a Bar?",  # Question 4
    options=["Yes", "No"]
)

# Level 5
# For node4_full_10_no path
node5_full_10_no_yes = Node(
    question="Are you Hungry?",  # Question 4
    options=["Yes", "No"]
)

node5_full_10_no_no = wait_node  # Recommendation: Wait

# For node4_full_30_yes path
node5_full_30_yes_yes = wait_node  # Recommendation: Wait
node5_full_30_yes_no = leave_node  # Recommendation: Leave

# For node4_full_30_no path
node5_full_30_no_no = Node(
    question="Do you have a Reservation?",  # Question 5
    options=["Yes", "No"]
)

node5_full_30_no_yes = wait_node  # Recommendation: Wait

# Level 6
# For node5_full_10_no_yes path
node6_full_10_no_yes_yes = leave_node  # Recommendation: Leave
node6_full_10_no_yes_no = wait_node  # Recommendation: Wait

# For node5_full_30_no_no path
node6_full_30_no_no_yes = wait_node  # Recommendation: Wait
node6_full_30_no_no_no = leave_node  # Recommendation: Leave




# Level 5
# For node4_full_30_yes
node5_full_30_yes_yes = Node(
    question=None,
    options=[],
    result="Recommendation: Wait"
)

node5_full_30_yes_no = Node(
    question=None,
    options=[],
    result="Recommendation: Leave"
)

# For node4_full_30_no 
node5_full_30_no_yes = wait_node
node5_full_30_no_no = leave_node





# Assign children to nodes

# Level 1
root.children = {
    "Full": node2_full,
    "Some": node2_some,
    "None": node2_none
}

# Level 2
node2_full.children = {
    "0": node3_full_0,  # Recommendation: Leave
    "10": node3_full_10,
    "30": node3_full_30,
    "60": node3_full_60 # Recommendation: Wait
}

# Level 3
node3_full_10.children = {
    "Yes": wait_node,
    "No": node4_full_10_no
}

node3_full_30.children = {
    "Yes": node4_full_30_yes,
    "No": node4_full_30_no
}

# Level 4
node4_full_10_no.children = {
    "Yes": node5_full_10_no_yes,
    "No": node5_full_10_no_no
}

node4_full_30_yes.children = {
    "Yes": wait_node,
    "No": leave_node
}

node4_full_30_no.children = {
    "Yes": node5_full_30_no_yes,
    "No": node5_full_30_no_no
}

# Level 5
node5_full_10_no_yes.children = {
    "Yes": leave_node,
    "No": wait_node
}

node5_full_30_no_no.children = {
    "Yes": wait_node,
    "No": leave_node
}

# Level 6
node6_full_10_no_yes_yes.children = {}
node6_full_10_no_yes_no.children = {}

node6_full_30_no_no_yes.children = {}
node6_full_30_no_no_no.children = {}



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