import tkinter as tk
import tkinter.filedialog
import tkinter.ttk as ttk
import os
from custom_treeview import ScrolledTreeView
import scandir_rs
import datetime

def scandir_rs_search(search_loc, search_var):
    return [
        os.path.join(root, filename).replace("[", "\\[").replace("]", "\\]").replace("\\\\?\\", "").replace(search_loc+os.sep, "")
        for root, directories, filenames in scandir_rs.walk.Walk(search_loc)
        for filename in filenames
        if search_var in filename
    ]

class FileWalker:
    def __init__(self, master):
        self.master = master
        self.master.title("Fast File Search")

        self.search_loc = tk.StringVar()
        self.search_loc.set(os.path.expanduser("~"))
        self.search_var = tk.StringVar()

        self.init_menubar()
        self.init_searchbar()
        self.init_treeview()

        self.files = []
        self.inside_search_files = []

    def init_menubar(self):
        self.menubar = tk.Menu(self.master)
        self.master.configure(menu=self.menubar)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open Folder", command=self.open_folder)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

    def open_folder(self):
        folder = tk.filedialog.askdirectory()
        if folder:
            self.search_loc.set(os.path.abspath(folder))

    def init_searchbar(self):
        ttk.Entry(
            self.master,
            textvariable=self.search_loc,
            justify="center",
        ).grid(row=0, column=0, sticky="ns")

        self.search_bar = ttk.Entry(self.master, textvariable=self.search_var)
        self.search_bar.grid(row=0, column=1, sticky="nsew")

        self.search_but = ttk.Button(
            self.master, text="Search", command=self.search)
        self.search_but.grid(row=0, column=2)

    def init_treeview(self):
        self.search_vew = ScrolledTreeView(self.master)
        self.search_vew.grid(row=1, column=0, columnspan=3, sticky="nsew")

        self.search_vew.heading("#0", text="File")
        self.search_vew["columns"] = (
            "fullpath", "type", "size", "Last Access")
        self.search_vew["displaycolumns"] = ("size", "Last Access")
        for col in self.search_vew["columns"]:
            self.search_vew.heading(col, text=col[0].upper() + col[1:])

        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

    def search(self):
        if not os.path.isdir(self.search_loc.get()):
            return
        self.search_but.configure(state="disabled")
        self.files = scandir_rs_search(self.search_loc.get(), self.search_var.get())
        self.search_vew.delete(*self.search_vew.get_children())
        for path in self.files:
            self.search_vew.insert("", "end", text=path, values=[path, "file"])
        self.master.after(100, self.stat_check)
        self.search_but.configure(state="enabled")

    def stat_check(self):
        stat_dict = {}
        print(self.files)
        for path in self.files:
            _path = os.path.join(self.search_loc.get(), str(path))
            stat = os.stat(_path)
            stat_dict[path] = [stat.st_size, stat.st_atime]
        self.search_vew.delete(*self.search_vew.get_children())
        for key, (size, atime) in stat_dict.items():
            atime = datetime.datetime.fromtimestamp(atime).strftime('%c')
            self.search_vew.insert("", "end", text=key, values=[key, "file", size, atime])


def main():
    root = tk.Tk()
    FileSearch = FileWalker(root)
    root.mainloop()

if __name__ == '__main__':
    main()