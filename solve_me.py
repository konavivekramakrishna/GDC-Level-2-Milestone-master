class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "r") as f:
            self.completed_items = [line.strip() for line in f.readlines()]

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "help":
            self.help()

    def help(self):
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics"""
        )

    def add(self, args):
        if len(args) < 2:
            print("please provide suffient arguments")
            return

        priority = int(args[0])

        desc = args[1]

        if priority > 0:
            print(f'Added task: "{desc}" with priority {priority}')
            self.recursiveAdd(int(priority), desc)

        else:
            print("enter non negative number")

    def recursiveAdd(self, p, d):
        if p in self.current_items:
            self.recursiveAdd(int(p + 1), self.current_items[p])

        self.current_items[int(p)] = d

        self.write_current()

        # self.ls()

    def done(self, args):
        priorityToMarkAsComplete = int(args[0])

        if priorityToMarkAsComplete in self.current_items:
            self.completed_items.append(
                self.current_items[priorityToMarkAsComplete].strip()
            )

            del self.current_items[priorityToMarkAsComplete]

            self.write_completed()

            self.write_current()
            print("Marked item as done.")

        else:
            print(
                f"Error: no incomplete item with priority {priorityToMarkAsComplete} exists."
            )

    def delete(self, args):
        try:
            priorityToDelete = int(args[0])

            del self.current_items[priorityToDelete]
            self.write_current()
            print(f"Deleted item with priority {priorityToDelete}")

        except KeyError:
            print(
                f"Error: item with priority {priorityToDelete} does not exist. Nothing deleted."
            )

    def ls(self):
        index = 1

        for key, val in self.current_items.items():
            print(f"{index}. {val.strip()} [{key}]")
            index += 1

    def report(self):
        len_Pending = len(self.current_items)

        print(f"Pending : {len_Pending}")

        if len_Pending > 0:
            index = 1

            for key, val in self.current_items.items():
                print(f"{index}. {val.strip()} [{key}]")
                index += 1
        print("")

        print(f"Completed : {len(self.completed_items)}")

        index = 1
        for i in self.completed_items:
            print(f"{index}. {i}")
            index += 1
