# chatbot_gui.py
import customtkinter as ctk
from tkinter import scrolledtext
from datetime import datetime
from chatbot import handle_query

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"


class ChatBotGUI:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Support Chatbot")
        self.window.geometry("900x700")
        
        # Configure grid weight
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface"""
        # Main container
        main_frame = ctk.CTkFrame(self.window)
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Title section
        title_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="🤖 Support Chatbot",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left", padx=10)
        
        # Clear chat button
        self.clear_btn = ctk.CTkButton(
            title_frame,
            text="Clear Chat",
            width=100,
            command=self.clear_chat,
            fg_color="#dc3545",
            hover_color="#c82333"
        )
        self.clear_btn.pack(side="right", padx=10)
        
        # Theme toggle button
        self.theme_btn = ctk.CTkButton(
            title_frame,
            text="🌙 Dark",
            width=100,
            command=self.toggle_theme,
        )
        self.theme_btn.pack(side="right", padx=5)
        self.current_theme = "dark"
        
        # About button
        self.about_btn = ctk.CTkButton(
            title_frame,
            text="ℹ️",
            width=40,
            command=self.show_about,
        )
        self.about_btn.pack(side="right", padx=5)
        
        # Chat display area (scrollable frame)
        self.chat_frame = ctk.CTkScrollableFrame(
            main_frame,
            fg_color=("#E8E8E8", "#2B2B2B")
        )
        self.chat_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.chat_frame.grid_columnconfigure(0, weight=1)
        
        # Input section
        input_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        input_frame.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Text input
        self.input_field = ctk.CTkTextbox(
            input_frame,
            height=80,
            wrap="word",
            font=ctk.CTkFont(size=14)
        )
        self.input_field.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.input_field.bind("<Return>", self.handle_return_key)
        self.input_field.bind("<Shift-Return>", lambda e: None)  # Allow Shift+Enter for newline
        
        # Send button
        self.send_btn = ctk.CTkButton(
            input_frame,
            text="Send",
            width=100,
            height=80,
            command=self.send_message,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#28a745",
            hover_color="#218838"
        )
        self.send_btn.grid(row=0, column=1)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="Ready to help! Type your question above.",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.status_label.grid(row=3, column=0, padx=10, pady=(0, 5))
        
        # Welcome message
        self.add_bot_message(
            "Hello! 👋 I'm your support assistant. I can help you with:\n\n"
            "💳 Billing & Payments\n"
            "   • Billing inquiries, invoices, refunds\n"
            "   • Payment disputes, subscription changes\n\n"
            "👤 Account Management\n"
            "   • Password resets, account creation\n"
            "   • Security settings, 2FA setup\n"
            "   • Data export, multiple accounts\n\n"
            "📦 Orders & Tracking\n"
            "   • Order status, delivery tracking\n"
            "   • Shipping information\n\n"
            "💻 Technical Support\n"
            "   • App crashes, bug reports\n"
            "   • Mobile apps (iOS/Android)\n"
            "   • Integration help, API support\n\n"
            "⚙️ Settings & Features\n"
            "   • Notification preferences\n"
            "   • Feature requests, pricing info\n"
            "   • Business hours, trial extensions\n\n"
            "How can I assist you today?"
        )
        
    def handle_return_key(self, event):
        """Handle Enter key press"""
        # If Shift is not pressed, send message
        if not event.state & 0x1:  # 0x1 is Shift modifier
            self.send_message()
            return "break"  # Prevent default newline insertion
        return None  # Allow Shift+Enter to create newline
        
    def send_message(self):
        """Send user message and get bot response"""
        user_text = self.input_field.get("1.0", "end-1c").strip()
        
        if not user_text:
            return
        
        # Clear input field
        self.input_field.delete("1.0", "end")
        
        # Add user message
        self.add_user_message(user_text)
        
        # Update status
        self.status_label.configure(text="Thinking...")
        self.send_btn.configure(state="disabled", text="...")
        
        # Process in main thread after a short delay to keep UI responsive
        # pyDatalog is not thread-safe, so we must call handle_query in main thread
        self.window.after(100, lambda: self.get_bot_response(user_text))
        
    def get_bot_response(self, user_text):
        """Get response from chatbot (runs in main thread)"""
        try:
            response = handle_query(user_text)
            self.add_bot_message(response)
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            self.add_bot_message(error_msg)
        finally:
            # Re-enable send button
            self.send_btn.configure(state="normal", text="Send")
            self.status_label.configure(text="Ready to help!")
            self.input_field.focus()
    
    def add_user_message(self, message):
        """Add user message to chat"""
        self.add_message(message, is_user=True)
        
    def add_bot_message(self, message):
        """Add bot message to chat"""
        self.add_message(message, is_user=False)
        
    def add_message(self, message, is_user=True):
        """Add a message bubble to the chat"""
        # Create message container
        msg_container = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        msg_container.grid(row=len(self.chat_frame.winfo_children()), column=0, pady=5, sticky="ew")
        msg_container.grid_columnconfigure(0 if is_user else 2, weight=1)
        
        # Configure colors based on sender
        if is_user:
            bg_color = ("#007bff", "#0056b3")  # Blue for user
            text_color = "white"
            icon = "👤"
            align = "e"
            col = 1
        else:
            bg_color = ("#f8f9fa", "#3a3a3a")  # Gray for bot
            text_color = ("black", "white")
            icon = "🤖"
            align = "w"
            col = 1
        
        # Message bubble
        bubble = ctk.CTkFrame(
            msg_container,
            fg_color=bg_color,
            corner_radius=15
        )
        bubble.grid(row=0, column=col, sticky=align, padx=10)
        
        # Header with icon and timestamp
        header_frame = ctk.CTkFrame(bubble, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(10, 5))
        
        icon_label = ctk.CTkLabel(
            header_frame,
            text=icon,
            font=ctk.CTkFont(size=14)
        )
        icon_label.pack(side="left")
        
        name_label = ctk.CTkLabel(
            header_frame,
            text="You" if is_user else "Support Bot",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=text_color
        )
        name_label.pack(side="left", padx=5)
        
        time_label = ctk.CTkLabel(
            header_frame,
            text=datetime.now().strftime("%H:%M"),
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        time_label.pack(side="right")
        
        # Message text
        msg_label = ctk.CTkLabel(
            bubble,
            text=message,
            font=ctk.CTkFont(size=14),
            text_color=text_color,
            wraplength=500,
            justify="left",
            anchor="w"
        )
        msg_label.pack(fill="both", padx=15, pady=(0, 10))
        
        # Scroll to bottom
        self.window.after(100, lambda: self.chat_frame._parent_canvas.yview_moveto(1.0))
        
    def clear_chat(self):
        """Clear all messages from chat"""
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        
        # Add welcome message back
        self.add_bot_message(
            "Chat cleared! How can I help you today?"
        )
    
    def toggle_theme(self):
        """Toggle between dark and light theme"""
        if self.current_theme == "dark":
            ctk.set_appearance_mode("light")
            self.theme_btn.configure(text="☀️ Light")
            self.current_theme = "light"
        else:
            ctk.set_appearance_mode("dark")
            self.theme_btn.configure(text="🌙 Dark")
            self.current_theme = "dark"
    
    def show_about(self):
        """Show about dialog"""
        about_window = ctk.CTkToplevel(self.window)
        about_window.title("About Support Chatbot")
        about_window.geometry("400x350")
        about_window.resizable(False, False)
        
        # Make it modal
        about_window.transient(self.window)
        about_window.grab_set()
        
        # Content
        content_frame = ctk.CTkFrame(about_window)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Icon
        icon_label = ctk.CTkLabel(
            content_frame,
            text="🤖",
            font=ctk.CTkFont(size=48)
        )
        icon_label.pack(pady=(10, 5))
        
        # Title
        title_label = ctk.CTkLabel(
            content_frame,
            text="Support Chatbot",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=5)
        
        # Version
        version_label = ctk.CTkLabel(
            content_frame,
            text="Version 1.0",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        version_label.pack(pady=2)
        
        # Description
        desc_label = ctk.CTkLabel(
            content_frame,
            text="An intelligent support assistant powered by\npyDatalog logic programming and NLU.",
            font=ctk.CTkFont(size=13),
            justify="center"
        )
        desc_label.pack(pady=15)
        
        # Features
        features_text = "✨ Features:\n\n• Intent Recognition\n• Entity Extraction\n• Smart Escalation\n• Rule-based Reasoning"
        features_label = ctk.CTkLabel(
            content_frame,
            text=features_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        features_label.pack(pady=10)
        
        # Close button
        close_btn = ctk.CTkButton(
            content_frame,
            text="Close",
            width=100,
            command=about_window.destroy
        )
        close_btn.pack(pady=15)
        
    def run(self):
        """Start the GUI application"""
        self.input_field.focus()
        self.window.mainloop()


if __name__ == "__main__":
    app = ChatBotGUI()
    app.run()
