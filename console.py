#!/usr/bin/python3

import ast
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
import cmd 

def list_from_args(arg):

    braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)

    if braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            new_list = split(arg[:brackets.span()[0]])
            final_list = [i.strip(",") for i in new_list]
            final_list.append(brackets.group())
            return final_list
    else:
        new_list = split(arg[:braces.span()[0]])
        final_list = [i.strip(",") for i in new_list]
        final_list.append(braces.group())
        return final_list

class HBNBCommand(cmd.Cmd):

    prompt = '(hbnb) '

    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def do_quit(self, arg):
        """Exit the program."""
        return True

    def do_EOF(self, arg):
        """Exit the program."""
        print()  
        return True

    def emptyline(self):
        """Do nothing on an empty line."""
        pass

    def help_quit(self):
        """Exit the program."""
        print("Quit command to exit the program.")

    def help_EOF(self):
        """Exit the program."""
        print("Exit the command interpreter. Equivalent to typing 'quit'.")

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        args_list = list_from_args(arg)
        if len(args_list) == 0:
            print("** class name missing **")
        elif args_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(args_list[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        args_list = list_from_args(arg)
        dict = storage.all()

        if len(args_list) == 0:
            print("** class name missing **")
        elif args_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(args_list[0], args_list[1]) not in dict:
            print("** no instance found **")
        else:
            print(dict["{}.{}".format(args_list[0], args_list[1])]) 

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""

        args_list = list_from_args(arg)
        dict = storage.all()

        if len(args_list) == 0:
            print("** class name missing **")
        elif args_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(args_list[0], args_list[1]) not in dict.keys():
            print("** no instance found **")
        else:
            del dict["{}.{}".format(args_list[0], args_list[1])]
            storage.save()
    
    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        
        args_list = list_from_args(arg)

        if len(args_list) > 0 and args_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            class_to_string = []
            for obj in storage.all().values():
                if len(args_list) > 0 and args_list[0] == obj.__class__.__name__:
                    class_to_string.append(obj.__str__())
                elif len(args_list) == 0:
                    class_to_string.append(obj.__str__())
            print(class_to_string)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value>
        or
        <class>.update(<id>, <attribute_name>, <attribute_value>)
        or
        <class>.update(<id>, <dictionary>)

        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary.
        """

        args_list = list_from_args(arg)
        obj_dict = storage.all()

        if len(args_list) == 0:
            print("** class name missing **")
            return False
        if args_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(args_list) == 1:
            print("** instance id missing **")
            return False
        instance_key = "{}.{}".format(args_list[0], args_list[1])
        if instance_key not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(args_list) == 2:
            print("** attribute name missing **")
            return False
        if len(args_list) < 4:
            print("** value missing **")
            return False

        obj = obj_dict[instance_key]
        try:
            value_type = type(ast.literal_eval(args_list[3]))
            if value_type != dict:
                print("** value is not a dictionary **")
                return False
        except (SyntaxError, ValueError):
            print("** value missing or not a valid dictionary **")
            return False

        if len(args_list) == 4:
            if hasattr(obj, args_list[2]):
                valtype = type(getattr(obj, args_list[2]))
                setattr(obj, args_list[2], valtype(args_list[3]))
            else:
                setattr(obj, args_list[2], args_list[3])
        elif value_type == dict:
            for k, v in ast.literal_eval(args_list[3]).items():
                if hasattr(obj, k):
                    valtype = type(getattr(obj, k))
                    setattr(obj, k, valtype(v))
                else:
                    setattr(obj, k, v)

        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
