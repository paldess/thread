import asyncio
import time
import random
import pandas as pd
import threading


extra = []
start_time = time.time()

async def printt(n):
    x = int(100000*n)
    for i in range(x):
        # await asyncio.sleep(n)
        extra.append(n)
        # print(x)


async def printt1(extra):
    time.sleep(0.3)
    print(len(extra))








loop = asyncio.get_event_loop()
# potoky = [potok.create_task(printt(1)),
#           potok.create_task(printt1(2))]

potoky = [printt1(extra)]
for i in range(100000):
    x = random.randint(1, 10000)/100000
    potoky.append(loop.create_task(printt(x)))


loop.run_until_complete(asyncio.wait(potoky))
loop.close()
a = pd.DataFrame(extra, columns=['n'])
ss = time.time()-start_time
print(('%s seconds'%ss))
print(len(extra))


