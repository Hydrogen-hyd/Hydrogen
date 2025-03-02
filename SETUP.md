# Hydrogen Blockchain Setup Guide

## Prerequisites
Before you begin, ensure you have the following installed:
- The latest version of Python
- A laptop (Obviously)
- Pip (Python package manager)

---

## Step 1: Download the Hydrogen Blockchain Files
1. Clone the Hydrogen repository from GitHub or download the files manually.
   ```sh
   git clone <hydrogen-repo-url>
   cd hydrogen
   ```

---

## Step 2: Install Dependencies
2. Open a terminal in the Hydrogen project directory and install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

---

## Step 3: Set Up a Virtual Environment
3. Create a virtual environment:
   ```sh
   python3 -m venv venv
   ```
4. Activate the virtual environment:
   ```sh
   source venv/bin/activate
   ```

---

## Step 4: Start the Blockchain Services
5. Open a **new terminal** and activate the virtual environment:
   ```sh
   source venv/bin/activate && python rpc_server.py
   ```
   - Keep this terminal open, as it runs the RPC server.

6. Open another **new terminal** and activate the virtual environment:
   ```sh
   source venv/bin/activate && python app.py
   ```
   - After running this command, a link will appear in the terminal. **Click the link** to open the blockchain's website and start testing.

---

## Step 5: Shutting Down
7. To finish, simply close all terminals. This will stop the blockchain services.

---

Your Hydrogen blockchain setup is now complete, so now you can test the blockchain out!
