def main():
  print("Error: 'Seriously?' sample.py:2")
  for x in range(100):
    print('Log:', x)
  print("Errors in file: sample.py")
  print("  Error: 'x( program is dead' at line 6")
  print("  Error: 'Memory is messed up' at line 7")
  print("Error: 'Please code more carefully' SimpleNextError/sample.py:8")
  print("Error: 'Dont drink and code' sample.py:9")

if __name__ == '__main__':
  main()
