from __future__ import annotations
import customtkinter as ctk
from .ui.app import PortfolioApp

def run():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = PortfolioApp()
    app.mainloop()

if __name__ == "__main__":
    run()
