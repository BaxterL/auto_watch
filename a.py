from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from concurrent import futures
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import threading


path = r'D:\Tool\chromedriver-win64\chromedriver.exe'
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

username="账号"
password="密码"
maxworks = 6 #is6 0,1,2,3,4,5
wdf = r"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAfhJREFUSEu9lj1oE2EYx//PqaDYDJHaQlCoH7k4dVYuUMFFERSHQIeCUcxiih/QpXS4u9Gp9MNJwSWC4CAKKgiClgSLg4hkMIkBISFrhwhKPu4p7zWXz7vLXWjMmPd5/r/3+XyP4PKbVS+e+Cc1rsPgqyCcARBqmVfAKEKit4eNg69/6J/KTjJkdxBRlRATdGbcAviA2yUAahLhGTHUnJ6p9NsOACKqco2BFIMD7sK9pwSqErCQ0zNvuk96AGEteg8wVsGQ/Ii3bQkGID0saOl16782QNzcIH41snhH0ZCYbliRmAAz58BPv2lxLqyZrnOiJiZA1pQnzHxnpLQ4OBHR07yWSZBoxb+o/x7eLX7x1DyCQzMk69EkG8amX3cv9iRJiySryjsGX/Hi0G8zHZhEeOo00sWvtu4Eek+ypuSYWfYLOHv8FFLxDRw7GsSltRhKOwMzBiLKC0CVmSf8ALrFPxe+IPF8yT4Coj+ugNsX5vGtlMX3crYt0C9+98Uy6s26K8A2RSeDIXy8/xK1Rg1CZOvXNvyIC+JeilyKvHL5AW6ej5mQRx8eIzkXN3Mu0uJ2885QiyIPaVMLYjl5FTcjEG3qZdAsiB9xscbNQfO6KkRN7FrRcR9Zq+K/LLsWZHzr2gpzrA+OBRnrk9kFGd+j390V+/HZsgvSIhcecicecAAAAABJRU5ErkJggg=="
url = "https://www.cqooc.com/course/detail/courseStudy?id=fd546ac8812b568f"

def login(fdelay=1):
    time.sleep(fdelay)
    username_input = driver.find_element(By.CSS_SELECTOR, ".username-box .ant-input")
    username_input.clear()    
    username_input.send_keys(username)

    password_input = driver.find_element(By.CSS_SELECTOR,".password-box .ant-input")
    password_input.clear()
    password_input.send_keys(password)

    login_btn = driver.find_element(By.CLASS_NAME, "submit-btn")
    driver.execute_script("arguments[0].click()", login_btn)
    time.sleep(0.6)
    
def is_completed(box):
    try:
        strr = box.find_element(By.CLASS_NAME, "file-complete").get_attribute("src")
        if strr == wdf:
            return True
        else:
            return False
    except:
        return False

def check_class():
    driver.maximize_window()
    driver.get(url)
    login()

    try:
        fuckad = driver.find_element(By.CLASS_NAME,"ant-modal-close-icon")
        if fuckad: driver.execute_script("arguments[0].click()", fuckad)
    except:
        pass

    driver.refresh()

    time.sleep(1)
    allMenu = driver.find_elements(By.CLASS_NAME, "first-level-box")
    for menu in allMenu:
        driver.execute_script("arguments[0].click()",menu)
        time.sleep(0.3)

    time.sleep(0.6)
    boxes = driver.find_elements(By.CLASS_NAME, "third-level-inner-box")
    unfinished_titles = []
    for i,box in enumerate(boxes):
        title = box.find_element(By.CLASS_NAME, "title")
        if (is_completed(box)):
            pass
        else:
            unfinished_titles.append({
                "title": title.get_attribute("title"),
                "wind": i % maxworks
            })
    time.sleep(2)
    return unfinished_titles

iswork = [0 for _ in range(maxworks)]
work_lock = threading.Lock()

def switch(i,timeout=1200,isvideo=False):
    start_time = time.time()
    while True:
        with work_lock:
            if iswork[0] == 0:
                break
        if time.time() - start_time > timeout:
            if isvideo:
                pass
            else:
                raise TimeoutError(f"窗口0空闲超时（{timeout}秒）")
        time.sleep(1)
    driver.switch_to.window(driver.window_handles[i])

def start_work(i): 
    with work_lock:
        iswork[i] = 1

def end_work(i):
    with work_lock:
        iswork[i] = 0

def handel_task(task):
    #切换并跳转
    switch(task["wind"])
    css = f'p.title[title="{task["title"]}"]'
    try:
        element = driver.find_element(By.CSS_SELECTOR, css)
        content(element,task["wind"])
    except Exception as e:
        print(e)

def content(now,id):
    driver.execute_script("arguments[0].click()", now)
    time.sleep(0.3)
    try:
        video_box = driver.find_element(By.CLASS_NAME, "video-box")
        right_box = driver.find_element(By.CLASS_NAME, "right-box")
    except NoSuchElementException:
        return
    
    try:
        doc = video_box.find_element(By.CLASS_NAME, "ifrema")
        start_work(id)
        time.sleep(31)
        end_work(id)
        return
    except NoSuchElementException:
        pass
    finally:
        end_work(id)

    try:
        media = video_box.find_element(By.CLASS_NAME, "dplayer")
        video_wrap = media.find_element(By.CLASS_NAME, "dplayer-video-wrap")
        # video_wrap.click()
        driver.execute_script("arguments[0].click()", video_wrap.find_element(By.CLASS_NAME,"dplayer-video"))

        dtime = media.find_element(By.CLASS_NAME, "dplayer-dtime").text
        mins, secs = dtime.split(":")
        duration = int(mins) * 60 + int(secs)
        start_work(id)
        time.sleep(duration + 2)  # 等待视频播放完成
        # while True:
        #     current_time = media.find_element(By.CLASS_NAME, "dplayer-ptime").text
        #     duration = media.find_element(By.CLASS_NAME, "dplayer-dtime").text
        #     if current_time == duration:  # 播放完成
        #         break
        #     time.sleep(5)
        # end_work(id)
        # return
        end_work(id)
        return
    except NoSuchElementException:
        pass
    finally:
        end_work(id)

    try:
        _ = right_box.find_element(By.CLASS_NAME, "course-courseQaDiscussion-container")        
    except NoSuchElementException:
        pass

    try:
        _ = right_box.find_element(By.CLASS_NAME, "test-container")
    except NoSuchElementException:
        pass

    time.sleep(0.5)


def mutiple_watch():
    tasks = check_class()
    for _ in range(maxworks-1):
        driver.execute_script(f"window.open('{url}')")

    tasks_length = len(tasks)
    with futures.ThreadPoolExecutor(min(tasks_length,maxworks)) as executor:
        res = executor.map(handel_task,tasks)
    # return list(res)

if __name__ == "__main__":
    mutiple_watch()