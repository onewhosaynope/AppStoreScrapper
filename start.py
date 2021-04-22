from main import send_results, clean_json, scrap_and_save
import schedule
import time
from helpers import bcolors

print("\n" + bcolors.OKGREEN  + "STARTED" + bcolors.ENDC + "\n")
schedule.every().day.at("11:00").do(send_results)
schedule.every(2).hours.do(scrap_and_save) 
schedule.every().day.at("11:10").do(clean_json)

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute
