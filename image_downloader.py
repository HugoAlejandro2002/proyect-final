from icrawler.builtin import BingImageCrawler
import os

def filter_images_by_extension(download_path, allowed_extensions):
    """Elimina archivos que no tengan la extensión permitida."""
    for filename in os.listdir(download_path):
        if not any(filename.endswith(ext) for ext in allowed_extensions):
            os.remove(os.path.join(download_path, filename))

def download_images(search_term, num_images, download_path, allowed_extensions=['.jpg', '.png']):

    crawler = BingImageCrawler(storage={'root_dir': download_path})
    
    crawler.crawl(keyword=search_term, max_num=num_images, file_idx_offset=0)

    filter_images_by_extension(download_path, allowed_extensions)

download_images(
    "fat male frontal body", 
    50, 
    "./fat_images2", 
    allowed_extensions=['.jpg', '.png','jpeg']
)
