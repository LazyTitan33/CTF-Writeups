import sys

def simple_calculator():
    print("Welcome to the Simple Calculator!")
    print("Enter a mathematical expression:", end=' ')
    expression = input()
    sys.stdin.close()
    try:
        blacklist = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for x in expression:
            if x in blacklist:
                print(f"{x} is not allowed!")
                exit()
        result = eval(expression)
        print(f"The result is: {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    simple_calculator()
