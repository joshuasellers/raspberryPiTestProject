# 🐷 Smart Piggy Bank  
**BLE-Triggered Savings Automation with Raspberry Pi + iOS**

A Raspberry Pi–powered physical piggy bank that automatically triggers a savings transfer when a recognized iPhone is brought nearby.

This project combines embedded systems, Bluetooth Low Energy (BLE), mobile development, and backend API design to create a tangible, habit-forming savings device.

---

## 📸 Concept

Bring your phone near the piggy bank → savings transfer is triggered → positive reinforcement.

Instead of tapping NFC, this version uses **custom BLE advertisement detection** from a companion iOS app.

---

# 🏗 Architecture Overview
```
iPhone App (BLE Advertiser)
↓
Raspberry Pi (BLE Scanner + Logic)
↓
Secure Backend API
↓
Banking Integration (ACH / Savings Transfer)
```

---

## 🧩 Components

### 1️⃣ Raspberry Pi
- Continuously scans for BLE advertisements
- Detects a custom service UUID from the iOS app
- Applies proximity filtering (RSSI threshold)
- Applies cooldown logic
- Calls backend API to initiate transfer
- Runs as a `systemd` service on boot

**Tech:**
- Python
- `bleak` (BLE scanning)
- `requests`
- Linux `systemd`

---

### 2️⃣ iOS Companion App
- Built with Swift + CoreBluetooth
- Advertises a custom BLE service UUID
- Runs in background
- Acts as an authenticated “presence token”

---

### 3️⃣ Backend API
- Validates device requests
- Handles authentication
- Applies rate limiting & idempotency
- Integrates with banking provider (Plaid / Stripe / ACH API)
- Logs savings activity

---

# 🔄 System Flow

1. User brings iPhone near piggy bank.
2. iOS app advertises custom BLE UUID.
3. Raspberry Pi detects UUID.
4. Pi validates:
   - UUID matches authorized device
   - RSSI above proximity threshold
   - Cooldown period not exceeded
5. Pi sends authenticated POST request to backend.
6. Backend triggers savings transfer.
7. Optional LED/sound feedback confirms success.

---

# 🔐 Security Design

- No banking credentials stored on the Pi
- Backend handles all financial integrations
- Authenticated requests from Pi to backend
- Cooldown logic prevents repeated triggers
- Idempotency protection on backend
- Optional: signed device requests

---

# 🛠 Installation (Raspberry Pi)

## 1. Install dependencies

```bash
sudo apt update
sudo apt install python3-pip
pip3 install bleak requests
```
## Run the scanner
```
python3 app.py
```
## 3. Run on boot (systemd)
Create:
```
sudo nano /etc/systemd/system/piggybank.service
```
Add:
```
[Unit]
Description=Smart Piggy Bank
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/piggybank/app.py
WorkingDirectory=/home/pi/piggybank
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```
Enable:
```
sudo systemctl enable piggybank
sudo systemctl start piggybank
```
