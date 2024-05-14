import scrapy


class MyspiderSpider(scrapy.Spider):
    name = "myspider"
    allowed_domains = ["gayubo.com"]
    start_urls = ["https://gayubo.com/joyas/anillo-tutti-frutti-capsule-collection-3/"]
    def start_requests(self):
        for itm in range(1,10):
            url=f"https://gayubo.com/joyas/categoria-producto/anillo/pagina/{itm}"
            yield  scrapy.Request(url=url)

    def parse(self, response):
        hrefs = response.xpath('//a[@class="product-image-link"]/@href').getall()
        for href in hrefs:
            yield scrapy.Request(url=href,callback=self.details)

    def details(self, response):
        url=response.url
        main_image=response.xpath('//figure[@class="woocommerce-product-gallery__image"]/a/img/@src').get()

        product_title = response.xpath('//h1[@class="product_title entry-title wd-entities-title"]/text()').get()
        short_description_paragraphs = response.xpath(
            '//div[@class="woocommerce-product-details__short-description"]/p/text()').getall()
        additional_description_paragraphs = response.xpath(
            '//div[@class="wc-tab-inner wd-scroll-content"]/p/text()').getall()
        image_src = response.xpath('//div[@class="wd-carousel-item "]/img/@src').getall()
        short_description = " ".join(
            p.strip() for p in short_description_paragraphs) if short_description_paragraphs and any(
            short_description_paragraphs) else None
        additional_description = " ".join(
            p.strip() for p in additional_description_paragraphs) if additional_description_paragraphs and any(
            additional_description_paragraphs) else None
        price_value = response.xpath(
            '//p[@class="price"]/span[@class="woocommerce-Price-amount amount"]/bdi/text()').get()
        # image_data={image_src}
        data={}
        for i, image_src in enumerate(image_src, start=1):
            data[f'image_{i}_src']= image_src.strip() if image_src else None
        data['main_image']=main_image if main_image else None
        data['product_title']= product_title.strip() if product_title else None
        data['price_value']=price_value.strip() if price_value else None
        data['short_description_paragraphs']=short_description
        data['additional_description_paragraphs']=additional_description
        data['url']=url
        # yield {
        #     'image_src': image_src[0].strip() if image_src[0] else None,
        #     'image_src_2': image_src[1].strip() if image_src[1] else None,
        #     'product_title':
        #     '':
        #     'short_description_paragraphs':short_description,
        #     'additional_description_paragraphs':
        # }
        yield data
