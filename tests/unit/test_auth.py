# tests/unit/test_auth.py
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.auth import LoginSystem

class TestLoginSystem:
    """Unit tests for LoginSystem class"""
    
    def setup_method(self):
        """Setup before each test"""
        self.auth = LoginSystem()
        self.valid_users = {
            "student": ("student1@school.com", "Student@123"),
            "teacher": ("teacher1@school.com", "Teacher@123"),
            "admin": ("admin@school.com", "Admin@123")
        }
    
    # ========== POSITIVE TESTS ==========
    
    def test_login_valid_student(self):
        """Positive: Valid student login"""
        email, password = self.valid_users["student"]
        result = self.auth.login(email, password)
        
        assert result["success"] == True
        assert "user" in result
        assert result["user"]["email"] == email
        print("✅ test_login_valid_student passed")
    
    def test_login_valid_teacher(self):
        """Positive: Valid teacher login"""
        email, password = self.valid_users["teacher"]
        result = self.auth.login(email, password)
        
        assert result["success"] == True
        assert result["user"]["email"] == email
        print("✅ test_login_valid_teacher passed")
    
    def test_login_valid_admin(self):
        """Positive: Valid admin login"""
        email, password = self.valid_users["admin"]
        result = self.auth.login(email, password)
        
        assert result["success"] == True
        assert result["user"]["email"] == email
        print("✅ test_login_valid_admin passed")
    
    # ========== NEGATIVE TESTS ==========
    
    def test_login_wrong_password(self):
        """Negative: Wrong password"""
        email, _ = self.valid_users["student"]
        result = self.auth.login(email, "WRONG_PASSWORD")
        
        assert result["success"] == False
        assert "error" in result or "message" in result
        print("✅ test_login_wrong_password passed")
    
    def test_login_invalid_email(self):
        """Negative: Invalid email format"""
        result = self.auth.login("invalid-email", "SomePass123")
        
        assert result["success"] == False
        print("✅ test_login_invalid_email passed")
    
    def test_login_nonexistent_user(self):
        """Negative: Non-existent user"""
        result = self.auth.login("nonexistent@school.com", "SomePass123")
        
        assert result["success"] == False
        print("✅ test_login_nonexistent_user passed")
    
    def test_login_empty_credentials(self):
        """Negative: Empty email/password"""
        result1 = self.auth.login("", "password")
        result2 = self.auth.login("test@test.com", "")
        
        assert result1["success"] == False
        assert result2["success"] == False
        print("✅ test_login_empty_credentials passed")

# ========== RUN ALL UNIT TESTS ==========

def run_unit_tests():
    """Run all unit tests"""
    print("=" * 50)
    print("🧪 RUNNING UNIT TESTS (LoginSystem)")
    print("=" * 50)
    
    tester = TestLoginSystem()
    tests = [
        ("Positive: Valid student", tester.test_login_valid_student),
        ("Positive: Valid teacher", tester.test_login_valid_teacher),
        ("Positive: Valid admin", tester.test_login_valid_admin),
        ("Negative: Wrong password", tester.test_login_wrong_password),
        ("Negative: Invalid email", tester.test_login_invalid_email),
        ("Negative: Non-existent user", tester.test_login_nonexistent_user),
        ("Negative: Empty credentials", tester.test_login_empty_credentials),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        tester.setup_method()  # Reset before each test
        try:
            print(f"\n🔍 {test_name}")
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"❌ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ ERROR: {type(e).__name__}: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print("📊 UNIT TEST SUMMARY")
    print("=" * 50)
    print(f"Total tests: {len(tests)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    
    if failed == 0:
        print("🎉 ALL UNIT TESTS PASSED!")
    else:
        print("⚠️  SOME UNIT TESTS FAILED")
    
    print("=" * 50)
    return failed == 0

if __name__ == "__main__":
    success = run_unit_tests()
    exit(0 if success else 1)