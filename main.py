import subprocess
import sys

def main():
    """
    Main script to run tasks.
    """
    while True:
        print("\nSelect a task to run:")
        print("1: Task 1 (Maximum Flow)")
        print("2: Task 2 (Trie)")
        print("q: Quit")

        choice = input("Your choice: ")

        script_path = None
        if choice == '1':
            print("\n--- Running Task 1 ---\n")
            script_path = "task_1/task_1.py"
        elif choice == '2':
            print("\n--- Running Task 2 ---\n")
            script_path = "task_2/task_2.py"
        elif choice.lower() == 'q':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or q.")
            continue

        try:
            # Use the same Python interpreter that is running main.py
            subprocess.run([sys.executable, script_path], check=True)
        except FileNotFoundError:
            print(f"Error: File '{script_path}' not found.")
        except subprocess.CalledProcessError as e:
            print(f"Error during task execution: {e}")
        
        print(f"\n--- Task {choice} finished ---")

if __name__ == "__main__":
    main()