from selenium import webdriver
# Handle Error
from selenium.common.exceptions import NoSuchElementException
# to Download the images and make directory
import os
import wget


class MangaDownloader():
    def __init__(self, manga=None):
        self.browser = webdriver.PhantomJS()
        self.manga = manga
        self.initial_chapter = 1
        self.end_chapter = float('inf')

    def handle_manga(self):
        if self.manga is None:
            self.manga = input("Masukkan manga : \n").lower()
        if self.check_manga():
            set_chapter = int(input(
                "Ketik 1 untuk download semua chapter, ketik 2 untuk pilih chapter \n"))
            if set_chapter == 2:
                self.initial_chapter = int(input("Set Chapter awal: \n"))
                self.end_chapter = int(input("Set Chapter akhir: \n"))
        else:
            print("Manga tersebut tidak ditemukan")
            self.manga = None
            self.handle_manga()

    def handle_start(self):
        self.handle_manga()
        chapter = self.initial_chapter
        while chapter <= self.end_chapter:
            navigate = self.navigate(chapter)
            if navigate:
                chapter += 1
            else:
                break

    def check_manga(self):
        try:
            self.browser.get(
                f'https://www.komikid.com/manga/{self.manga}')
            self.browser.find_element_by_class_name('exception-summary')
            return False
        except NoSuchElementException as exception:
            return True

    def make_folder(self, chapter):
        self.directory = f"Manga/{self.manga}-Chapter-{chapter}"
        try:
            os.makedirs(self.directory)
        except FileExistsError:
            pass
        return self.directory

    def set_all_page(self):
        self.browser.maximize_window()
        self.dropdown = self.browser.find_element_by_xpath(
            '/html/body/nav/div/div[3]/ul/li[2]/a')
        self.dropdown.click()
        self.all_page = self.browser.find_element_by_id('modeALL')
        self.all_page.click()

    def download_all_pages(self, image_list, directory):
        page = 0
        for image in image_list:
            page += 1
            image_src = image.get_attribute('data-src')
            filename = f"{directory}/{page}.png"
            # Download Images using Linux Command
            os.system(f"wget -O {filename} {image_src}")
            # Download Images using wget
            # wget.download(image_src, filename)

    def navigate(self, chapter):
        self.browser.get(
            f'https://www.komikid.com/manga/{self.manga}/{chapter}')
        # Set to All Page
        self.set_all_page()
        try:
            self.image_list = self.browser.find_elements_by_class_name(
                'img-responsive')
            # Make Folder
            self.directory = self.make_folder(chapter)
            self.download_all_pages(self.image_list, self.directory)
            print(
                f"Manga : {self.manga}, Chapter : {chapter} Berhasil didownload.")
            return True
        except NoSuchElementException:
            print("Chapter tidak ditemukan")
            return False


manga = MangaDownloader()
manga.handle_start()
