# Unit tests for login
from src.auth import LoginSystem

def test_admin_login():
    """Test admin login"""
    auth = LoginSystem()
    result = auth.login("admin@school.com", "Admin@123")
    assert result["success"] == True
    print("✅ Test 1: Admin login passed")

def test_student_login():
    """Test student login"""
    auth = LoginSystem()
    result = auth.login("student1@school.com", "Student@123")
    assert result["success"] == True
    print("✅ Test 2: Student login passed")

def test_wrong_password():
    """Test wrong password"""
    auth = LoginSystem()
    result = auth.login("admin@school.com", "wrong")
    assert result["success"] == False
    print("✅ Test 3: Wrong password test passed")

def test_wrong_email():
    """Test wrong email"""
    auth = LoginSystem()
    result = auth.login("wrong@email.com", "password")
    assert result["success"] == False
    print("✅ Test 4: Wrong email test passed")

# Run all tests
if __name__ == "__main__":
    print("=" * 50)
    print("RUNNING UNIT TESTS")
    print("=" * 50)
    test_admin_login()
    test_student_login()
    test_wrong_password()
    test_wrong_email()
    print("=" * 50)
    print("✅ ALL 4 TESTS PASSED!")
    print("=" * 50)