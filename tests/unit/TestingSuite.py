import os
import sys

class PicoTestBase:
    is_test_class = True

class TestingSuite:
    TEST_DIR = 'unit'
    COMPONENTS_DIR = 'components'
    LIB_DIR = 'lib'

    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.test_count = 0
        self.failed_tests = []

    def get_test_methods(self, obj):
        methods = [method for method in dir(obj) if method.startswith('test_') and callable(getattr(obj, method))]
        self.test_count += len(methods)
        return methods

    def run_all(self):
        print("=" * 50)
        print("Smart Home Unit Testing Suite")
        print("=" * 50)

        subs = self.find_test_subclasses()
        if len(subs) == 0:
            print("❌ No tests found")
            return

        print(f"Found {len(subs)} test class(es)\n")

        for obj in subs:
            self.run_test_class(obj)

        # Print summary
        print("\n" + "=" * 50)
        print("Test Summary")
        print("=" * 50)
        print(f"Total tests: {self.test_count}")
        print(f"✅ Passed: {self.tests_passed}")
        print(f"❌ Failed: {self.tests_failed}")

        if self.tests_failed > 0:
            print("\nFailed tests:")
            for test_name, error in self.failed_tests:
                print(f"  - {test_name}: {error}")

        if self.test_count == 0:
            print("\n⚠️  No tests found")
        elif self.tests_passed == self.test_count:
            print("\n🎉 All tests passed!")
        else:
            print(f"\n⚠️  {self.tests_failed} test(s) failed")

    def run_test_class(self, obj):
        class_name = obj.__name__
        print(f"\n📦 Running {class_name}")
        print("-" * 50)

        inst = obj()
        test_methods = self.get_test_methods(inst)

        for m in test_methods:
            method = getattr(inst, m)
            try:
                print(f"  ▶ {m}...", end=" ")
                method()
                self.tests_passed += 1
                print("✅ PASSED")
            except AssertionError as e:
                self.tests_failed += 1
                self.failed_tests.append((f"{class_name}.{m}", str(e)))
                print(f"❌ FAILED: {e}")
            except Exception as e:
                self.tests_failed += 1
                self.failed_tests.append((f"{class_name}.{m}", str(e)))
                print(f"❌ ERROR: {e}")

    def find_test_subclasses(self):
        sys.path.insert(0, '..')  
        sys.path.insert(0, f'../{self.COMPONENTS_DIR}')  
        sys.path.insert(0, f'../{self.LIB_DIR}')  

        test_modules = []
        test_subclasses = []

        for filename in os.listdir():
            if filename.endswith(".py") and filename != 'TestingSuite.py' and not filename.startswith('_'):
                module_name = filename.split(".")[0]
                test_modules.append(module_name)

        for module_name in test_modules:
            try:
                module = __import__(module_name)
                for name in dir(module):
                    obj = getattr(module, name)
                    if isinstance(obj, type) and hasattr(obj, 'is_test_class') and obj.is_test_class:
                        test_subclasses.append(obj)
            except ImportError as e:
                print(f"⚠️  Warning: Could not import {module_name}: {e}")

        return test_subclasses

if __name__ == "__main__":
    suite = TestingSuite()
    suite.run_all()
