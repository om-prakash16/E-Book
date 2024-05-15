import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF

class Book:
    def __init__(self, title, author, content):
        self.title = title
        self.author = author
        self.content = content

class EBookReaderGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("EBook Reader")

        self.library = []
        self.current_book = None
        self.current_page = 0

        self.book_listbox = tk.Listbox(master, width=40)
        self.book_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.book_listbox.bind("<<ListboxSelect>>", self.on_book_select)

        self.page_display = tk.Canvas(master)
        self.page_display.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.next_button = tk.Button(master, text="Next Page", command=self.next_page)
        self.next_button.pack(side=tk.BOTTOM, fill=tk.X)

        self.prev_button = tk.Button(master, text="Previous Page", command=self.previous_page)
        self.prev_button.pack(side=tk.BOTTOM, fill=tk.X)

        self.open_button = tk.Button(master, text="Open PDF", command=self.open_pdf)
        self.open_button.pack(side=tk.BOTTOM, fill=tk.X)

    def add_book(self, book):
        self.library.append(book)
        self.book_listbox.insert(tk.END, f"{book.title} by {book.author}")

    def on_book_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.current_book = self.library[index]
            self.current_page = 0
            self.display_current_page()

    def display_current_page(self):
        if self.current_book:
            self.page_display.delete("all")
            content = self.current_book.content[self.current_page]
            self.page_display.create_image(0, 0, anchor="nw", image=content["image"])
            if "rects" in content:
                for text_box in content["rects"]:
                    self.page_display.create_text(text_box["x"], text_box["y"], anchor="nw", text=text_box["text"], fill="black")
            self.master.title(f"EBook Reader - {self.current_book.title} - Page {self.current_page + 1}")
        else:
            self.master.title("EBook Reader")

    def next_page(self):
        if self.current_book and self.current_page < len(self.current_book.content) - 1:
            self.current_page += 1
            self.display_current_page()

    def previous_page(self):
        if self.current_book and self.current_page > 0:
            self.current_page -= 1
            self.display_current_page()

    def open_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            pdf_document = fitz.open(file_path)
            title = file_path.split('/')[-1]
            author = "Unknown"  # You can extract author metadata from the PDF if available
            content = []
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                image_bytes = page.get_pixmap().tobytes()
                text_boxes = page.get_text("dict")
                page_content = {
                    "image": tk.PhotoImage(data=image_bytes),
                }
                if "rects" in text_boxes:
                    page_content["rects"] = text_boxes["rects"]
                content.append(page_content)
            book = Book(title, author, content)
            self.add_book(book)

# Sample usage
if __name__ == "__main__":
    # Create a Tkinter window
    root = tk.Tk()

    # Create an EBookReaderGUI instance
    ebook_reader_gui = EBookReaderGUI(root)

    root.mainloop()
