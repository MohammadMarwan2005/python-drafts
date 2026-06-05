import ast

with open("/home/mohammad-mint/PythonProjects/learn_kbs2/ast/input.py", "r") as f:
    source = f.read()


tree = ast.parse(source)

print(ast.dump(tree, indent=4))
