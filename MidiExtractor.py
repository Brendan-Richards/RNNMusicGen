from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
import os

class MidiExtractior:
    options = webdriver.ChromeOptions()
    desktop_dir = r"C:\Users\Brendan\Dropbox\Python 2019\RNN Music Generator\midi_training_files"
    laptop_dir = r"C:\Users\mark\Dropbox\Python 2019\RNN Music Generator\midi_training_files"
    preferences = {
        #"download.default_directory": laptop_dir,
        "download.default_directory": desktop_dir,
        "download.prompt_for_download": False,
        "safebrowsing.enabled": False
    }

    def get_urls(self):
        path = r'C:\Users\mark\Dropbox\Python 2019\RNN Music Generator\midiscrapy\midi_download_links'
        genres = dict()

        for doc in os.listdir(path):
            genre = doc[20:-4]
            genres[genre] = []
            with open(path + '\\' + doc, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    genres[genre].append(line.split()[-1].strip())

        return genres


    # genres should be a dict with entries {genre -> string: urls -> list}
    # downloads all the midi files from the links stored in the genres dictionary
    def download_files(self, genres):

        for genre in genres:
            self.preferences["download.default_directory"] = self.laptop_dir + '\\' + genre
            self.options.add_experimental_option("prefs", self.preferences)
            driver = webdriver.Chrome(chrome_options=self.options)

            for url in genres[genre]:
                driver.get(url)
                try:
                    driver.find_element(By.XPATH, "//a[@id='downloadmidi']").click()
                except selenium.common.exceptions.NoSuchElementException as e:
                    print('unable to locate download button for link: ' + url)



def main():
    midex = MidiExtractior()
    genres = midex.get_urls()
    midex.download_files(genres)

if __name__=='__main__':
    main()

