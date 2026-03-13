import requests
import xml.etree.ElementTree as ET


def fetch_arxiv_papers(query, max_results=20):

    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"

    response = requests.get(url)

    root = ET.fromstring(response.text)

    papers = []

    namespace = {"atom": "http://www.w3.org/2005/Atom"}

    for entry in root.findall("atom:entry", namespace):

        title = entry.find("atom:title", namespace).text
        summary = entry.find("atom:summary", namespace).text
        link = entry.find("atom:id", namespace).text

        papers.append({
            "title": title.strip(),
            "summary": summary.strip(),
            "link": link
        })

    return papers