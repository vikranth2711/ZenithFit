# ZenithFit
The ZenithFIt is a web-based application built using Flask and MySQL to help gym owners and members manage their workout routines, meal plans, memberships, and payments efficiently. The system enables users to register, track their progress, and access personalized workout and meal plans.

## 🚀 Features
- **User Authentication:** Secure login and signup with password hashing.
- **Workout Plan Management:** Create, update, and track workout routines.
- **Meal Plan Management:** Personalized diet plans for gym members.
- **Exercise Tracking:** Log and update exercises for better fitness tracking.
- **Membership Management:** Register new members and manage membership plans.
- **Payment Handling:** Track payments and membership fees.
- **User Dashboard:** View meal plans, workouts, and fitness stats.

## 🛠️ Tech Stack
- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** MySQL
- **Libraries:** Flask-MySQLdb, Jinja2, Werkzeug (for password hashing)

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.x
- MySQL Database
- Flask & required dependencies

### Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/vikranth2711/ZenithFit.git
   cd gym-management-system
   ```


3. **Setup MySQL Database**
   - Create a database in MySQL.
   - Update database credentials in `app.py`.

4. **Run the Flask App**
   ```bash
   python app.py
   ```

5. **Access the App**
   Open a browser and visit: `http://127.0.0.1:5000/`

## 🔒 Security Measures
- Passwords are hashed using **Werkzeug**.
- Session-based authentication for user security.
- Uses MySQL for data persistence.

## 📝 Future Enhancements
- Add an admin panel for managing members and plans.
- Implement an appointment scheduling feature.
- Integrate payment gateway for online transactions.

## 📜 License
This project is open-source and available under the **MIT License**.

## 👨‍💻 Contributing
Pull requests are welcome! If you'd like to contribute, please fork the repository and submit a PR.
---
