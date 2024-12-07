import signal
import sys
from AliasClientManager import AliasClientManager

class AliasClientCLI():
    def __init__(self):
        self.acm = AliasClientManager()

    def quit(self):
        print("Quitting...")
        self.acm.close_db()
        sys.exit(0)

    def signal_handler(self, sig, frame):
        self.quit()

    def cli_app(self):
        try:
            self.acm.open_db()
        except Exception as e:
            print(f"Error opening database: {e}")
            self.quit()

        help_text = """
            Welcome to the Alias Client Manager CLI App!
            This program will help you manage your alias clients in your Pi-hole.
            Available commands:
                - help: Show this help message
                - list: List all alias clients
                - add <name> (comment): Add a new alias client
                - delete <id>: Delete an alias client
                - update <id> (name=<name>) (comment=<comment>): Update an alias client
                - register <id> [<macs>] [<ips>]: Registers devices to an alias client
                - deregister [<macs>] [<ips>]: De-registers devices from their alias client
                - quit: Exit the program
            """
        print(help_text)
        while True:
            command = input("[acm-cli]> ")
            args = command.split(" ")
            if args[0] == "help":
                print(help_text)
            elif args[0] == "list":
                clients = self.acm.list_alias_clients()
                print(f"{'ID':<5}{'Name':<25}{'Comment':<30}")
                for client in clients:
                    name = (client[1][:22] + '...') if client[1] and len(client[1]) > 25 else client[1]
                    comment = (client[2][:27] + '...') if client[2] and len(client[2]) > 30 else client[2]
                    print(f"{client[0]:<5}{name:<25}{comment:<30}")
            elif args[0] == "add":
                if len(args) == 2:
                    self.acm.add_new_alias(args[1], None)
                elif len(args) == 3:
                    self.acm.add_new_alias(args[1], args[2])
                else:
                    print("Invalid usage.")
            elif args[0] == "delete":
                if len(args) == 2:
                    self.acm.delete_alias(int(args[1]))
                else:
                    print("Invalid usage.")
            elif args[0] == "update":
                if len(args) == 2:
                    print("Invalid usage: no name or comment specified.")
                elif len(args) == 3:
                    name = None
                    comment = None
                    if args[2].startswith("name="):
                        name = args[2][5:]
                    elif args[2].startswith("comment="):
                        comment = args[2][8:]
                    else:
                        print("Invalid usage.")
                    self.acm.update_alias(int(args[1]), name, comment)
                elif len(args) == 4:
                    if args[2].startswith("name=") and args[3].startswith("comment="):
                        self.acm.update_alias(int(args[1]), args[2][5:], args[3][8:])
                    elif args[2].startswith("comment=") and args[3].startswith("name="):
                        self.acm.update_alias(int(args[1]), args[3][5:], args[2][8:])
                    elif "=" not in args[2] and "=" not in args[3]:
                        self.acm.update_alias(int(args[1]), args[2], args[3])
                    else:
                        print("Invalid usage.")
                else:
                    print("Invalid usage.")
            elif command.startswith("register"):
                if len(args) != 4:
                    print("Invalid usage.")
                    continue
                id = int(args[1])
                macs = args[2].strip("[]").split(",")
                ips = args[3].strip("[]").split(",")
                self.acm.assign_device_to_alias(id, macs, ips)
            elif command.startswith("deregister"):
                if len(args) != 3:
                    print("Invalid usage.")
                    continue
                macs = args[1].strip("[]").split(",")
                ips = args[2].strip("[]").split(",")
                self.acm.remove_device_from_alias(macs, ips)
            elif command == "quit":
                self.quit()
            else:
                print("Invalid command")

if __name__ == "__main__":
    cli = AliasClientCLI()
    signal.signal(signal.SIGINT, cli.signal_handler)
    cli.cli_app()