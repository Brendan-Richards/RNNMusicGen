import scrapy
import re

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
             'https://freemidi.org/genre-pop',
             #'https://freemidi.org/genre-rock',
             #'https://freemidi.org/genre-hip-hop-rap',
             #'https://freemidi.org/genre-jazz'
             #'https://freemidi.org/genre-blues'
             #'https://freemidi.org/genre-rnb-soul',
             #'https://freemidi.org/genre-bluegrass'
             #'https://freemidi.org/genre-country',
             #'https://freemidi.org/genre-christian-gospel',
             #'https://freemidi.org/genre-opera',
             #'https://freemidi.org/genre-folk',
             #'https://freemidi.org/genre-punk',
             #'https://freemidi.org/genre-disco'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_genre, meta={'genre': url[27:]})

    def parse_genre(self, response):
        genre = response.meta.get('genre')
        for div in response.css("div.genre-link-text"):
            artist_name = div.css('a::text').extract()[0]
            artist_link = 'https://freemidi.org/' + div.css('a').attrib['href']
            url = response.urljoin(artist_link)
            yield scrapy.Request(url, callback=self.parse_artist_page, meta={'artist': artist_name, 'genre': genre})

    def parse_artist_page(self, response):
        artist_name = response.meta.get('artist')
        genre = response.meta.get('genre')
        for song_cell in response.css("div.artist-song-cell"):
            song_link = 'https://freemidi.org/' + song_cell.css('a').attrib['href']
            url = response.urljoin(song_link)
            yield scrapy.Request(url, callback=self.parse_song_page, meta={'artist': artist_name, 'genre': genre})

    def parse_song_page(self, response):
        artist_name = response.meta.get('artist')
        genre = response.meta.get('genre')
        lines = response.xpath('//a[@id="downloadmidi"]')
        with open('midi_download_links_' + genre + '.txt', 'a+') as f:
            for line in lines:
                name = line.attrib['title']
                link = line.attrib['href']
                #print(name, link)
                f.write(artist_name + ', ' + name + ', https://freemidi.org/' + link + '\n')

