import random
import requests
from concurrent.futures import ThreadPoolExecutor as ThreadPool
import logging
import time
from config import HOST
import pdb


PROMPT_SAMPLE = ["Illustrate a scene inside the labyrinth of the Moon Palace, where the 'Magical Pig Snout' is sniffing out the direction towards Chang'e. The labyrinth should look vast and complex, with Pigsy appearing both determined and hopeful."]


def error_handle(func, e):
    logging.error("error in " + func + ": " + str(e))


def mj_fetch_task(task_id):
    try:
        time_cnt = 1
        limit = 20
        while time_cnt <= limit:
            res = requests.get(HOST + "/mj/task/{}/fetch".format(task_id))
            if res.status_code == 200:
                res = res.json()
                logging.info(res)
                if res["status"] == "SUCCESS":
                    print(res)
                    logging.info("SUCCESS")
                    return res["imageUrl"]
                else:
                    logging.info(
                        "task_id {} action {} Waiting for result, cnt {}...".format(task_id, res["action"], time_cnt))
                    time.sleep(5)
                    time_cnt += 1
            else:
                limit = 3
                logging.info("task_id {} retrying, cnt {}...".format(
                    task_id, time_cnt))
                time.sleep(1)
                time_cnt += 1
                return None
        return None
    except Exception as e:
        error_handle(__name__, e)
        return None


def mj_imagine(prompt):
    try:
        res = requests.post(HOST + "/mj/submit/imagine",
                            json={"prompt": prompt})
        task_id = res.json()["result"]
        if not mj_fetch_task(task_id):
            logging.info("imagine task_id {} failed".format(task_id))
            return None
        return task_id
    except Exception as e:
        error_handle(__name__, e)
        return None



def mj_upscale(task_id):
    try:
        print(456)
        res = requests.post(HOST + "/mj/submit/change",
                            json={"action": "UPSCALE", "taskId": task_id, "index": 1})
        task_id = res.json()["result"]
        if not mj_fetch_task(task_id):
            logging.info("upscale task_id {} failed".format(task_id))
            return None
        return mj_fetch_task(task_id)

    except Exception as e:
        error_handle(__name__, e)
        return None


def imagine(prompt):
    try:
        task_id = mj_imagine(prompt)
        logging.info("mj_imagine success with prompt {}..., prepare to upscale".format(prompt[:10]))
        if task_id:
            image = mj_upscale(task_id)
            if image:
                logging.info(image)
        return None
    except Exception as e:
        error_handle(__name__, e)
        return None


def main():
    logging.basicConfig(filename='imagine.log', level=logging.INFO)
    with ThreadPool(max_workers=10) as pool:
        for prompt in PROMPT_SAMPLE:
            pool.submit(imagine, prompt)
            time.sleep(random.randint(1, 5))
        pool.shutdown(wait=True)


if __name__ == "__main__":
    main()
