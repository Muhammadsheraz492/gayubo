import scrapy


class MyspiderSpider(scrapy.Spider):
    name = "myspider"
    allowed_domains = ["gayubo.com"]
    start_urls = ["https://gayubo.com/joyas/categoria-producto/anillo/pagina/1"]
    def parse(self, response):
        hrefs = response.xpath('//a[@class="product-image-link"]/@href').getall()
        for href in hrefs:
            yield scrapy.Request(url=href,callback=self.details)
        pass

    def details(self, response):
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

        yield {
            'image_src': image_src[0].strip() if image_src[0] else None,
            'image_src_2': image_src[1].strip() if image_src[1] else None,
            'product_title': product_title.strip() if product_title else None,
            'price_value': price_value.strip() if price_value else None,
            'short_description_paragraphs':short_description,
            'additional_description_paragraphs':additional_description
        }
