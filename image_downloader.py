from icrawler.builtin import BingImageCrawler, BaiduImageCrawler

def download_images(search_term, num_images, download_path, source='bing'):
    if source == 'bing':
        crawler = BingImageCrawler(storage={'root_dir': download_path})
    elif source == 'baidu':
        crawler = BaiduImageCrawler(storage={'root_dir': download_path})
    else:
        raise ValueError("Fuente no válida. Usa 'bing' o 'baidu'.")

    # Realiza la búsqueda y descarga las imágenes
    crawler.crawl(keyword=search_term, max_num=num_images, file_idx_offset=0)


download_images("fat male front body mirror selfie", 50, "./fat_images", source='bing')
# download_images("fat male front body mirror selfie", 50, "./fat_images_2", source='baidu')

