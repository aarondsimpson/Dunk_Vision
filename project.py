from src.user_interface.dunk_vision_app import DunkVisionApp 

def main():
    print("Creating DunkVisionApp instance...")
    app = DunkVisionApp()
    print("Starting the application...")
    app.mainloop()

if __name__ == "__main__":
    main()