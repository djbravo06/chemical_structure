import tkinter as tk
from tkinter import messagebox
from urllib.request import urlopen
from urllib.parse import quote
import concurrent.futures
from rdkit import Chem
from rdkit.Chem import Draw
from PIL import Image, ImageTk  # Only used to convert RDKit images to Tkinter-compatible format

# Function to fetch SMILES and other names
def _get_smiles_also_names(iupac):
    def fetch_url(url):
        try:
            return urlopen(url).read().decode('utf8')
        except:
            return '0'
    
    url1 = f'http://cactus.nci.nih.gov/chemical/structure/{quote(iupac)}/smiles'
    url2 = f'http://cactus.nci.nih.gov/chemical/structure/{quote(iupac)}/names'
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        a1 = executor.submit(fetch_url, url1)
        b1 = executor.submit(fetch_url, url2)
        
        a = a1.result()
        b = b1.result()
    
    if a == '0':
        return '0', 'No other names found'
    
    b = " -> ".join(b.split("\n"))
    return a, b

# Function to handle search
def search_structure():
    iupac = entry.get()
    smiles, names = _get_smiles_also_names(iupac)
    
    if smiles == '0':
        messagebox.showerror("Error", f"'{iupac}' NOT FOUND")
    else:
        smiles_label.config(text=f"SMILES: {smiles}")
        names_label.config(text=f"Other Names: {names}")

        struct = Chem.MolFromSmiles(smiles)
        if struct:
            # Add explicit hydrogens to the molecule
            struct_with_h = Chem.AddHs(struct)

            # Create an image of the structure with explicit hydrogens
            img_data = Draw.MolToImage(struct_with_h, size=(300, 300), kekulize=True, wedgeBonds=True, highlightAtoms=[], highlightBonds=[])
            img = ImageTk.PhotoImage(img_data)
            canvas.create_image(0, 0, anchor=tk.NW, image=img)
            canvas.image = img

# Create the main window
root = tk.Tk()
root.title("Chemical Structure Finder")
root.configure(bg='black')  # Set background color to black

# Create and position the widgets
entry_label = tk.Label(root, text="Enter IUPAC Name:", bg='black', fg='white')  # Set label background to black and text to white
entry_label.grid(row=0, column=0, padx=10, pady=10)

entry = tk.Entry(root, width=40, bg='grey', fg='white', insertbackground='white')  # Set entry background to grey and text to white
entry.grid(row=0, column=1, padx=10, pady=10)

search_button = tk.Button(root, text="Search", command=search_structure, bg='grey', fg='white')  # Set button background to grey and text to white
search_button.grid(row=0, column=2, padx=10, pady=10)

smiles_label = tk.Label(root, text="SMILES: ", wraplength=500, bg='black', fg='white')  # Set label background to black and text to white
smiles_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='w')

names_label = tk.Label(root, text="Other Names: ", wraplength=500, bg='black', fg='white')  # Set label background to black and text to white
names_label.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky='w')

canvas = tk.Canvas(root, width=300, height=300, bg='black', highlightthickness=0)  # Set canvas background to black
canvas.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()

