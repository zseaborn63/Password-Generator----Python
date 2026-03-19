def generate_password():
    print("Hello Password Generator!")

    # Get user input for security level 1-3
    print("Welcome to The Password Generator!")
    print("Please choose a security level from the options below:")
    print("\t 1: Basic Password (default)")
    print("\t 2: Basic Safety Password")
    print("\t 3: Super Secure Password")
    choice = input("Enter your desired level of password security now!\n\t-->")

    choice = "1" if choice == "" else choice
    safety_net = 1
    while choice not in ["1", "2", "3"] and safety_net <= 3:
        safety_net += 1
        print(f"Please enter a valid choice....{3 - safety_net} chances before defaulting to Basic Password")
        choice = input("Enter your desired level of password security now!\n\t-->")

    if safety_net == 3:
        print("Defaulting to Basic Password")
        choice = 1

    _sec_level = int(choice)

    # TODO:  Fetch words from API

    # TODO:  Replace one letter w/ integer

    # TODO:  Replace one letter w/ special character

    # TODO:  Misspell one word in order to introduce security

if __name__ == "__main__":
    generate_password()
    exit(0)