import customtkinter as ctk
from PIL import Image # Import pillow to handle images
import os

# Set the appearance mode to light for the warm colors to pop
ctk.set_appearance_mode("Light")

# Define our soothing lo-fi color palette
COLORS = {
    "bg_cream": "#F8F0E3",
    "card_beige": "#F0EAD6",
    "text_terracotta": "#B56547",
    "accent_brown": "#D9B99B",
    "button_hover": "#E5DBC8"
}

# Playful fonts
PLAYFUL_FONT = "Comic Sans MS" 
BODY_FONT = "Helvetica"

class StudyBuddyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("ZenFocus Companion")
        self.geometry("450x700") # Made slightly taller for images
        self.configure(fg_color=COLORS["bg_cream"])
        self.resizable(False, False)

        # --- IMAGE LOADING SETUP ---
        # Get the path to the 'assets' folder next to this script
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.assets_path = os.path.join(current_path, "assets")

        # Helper function to load images easily
        def load_img(filename, size):
            return ctk.CTkImage(light_image=Image.open(os.path.join(self.assets_path, filename)),
                                size=size)

        # Load the three character images (adjust size=(x,y) if needed)
        # We use try/except in case you run the script before drawing them
        try:
            self.img_setup = load_img("image0.png", size=(180, 180))
            self.img_focus = load_img("img2.png", size=(200, 200))
            self.img_break = load_img("image1.png", size=(180, 180))
            images_loaded = True
        except FileNotFoundError:
            print("Warning: Character PNGs not found in 'assets' folder. Placeholders used.")
            images_loaded = False

        # Main Card Container
        self.main_card = ctk.CTkFrame(self, fg_color=COLORS["card_beige"], 
                                      border_color=COLORS["text_terracotta"], 
                                      border_width=4, corner_radius=30)
        self.main_card.pack(fill="both", expand=True, padx=25, pady=25)

        # -- STATE 1: SETUP FRAME --
        self.setup_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        
        self.title_label = ctk.CTkLabel(self.setup_frame, text="READY TO FOCUS? ✨", 
                                        font=(PLAYFUL_FONT, 26, "bold"), 
                                        text_color=COLORS["text_terracotta"])
        self.title_label.pack(pady=(30, 10))

        # Character Image Label
        self.char_setup_label = ctk.CTkLabel(self.setup_frame, text="", image=self.img_setup if images_loaded else None)
        self.char_setup_label.pack(pady=(0, 10))

        self.slider_label = ctk.CTkLabel(self.setup_frame, text="focus duration", 
                                         font=(PLAYFUL_FONT, 18, "italic"), 
                                         text_color=COLORS["text_terracotta"])
        self.slider_label.pack(pady=(10, 5))
        
        # Custom-styled slider
        self.time_slider = ctk.CTkSlider(self.setup_frame, from_=5, to=120, number_of_steps=23,
                                         fg_color=COLORS["accent_brown"],      
                                         progress_color=COLORS["accent_brown"], 
                                         button_color=COLORS["text_terracotta"], 
                                         button_hover_color=COLORS["text_terracotta"],
                                         command=self.update_slider_text)
        self.time_slider.set(45)
        self.time_slider.pack(pady=(5, 10), padx=30, fill="x")

        self.slider_value_label = ctk.CTkLabel(self.setup_frame, text="45 min", 
                                               font=(PLAYFUL_FONT, 22, "bold"), 
                                               text_color=COLORS["text_terracotta"])
        self.slider_value_label.pack(pady=(0, 20))

        self.start_btn = ctk.CTkButton(self.setup_frame, text="START!", height=55, 
                                       font=(PLAYFUL_FONT, 22, "bold"),
                                       fg_color=COLORS["card_beige"], text_color=COLORS["text_terracotta"],   
                                       border_color=COLORS["text_terracotta"], border_width=3, corner_radius=20,
                                       hover_color=COLORS["button_hover"],
                                       command=self.start_focus)
        self.start_btn.pack(pady=10, padx=50, fill="x")

        # -- STATE 2: FOCUS FRAME --
        self.focus_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        
        self.status_label = ctk.CTkLabel(self.focus_frame, text="Status: Monitoring ✨", 
                                         font=(BODY_FONT, 16), text_color=COLORS["accent_brown"])
        self.status_label.pack(pady=(30, 10))

        # Focus Character Image Label (Slightly larger)
        self.char_focus_label = ctk.CTkLabel(self.focus_frame, text="", image=self.img_focus if images_loaded else None)
        self.char_focus_label.pack(pady=10)

        self.timer_label = ctk.CTkLabel(self.focus_frame, text="45:00", 
                                        font=(PLAYFUL_FONT, 50, "bold"), 
                                        text_color=COLORS["text_terracotta"])
        self.timer_label.pack(pady=10)

        self.quote_label = ctk.CTkLabel(self.focus_frame, text="Stay with the flow.", 
                                        font=(PLAYFUL_FONT, 16, "italic"), 
                                        text_color=COLORS["accent_brown"])
        self.quote_label.pack(pady=(0, 20))

        self.debug_btn = ctk.CTkButton(self.focus_frame, text="Skip to Break (Debug)", 
                                       fg_color=COLORS["accent_brown"], font=(BODY_FONT, 12),
                                       command=self.start_break)
        self.debug_btn.pack(pady=10)

        # -- STATE 3: BREAK FRAME --
        self.break_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        
        self.break_title = ctk.CTkLabel(self.break_frame, text="Rest & Hydrate 💧", 
                                        font=(PLAYFUL_FONT, 26, "bold"), 
                                        text_color=COLORS["text_terracotta"])
        self.break_title.pack(pady=(40, 10))

        # Break Character Image Label
        self.char_break_label = ctk.CTkLabel(self.break_frame, text="", image=self.img_break if images_loaded else None)
        self.char_break_label.pack(pady=10)

        self.hydrate_label = ctk.CTkLabel(self.break_frame, text="Drink 150ml of water.", 
                                          font=(PLAYFUL_FONT, 18), text_color=COLORS["accent_brown"])
        self.hydrate_label.pack(pady=10)

        self.reset_btn = ctk.CTkButton(self.break_frame, text="I'm Hydrated & Ready!", height=55, 
                                       font=(PLAYFUL_FONT, 20, "bold"),
                                       fg_color=COLORS["card_beige"], text_color=COLORS["text_terracotta"],
                                       border_color=COLORS["text_terracotta"], border_width=3, corner_radius=20,
                                       hover_color=COLORS["button_hover"],
                                       command=self.reset_app)
        self.reset_btn.pack(pady=30, padx=50, fill="x")

        # Start by showing the Setup Frame
        self.setup_frame.pack(fill="both", expand=True)

    # --- UI Logic Functions ---
    def update_slider_text(self, value):
        self.slider_value_label.configure(text=f"{int(value)} min")

    def start_focus(self):
        self.setup_frame.pack_forget()
        self.focus_frame.pack(fill="both", expand=True)

    def start_break(self):
        self.focus_frame.pack_forget()
        self.break_frame.pack(fill="both", expand=True)

    def reset_app(self):
        self.break_frame.pack_forget()
        self.setup_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = StudyBuddyApp()
    app.mainloop()