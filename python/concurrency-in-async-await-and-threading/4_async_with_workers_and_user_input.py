import asyncio

import time

task_queue = asyncio.Queue()

order_num = 0

async def take_order():
   global order_num
   order_num += 1
   
   print(f"Order burger and fries for order #{order_num:04d}:")
   
   burger_num = await asyncio.to_thread(input, "Number of burgers:")
   for i in range(int(burger_num)):
       await task_queue.put(make_burger(f"{order_num:04d}-burger{i:02d}"))
   
   fries_num = await asyncio.to_thread(input, "Number of fries:")
   for i in range(int(fries_num)):
       await task_queue.put(make_fries(f"{order_num:04d}-fries{i:02d}"))
   
   print(f"Order #{order_num:04d} queued.")
   
   await task_queue.put(take_order())

async def make_burger(order_num):

   print(f"Preparing burger #{order_num}...")

   await asyncio.sleep(5)  # time for making the burger

   print(f"Burger made #{order_num}")

async def make_fries(order_num):

   print(f"Preparing fries #{order_num}...")

   await asyncio.sleep(2)  # time for making fries

   print(f"Fries made #{order_num}")

class Staff:

   def __init__(self, name):

       self.name = name

   async def working(self):

       while True:

           if task_queue.qsize() > 0:

               print(f"{self.name} is working...")

               task = await task_queue.get()

               await task

               print(f"{self.name} finish task...")

           else:

               await asyncio.sleep(1) #rest

async def main():

   task_queue.put_nowait(take_order())

   staff1 = Staff(name="John")

   staff2 = Staff(name="Jane")

   await asyncio.gather(staff1.working(), staff2.working())

if __name__ == "__main__":

   s = time.perf_counter()

   asyncio.run(main())

   elapsed = time.perf_counter() - s

   print(f"Orders completed in {elapsed:0.2f} seconds.")