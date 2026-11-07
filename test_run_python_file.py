from functions.run_python_file import run_python_file

print("test 1")
print(run_python_file("calculator", "main.py"))

print("test 2")
print(run_python_file("calculator", "main.py", ["3 + 5"]))

print("test 3")
print(run_python_file("calculator", "tests.py"))

print("test 4")
print(run_python_file("calculator", "../main.py"))

print("test 5")
print(run_python_file("calculator", "nonexistent.py"))

print("test 6")
print(run_python_file("calculator", "lorem.txt"))

