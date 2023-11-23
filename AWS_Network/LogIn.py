import sys
import basic_network


class Infrastructure:
    def selector(self) -> int:
        Infrastructure().welcome()
        selection = Infrastructure().selections()
        if selection == 1:
            Infrastructure().basic_network()
            selection = input("Do you agree? (Yes/No) : ")
            if selection.upper() == 'YES':
                basic_network.object_creation()   # creates  VPC with other resources
                Infrastructure().selector()
            elif selection.upper() == 'NO':
                Infrastructure().selector()
            else:
                print("Wrong Value inserted")
                Infrastructure().selector()
        elif selection == 2:
            Infrastructure().frontend_advanced_network()
            selection = input("Do you agree? (Yes/No) : ")
            if selection.upper() == 'YES':
                print("Production front end advanced network")
            elif selection.upper() == 'NO':
                Infrastructure().selector()
            else:
                print("Wrong Value inserted")
                Infrastructure().selector()
        elif selection == 3:
            Infrastructure().backend_advanced_network()
            selection = input("Do you agree? (Yes/No) : ")
            if selection.upper() == 'YES':
                print("Production  backend Advanced network")
            elif selection.upper() == 'NO':
                Infrastructure().selector()
            else:
                print("Wrong Value inserted")
                Infrastructure().selector()
        elif selection == 4:
            Infrastructure().entire_architecture()
            selection = input("Do you agree? (Yes/No) : ")
            if selection.upper() == 'YES':
                print("Production  all infrastructure")
            elif selection.upper() == 'NO':
                Infrastructure().selector()
            else:
                print("Wrong Value inserted")
                Infrastructure().selector()
        elif selection == 5:
            print("Thank you for using our service, Bye")
            sys.exit()
        return 0

    def welcome(self):
        print("\nWelcome to Group D network infrastructure App.\n"
              "Please select the infrastructure to build.\n")
        infrastructure = ["Basic Infrastructure", "Front-end Advanced Infrastructure",
                          "Backend Advanced Infrastructure", "Entire System "
                                                             "(Use pre-build configurations)", "Exit"]
        index = 0
        for item in infrastructure:
            print(f"{index + 1}) {infrastructure[index]}")
            index += 1

    def selections(self):
        try:
            selection = int(input("Please input your selection: "))
            while selection not in range(0, 6):
                print("Please, selection must be between 1 and 5 inclusive.")
                Infrastructure().selections()
                return
            else:
                return selection
        except ValueError:
            print(" Please, Whole numbers only.selection must be between 1 and 5 inclusive.")
            selection = Infrastructure().selections()
            return selection

    def basic_network(self):
        infrastructure = ["VPC", "Internet gateway", "Route Tables",
                          "Private and Public Subnets", "Security Groups"]
        print("\nThe following infrastructures will be created:")
        index = 0
        for structure in infrastructure:
            print(f"{index + 1}) {structure}")
            index += 1

    def frontend_advanced_network(self):
        infrastructure = ["Elastic load balancer", "Target groups", "Listeners"]
        print("\nThe following infrastructures will be created:")
        index = 0
        for structure in infrastructure:
            print(f"{index + 1}) {structure}")
            index += 1

    def backend_advanced_network(self):
        infrastructure = ["Gateway VPC endpoint", "Database (RDS)", "DynamoDB", "S3 bucket"]
        print("\nThe following infrastructures will be created:")
        index = 0
        for structure in infrastructure:
            print(f"{index + 1}) {structure}")
            index += 1

    def entire_architecture(self):
        infrastructure = ["All infrastructure needed"]
        print("\nThe following infrastructures will be created:")
        index = 0
        for structure in infrastructure:
            print(f"{index + 1}) {structure}")
            index += 1


Infrastructure().selector()
