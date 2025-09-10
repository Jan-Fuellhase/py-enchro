# Encrypt/Decrypt

A simple, cross-platform tool for AES-256 file encryption. Built with Python and Kivy, it runs on both Windows and Android.


---

### ► Features

*   **Strong Encryption:** Uses AES-256 (GCM mode) for secure file encryption.
*   **Password Protection:** Encrypt your files with a password.
*   **Customizable Salt:** Option to provide a custom salt for added security. Uses a default salt if none is provided.
*   **Cross-Platform:** Runs on Windows, and can be packaged for Android.
*   **Simple Interface:** A clean and straightforward UI for encrypting and decrypting files.

---

### ► Getting Started

#### Prerequisites

Make sure you have Python 3 installed on your system.

#### Running the App

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd enchrowithpython
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    python enchrowithpython.py
    ```

---

### ► Build for Android

To package the application for Android, use [Buildozer](https://buildozer.readthedocs.io/en/latest/).

1.  **Install Buildozer:**
    ```bash
    pip install buildozer
    ```

2.  **Build the APK:**
    ```bash
    buildozer android debug
    ```
    The APK will be located in the `bin/` directory.

---

### ► How It Works

The application uses the `pycryptodome` library to perform AES-256 encryption.

*   A 256-bit key is derived from your password and a salt using PBKDF2.
*   The encrypted file (`.enc`) contains the salt, nonce, GCM tag, and the ciphertext, which are all required for decryption.

