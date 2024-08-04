import tkinter as tk
from tkinter import ttk, filedialog
from fun import modeling
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostRegressor, RandomForestRegressor
import pandas as pd
root = tk.Tk()
root.title("AM")
features = []
value_feat_combo = tk.StringVar()
variables = tk.StringVar()
selected_file_path = tk.StringVar()

switch_logistic = tk.BooleanVar()
switch_tree = tk.BooleanVar()
switch_svm = tk.BooleanVar()
switch_linear = tk.BooleanVar()
switch_ada = tk.BooleanVar()
switch_rf = tk.BooleanVar()

def start():
    print(f"Button clicked!")
    print(f"{selected_file_path.get()}")

    filtered_strings = filter_strings()

    X = Xy()

    accuracies = modeling(selected_file_path.get(),
            models = filtered_strings,
            features = X,
            aim = 'classification')
    start_modeling.config(text=f"Accuracies: {str(accuracies)}")
def filter_strings():
    switches = [switch_logistic.get(), switch_tree.get(), switch_svm.get(), switch_linear.get(), switch_ada.get(), switch_rf.get()]
    string_list = [LogisticRegression(solver="liblinear"), 
                   DecisionTreeClassifier(random_state=2), 
                   SVC(), 
                   LinearRegression(), 
                   AdaBoostRegressor(n_estimators=50, learning_rate=1.0), 
                   RandomForestRegressor(n_estimators=100, random_state=42)]
    
    filtered_strings = [s for s, switch in zip(string_list, switches) if switch == 1]
    
    return filtered_strings

def on_switch_toggle(var):
    filter_strings()
def update_checkbutton(var, value):
    if value.get() == 1:
        features.append(var)
    if value.get() == 0:
        features.remove(var)
def Xy():
    y = value_feat_combo.get()
    X = [x for x in features if x != value_feat_combo.get()]
    return [X,y]
def listify(s):
    s = s.strip("()")  
    s = s.replace("'", "")  
    list_of_strings = s.split(", ")  
    return list_of_strings

def browse_files():
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=(("CSV files", "*.csv*"), ("all files", "*.*"))
    )
    if file_path:
        selected_file_path.set(file_path)
        file_label.config(text=f"Selected File: {file_path}")

        data = pd.read_csv(file_path)
        variables.set(list(data.columns))
        feat_label = ttk.Label(feat_frame, text="Select a Feature to predict:", font=("Helvetica", 12), background="#e9ecef")
        feat_label.pack()

        feat_combo = ttk.Combobox(feat_frame, values=list(data.columns) ,state="readonly", textvariable=value_feat_combo)
        feat_combo.bind("<<ComboboxSelected>>", file_selected)
        feat_combo.pack()
def file_selected(event):
    global features
    features = []
    vars = listify(variables.get())
    vars = [x for x in vars if x != value_feat_combo.get()]
    for widget in button_frame.winfo_children():
        widget.destroy()
    i = 0
    for var in vars:
        value = tk.IntVar()
        but = ttk.Checkbutton(button_frame, text=var, variable = value, command=lambda var=var, value=value: update_checkbutton(var, value))
        but.grid(row=(i // 4) + 1, column=i % 4, padx=5, pady=10, sticky="w")
        i += 1

def update_buttons(event):
    switch_logistic.set(False)
    switch_tree.set(False)
    switch_svm.set(False)
    switch_linear.set(False)
    switch_ada.set(False)
    switch_rf.set(False)
    selected_option = combo.get()
    if selected_option == "Classification":
        for i, button in enumerate(option1_buttons):
            button.grid(row=(i // 3) + 1, column=i%3, padx=5, pady=5)
        for button in option2_buttons:
            button.grid_remove()
    elif selected_option == "Regression":
        for i, button in enumerate(option2_buttons):
            button.grid(row=(i // 3) + 1, column=i%3, padx=5, pady=5)
        for button in option1_buttons:
            button.grid_remove()

############################################################################################################

switches = [switch_logistic.get(), 
            switch_tree.get(), 
            switch_svm.get(), 
            switch_linear.get(), 
            switch_ada.get(),
            switch_rf.get()]

root.geometry("1000x600")
root.configure(bg="#e9ecef") 



style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12), padding=10)
style.configure("TButton", font=("Helvetica", 12), padding=10, foreground="black", background="#d1d3fe")
style.configure("TCheckbutton", font=("Helvetica", 12), padding=10, foreground="black", background="#d1d3fe", width = 20)
style.configure("TCombobox", font=("Helvetica", 12), background="#c3c5f1")

###############################################################################################################


label = ttk.Label(root, text="Please attach your data!", font=("Helvetica", 20), background="#e9ecef")
label.pack(pady=25)

browse_button = ttk.Button(root, text="Browse Files", command=browse_files)
browse_button.pack(pady=10)

file_label = ttk.Label(root, text="No file selected", background="#e9ecef")
file_label.pack(pady=10)

feat_frame = tk.Frame(root)
feat_frame.pack()

button_frame = tk.Frame(root)
button_frame.pack(padx=10, pady=10)



combo = ttk.Combobox(root, values=["Classification", "Regression"], state="readonly")
combo.pack(pady=20)
combo.bind("<<ComboboxSelected>>", update_buttons)
combo.current(0)

options_frame = ttk.Frame(root)
options_frame.pack()
option1_frame = ttk.Frame(options_frame)

option1_buttons = [
    ttk.Checkbutton(option1_frame, text="Logistic Regression", variable=switch_logistic, command=lambda: on_switch_toggle(switch_logistic)),
    ttk.Checkbutton(option1_frame, text="Decision Tree", variable=switch_tree, command=lambda: on_switch_toggle(switch_tree)),
    ttk.Checkbutton(option1_frame, text="SVM", variable=switch_svm, command=lambda: on_switch_toggle(switch_svm)),
]
option1_frame.pack()

option2_frame = ttk.Frame(options_frame)

option2_buttons = [
    ttk.Checkbutton(option2_frame, text="Linear Regression", variable=switch_linear, command=lambda: on_switch_toggle(switch_linear)),
    ttk.Checkbutton(option2_frame, text="Ada Boost Regressor", variable=switch_ada, command=lambda: on_switch_toggle(switch_ada)),
    ttk.Checkbutton(option2_frame, text="Random Forest", variable=switch_rf, command=lambda: on_switch_toggle(switch_rf)),
]
option2_frame.pack()

update_buttons(None)
start_modeling = ttk.Button(root, text="Start genrating models", command=start)
start_modeling.pack(pady=20, anchor="s")
start_modeling.place(anchor="s", relx=0.5, rely=0.9, y = 20)


root.mainloop()