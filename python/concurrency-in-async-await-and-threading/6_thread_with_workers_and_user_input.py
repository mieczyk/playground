def working():

   while True:

       with queue_lock:

           if len(order_queue) == 0:

               return

           else:

               task = order_queue.pop(0)

       print(f"{threading.current_thread().name} is working...")

       task()

       print(f"{threading.current_thread().name} finish task...")

```

Based on what we have learned so far, we can complete our final code with threading like this:

```

import logging

import threading

import time

logger = logging.getLogger(__name__)

logging.basicConfig(filename="pyburger_threads.log", level=logging.INFO)

queue_lock = threading.Lock()

task_queue = []

order_num = 0

closing = False

def take_order():

   global order_num, closing

   try:

       order_num += 1

       logger.info(f"Taking Order #{order_num:04d}...")

       print(f"Order burger and fries for order #{order_num:04d}:")

       burger_num = input("Number of burgers:")

       for i in range(int(burger_num)):

           with queue_lock:

               task_queue.append(make_burger(f"{order_num:04d}-burger{i:02d}"))

       fries_num = input("Number of fries:")

       for i in range(int(fries_num)):

           with queue_lock:

               task_queue.append(make_fries(f"{order_num:04d}-fries{i:02d}"))

       logger.info(f"Order #{order_num:04d} queued.")

       print(f"Order #{order_num:04d} queued, please wait.")

       with queue_lock:

           task_queue.append(take_order)

   except ValueError:

       print("Goodbye!")

       logger.info("Closing down... stop taking orders and finish all tasks.")

       closing = True

def make_burger(order_num):

   def making_burger():

       logger.info(f"Preparing burger #{order_num}...")

       time.sleep(5)  # time for making the burger

       logger.info(f"Burger made #{order_num}")

   return making_burger

def make_fries(order_num):

   def making_fries():

       logger.info(f"Preparing fried #{order_num}...")

       time.sleep(2)  # time for making fries

       logger.info(f"Fries made #{order_num}")

   return making_fries

def working():

   while True:

       with queue_lock:

           if len(task_queue) == 0:

               if closing:

                   return

               else:

                   task = None

           else:

               task = task_queue.pop(0)

       if task:

           logger.info(f"{threading.current_thread().name} is working...")

           task()

           logger.info(f"{threading.current_thread().name} finish task...")

       else:

           time.sleep(1)  # rest

def main():

   print("Welcome to Pyburger!")

   logger.info("Ready for business!")

   task_queue.append(take_order)

   staff1 = threading.Thread(target=working, name="John")

   staff1.start()

   staff2 = threading.Thread(target=working, name="Jane")

   staff2.start()

   staff1.join()

   staff2.join()

   logger.info("All tasks finished. Closing now.")

if __name__ == "__main__":

   s = time.perf_counter()

   main()

   elapsed = time.perf_counter() - s

   logger.info(f"Orders completed in {elapsed:0.2f} seconds.")