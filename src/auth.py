# Simple login system
class LoginSystem:
    def __init__(self):
        # User database
        self.users = {
            "admin@school.com": {"password": "Admin@123", "name": "Admin", "role": "admin", "id": "AD001"},
            "student1@school.com": {"password": "Student@123", "name": "Ali Khan", "role": "student", "id": "ST001"},
            "teacher1@school.com": {"password": "Teacher@123", "name": "Sara Ahmed", "role": "teacher", "id": "TE001"}
        }
    
    def login(self, email, password):
        """Check if login is correct"""
        if email in self.users:
            if self.users[email]["password"] == password:
                return {
                    "success": True,
                    "message": "Login successful",
                    "user": self.users[email]
                }
        return {
            "success": False,
            "message": "Invalid email or password"
        }