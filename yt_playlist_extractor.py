import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import yt_dlp


def fetch_playlist(url):
    opts = {
        "quiet": True,
        "extract_flat": "in_playlist",
        "skip_download": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
    entries = [e for e in (info.get("entries") or []) if e]
    results = []
    for i, e in enumerate(entries, 1):
        title = e.get("title", "Unknown")
        vid = e.get("id") or e.get("url")
        link = f"https://www.youtube.com/watch?v={vid}" if vid and "http" not in str(vid) else vid
        results.append((i, title, link))
    return results


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Playlist Link Extractor")
        self.geometry("750x500")
        self.data = []

        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")
        ttk.Label(top, text="Playlist URL:").pack(side="left")
        self.url_entry = ttk.Entry(top)
        self.url_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.fetch_btn = ttk.Button(top, text="Fetch", command=self.on_fetch)
        self.fetch_btn.pack(side="left")

        self.status = ttk.Label(self, text="", padding=(10, 0))
        self.status.pack(fill="x")

        cols = ("no", "title", "link")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        self.tree.heading("no", text="#")
        self.tree.heading("title", text="Title")
        self.tree.heading("link", text="Link")
        self.tree.column("no", width=40, anchor="center")
        self.tree.column("title", width=350)
        self.tree.column("link", width=300)
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree.bind("<Double-1>", lambda e: self.copy_selected_link())

        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Copy Link", command=self.copy_selected_link)
        self.tree.bind("<Button-3>", self.show_context_menu)

        bottom = ttk.Frame(self, padding=10)
        bottom.pack(fill="x")
        ttk.Button(bottom, text="Save to .txt", command=self.on_save).pack(side="right")
        ttk.Button(bottom, text="Copy Selected Link", command=self.copy_selected_link).pack(side="right", padx=5)

    def on_fetch(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Enter a playlist URL")
            return
        self.fetch_btn.config(state="disabled")
        self.status.config(text="Fetching...")
        self.tree.delete(*self.tree.get_children())
        threading.Thread(target=self._fetch_worker, args=(url,), daemon=True).start()

    def _fetch_worker(self, url):
        try:
            data = fetch_playlist(url)
            self.after(0, self._on_fetch_done, data, None)
        except Exception as e:
            self.after(0, self._on_fetch_done, None, str(e))

    def _on_fetch_done(self, data, error):
        self.fetch_btn.config(state="normal")
        if error:
            self.status.config(text="Failed")
            messagebox.showerror("Error", error)
            return
        self.data = data
        for no, title, link in data:
            self.tree.insert("", "end", values=(no, title, link))
        self.status.config(text=f"{len(data)} videos found")

    def show_context_menu(self, event):
        row = self.tree.identify_row(event.y)
        if row:
            self.tree.selection_set(row)
            self.menu.post(event.x_root, event.y_root)

    def copy_selected_link(self):
        sel = self.tree.selection()
        if not sel:
            return
        link = self.tree.item(sel[0], "values")[2]
        self.clipboard_clear()
        self.clipboard_append(link)
        self.status.config(text="Link copied to clipboard")

    def on_save(self):
        if not self.data:
            messagebox.showinfo("Nothing to save", "Fetch a playlist first")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text file", "*.txt")])
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            for no, title, link in self.data:
                f.write(f"{no}. {title} - {link}\n")
        messagebox.showinfo("Saved", f"Saved to {path}")


if __name__ == "__main__":
    App().mainloop()
