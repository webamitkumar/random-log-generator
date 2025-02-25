import random 
import string 
import time
import logging

# setting up logging for error handling

logging.basicConfig(filename='log_Generator_errors.log', level=logging.ERROR)

#list of level of logs
log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR',]

#list of possible actions
ACTIONS = ['login', 'logout', 'view', 'edit', 'delete']


#fuctions to generate random string for logs
def generate_random_string(length=10):
    try:
        return ''.join(random.choices(string.ascii_letters + string.digits , k=length))
    except Exception as e:
        logging.error(f"error in generate_random_string function: " + str(e))
        return "error"
    
# function to generate a random log entry 
def generate_random_log_entry():
    try:
        log_level = random.choice(log_levels)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        action = random.choice(ACTIONS)
        user = generate_random_string(8)
        log_entry = f"{timestamp} - {log_level} - {action} - {user}"
        return log_entry
    except Exception as e:
        logging.error(f"error in generate_random_log_entry function: " + str(e))
        return "error"
    
# function to write logs to a file
def write_log_to_file(log_filename, num_entries=100):
    try:
        with open(log_filename, 'w') as file:
            for _ in range(num_entries):
                log_entry = generate_random_log_entry()
                if log_entry != "error":
                    file.write(log_entry + '\n')
        print(f"Logs have been successfull written {log_filename}")
    except Exception as e:
        logging .error(f"error in write_log_to_file function: " + str(e))
        print("an error occupied while writting logs to  the file.")

#generate  and write 200 random entries to a file
write_log_to_file('generated_logs.txt', num_entries=200)


