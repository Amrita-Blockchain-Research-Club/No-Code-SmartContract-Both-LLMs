import openai
import re
import os
from termcolor import colored
from prettytable import PrettyTable
from key import OpenAi_Key as GptKey
openai.api_key = GptKey


Model = 'gpt-3.5-turbo'

def search(prompt):

    response=openai.ChatCompletion.create(
        model=Model,
        messages=[{"role":"user",
                "content":prompt}
                ],
        max_tokens=2048,                                                                                                                                                           
    )

    Message = response.choices[0].message.content
#     Message = """pragma solidity ^0.4.24;

# contract Addition {
#   function add(uint a, uint b) public pure returns (uint) {
#     return a + b;
#   }
# }
# For debugging purpose"""

    history[prompt] = Message
    # print(Message)

    return Message



def advanced_search(prompt):

    response = openai.ChatCompletion.create(
            model=Model,
            messages=[{"role":"assistant", "content":history[list(history)[-1]]},
                    {"role":"user",
                        "content":prompt}
                        ],
            max_tokens=2048,
        )

    Message = response.choices[0].message.content
#     Message = """pragma solidity ^0.4.24;

# contract Advanced_Addition {
#   function add(uint a, uint b) public pure returns (uint) {
#     return a + b;
#   }
# }
# For debugging purpose""" 
    history[prompt] = Message
    # print(Message)

    return Message




def user_satisfaction(message):
    user_choice = input(colored("Satisfy with Output? (y/n) >>> ", 'yellow', attrs=['bold']))
    if user_choice == "y":
        return
    elif user_choice == "n":
        user_prompt = input(colored("Enter Improvisations in Output? >>> ", 'light_magenta', attrs=['bold']))
        return advanced_search(user_prompt)
    else:
        print(colored("Invalid Input, breaking to main...", 'red', attrs=['bold']))
        return 




def History():
    for key, value in history.items():
        table.add_row([key, value], divider=True)
    print(table)
    return

def create_SOLFile():
    pattern = r"(?s)pragma solidity.*\}"
    matches = re.findall(pattern, history[list(history)[-1]])
    solidity_code = ''.join(matches)

    filepath = './Contracts'
    file_base_name = 'SOLFile'
    file_extension = '.sol'

    i = 1
    filename = os.path.join(filepath, file_base_name + file_extension)

    while os.path.exists(filename):
        filename = os.path.join(filepath, f'{file_base_name}_{i}{file_extension}')
        i += 1

    try:
        with open(filename, 'w') as f:
            f.write(solidity_code)
            f.close()
    except IOError:
        print(colored(f"Error: Could not write to file '{filename}'", 'red', attrs=['bold']))
        return None

    print(colored("SOL File Created", 'green', attrs=['bold']))

    with open('FileHistory.txt', 'a') as f:
        f.write(filename)
        f.write("\n")
        f.close()

    return filename


history = {}
if __name__ == '__main__':
    prompt = input(colored("Enter Prompt you want to search for? >>> ", 'light_magenta', attrs=['bold']))
    table = PrettyTable(["Prompt", "Output"])
    table.align = "l"
    table.max_width = 120
    history = {}
    search(prompt)


    print(colored("\n<-----Searching Done----->\n", 'red', attrs=['bold']))


    history_check = input(colored("Do you want to see history? (y/n) >>> ", 'yellow', attrs=['bold']))
    if history_check == "y":
        History()
    else:
        print(colored("History still be stored in dictonary...", 'red', attrs=['bold']))


    deploy = input(colored("Do you want to deploy this code in a SOL file? (y/n) >>> ", 'yellow', attrs=['bold']))
    if deploy == "y":
        FileName = create_SOLFile()
    else:
        print(colored("Solidity File not created...", 'red', attrs=['bold']))

    print(colored("Thankyou for using our service", 'red', attrs=['bold']))


