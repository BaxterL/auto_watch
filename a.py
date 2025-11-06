from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from concurrent import futures
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
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
        if time.time() - start_time > timeout and not isvideo:
            raise TimeoutError(f"窗口0空闲超时（{timeout}秒）")
        time.sleep(1)
    with work_lock:
        iswork[i] = 1
    driver.switch_to.window(driver.window_handles[i])

def start_work(i): 
    with work_lock:
        iswork[i] = 1

def end_work(i):
    with work_lock:
        iswork[i] = 0

def handel_task(task):
    #切换并跳转
    id= task["wind"]
    switch(id)
    time.sleep(1)
    css = f'p.title[title="{id}"]'
    try:
        element = driver.find_element(By.CSS_SELECTOR, css)
        content(element,task["wind"])
    except Exception as e:
        print(e)
    finally:
        end_work(id)
    
def all_menu_unfold():
    allMenu = driver.find_elements(By.CLASS_NAME, "first-level-box")
    for menu in allMenu:
        driver.execute_script("arguments[0].click()",menu)

def content(now,id):
    driver.execute_script("arguments[0].click()", now)
    time.sleep(1)
    try:
        video_box = driver.find_element(By.CLASS_NAME, "video-box")
        right_box = driver.find_element(By.CLASS_NAME, "right-box")
    except NoSuchElementException:
        return
    
    try:
        doc = video_box.find_element(By.CLASS_NAME, "ifrema")
        time.sleep(31)
        return
    except NoSuchElementException:
        pass

    try:
        duration = ensure_video_play(video_box, timeout=20)
        # media = video_box.find_element(By.CLASS_NAME, "dplayer")
        # video_wrap = media.find_element(By.CLASS_NAME, "dplayer-video-wrap")
        # dplayer = video_wrap.find_element(By.CLASS_NAME,"dplayer-video")
        # # video_wrap.click()
        # time.sleep(1.6)
        # dplayer.click()
        # time.sleep(1)
        # dtime = media.find_element(By.CLASS_NAME, "dplayer-dtime").text
        # mins, secs = dtime.split(":")
        # duration = int(mins) * 60 + int(secs)
        time.sleep(duration + 2)  # 等待视频播放完成
        # while True:
        #     current_time = media.find_element(By.CLASS_NAME, "dplayer-ptime").text
        #     duration = media.find_element(By.CLASS_NAME, "dplayer-dtime").text
        #     if current_time == duration:  # 播放完成
        #         break
        #     time.sleep(5)
        # end_work(id)
        # return
        return
    except NoSuchElementException:
        pass

    try:
        _ = right_box.find_element(By.CLASS_NAME, "course-courseQaDiscussion-container")        
    except NoSuchElementException:
        pass

    try:
        _ = right_box.find_element(By.CLASS_NAME, "test-container")
    except NoSuchElementException:
        pass

    time.sleep(0.5)

def ensure_video_play(video_box, timeout=30):
    """
    确保视频处于播放状态，未播放则触发播放，处理加载中/暂停等场景
    :param video_box: 视频外层容器（driver.find_element(By.CLASS_NAME, "video-box")）
    :param timeout: 最大等待时间（秒）
    :return: 视频总时长（秒），便于后续等待播放完成
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            # 1. 找到视频核心元素（video标签）
            video = video_box.find_element(By.CLASS_NAME, "dplayer-video")
            
            # 2. 获取视频播放状态（通过JS获取原生video属性）
            # paused: 布尔值，true=暂停/未播放，false=正在播放
            # readyState: 0=未加载，1=加载元数据，2=可播放部分，3=大部分可播放，4=完全可播放
            video_info = driver.execute_script("""
                return {
                    paused: arguments[0].paused,
                    readyState: arguments[0].readyState,
                    duration: arguments[0].duration
                };
            """, video)
            
            # 3. 处理视频未加载完成的情况
            if video_info["readyState"] < 1:
                # print("视频正在加载中，等待1秒...")
                time.sleep(1)
                continue
            
            # 4. 未播放则触发播放（点击视频容器，避免直接操作video标签的兼容性问题）
            if video_info["paused"]:
                # video_wrap = video_box.find_element(By.CLASS_NAME, "dplayer-video-wrap")
                # driver.execute_script("arguments[0].click()", video_wrap)
                # # print("已触发视频播放")
                # time.sleep(1)  # 等待播放状态切换
                play_result = driver.execute_script("""
                return new Promise((resolve) => {
                    const video = arguments[0];
                    video.play().then(() => {
                        resolve({ success: true, paused: video.paused, duration: video.duration });
                    }).catch((err) => {
                        resolve({ success: false, error: err.message });
                    });
                });
            """, video)
                if play_result["success"] and not play_result["paused"]:
                    duration = play_result["duration"]
                    if duration > 0:
                        print(f"JS 触发播放成功，总时长：{duration:.1f}秒")
                        return duration
                else:
                    driver.execute_script("arguments[0].click()", video)
                    time.sleep(1)
                    video_info = driver.execute_script("""
                        return { paused: arguments[0].paused, duration: arguments[0].duration };
                    """, video)
                    if not video_info["paused"] and video_info["duration"] > 0:
                        print("点击 video 标签播放成功")
                        return video_info["duration"]
            
            # 5. 确认播放成功，返回总时长
            if not video_info["paused"]:
                duration = video_info["duration"]
                # 处理异常时长（如直播/未获取到时长）
                if duration <= 0:
                    raise ValueError("无法获取视频时长，可能是直播或资源异常")
                print(f"视频正在播放，总时长：{duration:.1f}秒")
                return duration
        
        # 处理元素过时（页面刷新/切换导致元素失效）
        except StaleElementReferenceException:
            # print("视频元素已更新，重新查找...")
            video_box = driver.find_element(By.CLASS_NAME, "video-box")
            time.sleep(1)
        # 处理元素未找到（可能还在加载）
        except NoSuchElementException:
            # print("视频元素未找到，等待1秒...")
            time.sleep(1)
        # 其他异常
        except Exception as e:
            # print(f"检测视频播放异常：{str(e)}")
            time.sleep(1)
    
    # 超时未成功播放
    raise TimeoutError(f"等待视频播放超时（{timeout}秒）")

def mutiple_watch():
    tasks = check_class()
    print(tasks)
    for _ in range(maxworks-1):
        driver.execute_script(f"window.open('{url}')")
        all_menu_unfold()
        time.sleep(1)

    tasks_length = len(tasks)
    with futures.ThreadPoolExecutor(min(tasks_length,maxworks)) as executor:
        res = executor.map(handel_task,tasks)
    # return list(res)

if __name__ == "__main__":
    mutiple_watch()