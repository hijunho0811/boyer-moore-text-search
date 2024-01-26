import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import libboyer_moore
import fitz


class PDFSearchApp:

    def __init__(self, master):
        self.master = master
        self.master.title("PDF Search App")

        # Variables for storing user input
        self.pdf_path_var = tk.StringVar()
        self.pattern_var = tk.StringVar()

        # Create widgets
        ttk.Label(self.master, text="PDF Path:").pack(pady=5)
        self.pdf_path_entry = ttk.Entry(self.master, textvariable=self.pdf_path_var, width=50)
        self.pdf_path_entry.pack(pady=5)

        ttk.Label(self.master, text="Search Pattern:").pack(pady=5)
        self.pattern_entry = ttk.Entry(self.master, textvariable=self.pattern_var, width=30)
        self.pattern_entry.pack(pady=5)

        self.search_button = ttk.Button(self.master, text="Search", command=self.search_pattern)
        self.search_button.pack(pady=10)

        self.text_widget = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=80, height=20)
        self.text_widget.pack(pady=10)

    def search_pattern(self):   
        self.text_widget.delete("1.0", tk.END)
        pdf_path = self.pdf_path_var.get()
        extracted_text = extract_text_from_pdf(pdf_path)

        # conver the pattern and text for case insensitive search
        pattern_to_search = self.pattern_var.get().lower()
        extracted_text_lower = extracted_text.lower()

        # Call the Boyer-Moore search function
        occurrences = libboyer_moore.searchBoyerMoore(extracted_text_lower, pattern_to_search)

        # Display full text on widget
        self.text_widget.insert(tk.END, extracted_text)

        # Emphasize occurences
        for start_index in occurrences:
            real_start_index= convert_to_text_widget_index(start_index, extracted_text)
            end_index = start_index + len(pattern_to_search)
            real_end_index= convert_to_text_widget_index(end_index, extracted_text)
            self.text_widget.tag_add("emphasis", real_start_index, real_end_index)
            self.text_widget.tag_configure("emphasis", foreground="white", background="blue")
            self.text_widget.mark_set(tk.INSERT, "1.0")

        print(f"Occurrences: {occurrences}")


def convert_to_text_widget_index(original_index, text_content):
        # Count the number of \n before index
        line_number = text_content.count('\n', 0, original_index) + 1

        # Calculate position
        char_position = original_index - text_content.rfind('\n', 0, original_index) -1
        return f"{line_number}.{char_position}"



def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text = ""
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        text += page.get_text()
    pdf_document.close()
    return text

def main():
    root = tk.Tk()
    app = PDFSearchApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
