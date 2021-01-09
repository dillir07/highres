"""
highres
-------

Welcome to highres, by Dilli Babu R < dillir07@outlook.com >

'highres' is a simple script, which can download a higher resolution image for images in a given folder.
This is done by uploading the image to google images with 'search by image' by image.
If there is a match is found, script can download higher resolution image, if match is not found,
script will simply ignore and will move on next folder.

"""

import os
from pathlib import Path
import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import urllib.request


def wait_for_element(driver, byType, byValue, maxWait: int):
    """
    This method, takes properties of an element and looks for the element in page.
    if the element is found, it will return the element else None is returned

    :Args:
    ------
    - driver ([webdriver]): [Selenium webdriver]
    - byType ([By Type]): [Which property we are using to get element. ex: By.XPATH or BY.Id]
    - byValue ([type]): [value of property]
    - maxWait (int): [wait for element to be found]

    Returns:
        [webdriverelement]: [identified element]
    """
    try:
        element = WebDriverWait(driver, maxWait).until(
            EC.presence_of_element_located((byType, byValue)))
        return element
    except TimeoutException:
        print("Element not found")
        return None


def highres(dr, url, images_folder_path, highres_folder_name, success_folder_name, error_folder_name, image_extensions: list, wait_time: int):
    """
    loops over images files in give folder and downloads hi-res images if available,
    if found hi-res images is saved in success folder,
    input image is saved in old folder
    if hi-res not found, input image is saved in error folder

    Args:
    -----
    - dr ([webdriver]): [Selenium Webdriver]
    - url ([str]): URL for google images webpage
    - images_folder_path ([Path]): [where to look for images]
    - highres_folder_name ([Path]): [where to store downloaded hi-res images if found]
    - success_folder_name ([Path]): [on sucess where to move old low-res image file]
    - error_folder_name ([Path]): [on error where to store old low-res image file]
    - image_extensions (list): [list of image file extensions to look for like [".jpg", ".jpeg"]]
    - wait_time (int): [max wait time to wait for an element to be available]

    Raises:
    ------
        SystemExit: [If folder not found, or some error while navigating in browser]
    """

    files = os.listdir(images_folder_path)

    files = [file for file in files if Path(
        file).suffix.lower() in image_extensions]

    if len(files) == 0:
        dr.quit()
        raise SystemExit("No images found in the input folder")

    for file in files:
        dr.get(url)
        print("working on file:", file)
        file_name = Path(file)
        image_icon = wait_for_element(dr,
                                      By.XPATH, "/html/body/div[2]/div[2]/div[2]/form/div[2]/div[1]/div[1]/div/div[3]/div[2]", 10)
        image_icon.click()

        upload_image_link = wait_for_element(dr,
                                             By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[2]/form/div[1]/div/a", 10)
        upload_image_link.click()

        browse_image_button = wait_for_element(dr,
                                               By.XPATH, '//*[@id="awyMjb"]', 10)
        browse_image_button.send_keys(str(images_folder_path) + "/" + file)
        try:

            all_sizes_button = wait_for_element(dr,
                                                By.XPATH, '/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/span[1]/a', 10)
            all_sizes_button.click()

            first_image = wait_for_element(dr,
                                           By.XPATH, '/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div[1]/a[1]/div[1]/img', 10)
            first_image.click()

            time.sleep(wait_time)

            preview_image_link = wait_for_element(dr,
                                                  By.XPATH, '/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img', 10)
            src = preview_image_link.get_attribute('src')

            if not os.path.exists(images_folder_path / highres_folder_name):
                os.mkdir(images_folder_path / highres_folder_name)
            if not os.path.exists(images_folder_path / success_folder_name):
                os.mkdir(images_folder_path / success_folder_name)
            if not os.path.exists(images_folder_path / error_folder_name):
                os.mkdir(images_folder_path / error_folder_name)

            urllib.request.urlretrieve(
                src, images_folder_path / highres_folder_name / file_name)
            os.renames(images_folder_path / file_name,
                       images_folder_path / success_folder_name / file_name)
            print("success for file:", file)
        except:
            print("failure for file:", file)
            os.renames(images_folder_path / file_name,
                       images_folder_path / error_folder_name / file_name)

    dr.quit()
    print("completed")


def highres_handler() -> None:
    """
    This method bootstraps the arg_parse module and verifies the inputs given by the user via CLI.
    Then calls process_input() method.
    :return: None
    """

    arg_parser = argparse.ArgumentParser(
        description=""" Welcome to highres, by Dilli Babu R < dillir07@outlook.com >
        'highres' is a simple script, which can download a higher resolution image for images in a given folder.
        This is done by uploading the image to google images with 'search by image' by image.
        If there is a match is found, script can download higher resolution image, if match is not found,
        script will simply ignore and will move on next folder.
        """,
        epilog='If you require any help, please reach out to me at dillir07@outlook.com')

    arg_parser.add_argument('images_folder_path', metavar=r'"C:\..\pictures\input"',
                            type=str, help='folder path in which image files are present')
    args = arg_parser.parse_args()

    images_folder_path = Path(str(args.images_folder_path).replace("\\", "/"))

    # these are for config
    highres_folder_name = Path(r'highres')
    success_folder_name = Path(r'old')
    error_folder_name = Path(r'error')
    image_extensions = [".jpeg", ".jpg", ".png", ".bmp"]
    wait_time = 5
    if not os.path.exists(images_folder_path):
        raise SystemExit("{} is a invalid folder".format(
            args.images_folder_path))

    browser = None
    google_images_url = "https://google.com/images"

    if browser is None:
        try:
            browser = webdriver.Chrome()
            browser.get(google_images_url)
        except (Exception) as err:
            print(err)
    if browser is None:
        try:
            browser = webdriver.Firefox()
            browser.get(google_images_url)
        except (Exception) as err:
            print(err)
    if browser is None:
        try:
            browser = webdriver.Safari()
            browser.get(google_images_url)
        except (Exception) as err:
            print(err)
    if browser is None:
        try:
            browser = webdriver.Edge()
            browser.get(google_images_url)
        except (Exception) as err:
            print(err)
    if browser is None:
        raise SystemExit(
            "Browser is not available or Webdriver is not set up properly")

    highres(browser, google_images_url, images_folder_path, highres_folder_name,
            success_folder_name, error_folder_name, image_extensions, wait_time)
