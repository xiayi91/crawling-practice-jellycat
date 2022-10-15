from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd


class jellycatSpider(object):
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.url = 'https://www.jellycat.com/'
        self.links = ['all-soft-toys/', 'all-animals/','all-amuseables/','all-baby-gifts/','anniversary-gifts/', 'all-books/', 'all-accessories/', 'all-personalised/']
        self.all_products = {}
        self.index = 1
        
    def get_categories(self):
        for link in self.links:
            url = self.url + 'us/' + link
            self.parse_pages(url)
            file_name = self.link[:-2]
            self.toCSV(file_name)
    
    def parse_pages(self, url):
        self.get_page(url)
        max_page = int(self.browser.find_element(By.ID, 'productDataOnPagex').get_attribute('data-nq-maxpages'))
        
        for page in range(1, max_page + 1):
            if page != 1:
                link = url + '?page=' + str(page)
                self.get_page(link)
            products = self.browser.find_elements(By.XPATH, '//*[@class="listing gproduct relative"]')
            for product in products:
                # get product link
                product_link = product.find_element(By.TAG_NAME,'a').get_attribute('href')
                # save original window info
                original_window = self.browser.current_window_handle
                # open switch and get to product link in new tab
                self.browser.switch_to.new_window('tab')
                self.browser.switch_to.window(self.browser.window_handles[1])
                self.browser.get(product_link)
                # get product info in dict
                self.get_product()
                # back to the original window
                self.browser.switch_to.window(original_window)
                
    def get_product(self):
        time.sleep(2)
        # get name, img and size info
        colors = self.browser.find_elements(By.CLASS_NAME,'swatchimg')
        for i, ele in enumerate(colors):
            try:
                ele.click()
            except:
                self.all_products[self.index] = {'model':None, 'name':None, 'img': None, 'size': None, 'price': None, 'error':'color'}
                self.index += 1
                continue
            time.sleep(0.5)
            model = self.browser.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[4]/div[1]/div[1]').text
            name = self.browser.find_element(By.XPATH, '//*[@id="ProductHeadingNotNarrow"]/h1').accessible_name
            img = self.browser.find_element(By.ID, 'mainImage').get_attribute('src')
            sizes = self.browser.find_elements(By.CLASS_NAME, 'ptb1-5')
            for i, ele in enumerate(sizes):
                try:
                    ele.click()
                except:
                    self.all_products[self.index] = {'model':None, 'name':None, 'img': None, 'size': None, 'price': None, 'error':'size'}
                    self.index += 1
                    continue
                time.sleep(0.5)
                size_xpath = '//*[@id="variant-grid-area"]/div[4]/div[2]/div[4]/div[' + str(i + 1) + ']/div'
                size = self.browser.find_element(By.XPATH, size_xpath).text
                price = self.browser.find_element(By.XPATH, '//*[@id="ProductHeadingNotNarrow"]/div[2]/div[1]/span[2]').text
                self.all_products[self.index] = {'model':model, 'name':name, 'img': img, 'size': size, 'price': price, 'error':None}
                self.index += 1
        # close the current tab
        self.browser.close()
            
    def get_page(self, url):
        self.browser.get(url)
        time.sleep(1)
      
    def toCSV(self,file_name):
        file = file_name + '.csv'
        pd.DataFrame.from_dict(data=self.all_products, orient='index').to_csv(file, header=False)
    
    def main(self):
        self.get_categories()

if __name__ == "__main__":
    spider = jellycatSpider()
    spider.main()
        
        
            

