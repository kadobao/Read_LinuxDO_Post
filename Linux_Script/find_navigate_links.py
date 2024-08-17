# Linux_Script/find_navigate_links.py

def find_navigate_links(page):
    eles = page.eles('css:a[href][class="title raw-link raw-topic-link"]')               
    links = eles.get.links()

    return len(links), links