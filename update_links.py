import re
from duckduckgo_search import DDGS

def search(query):
    print("Performing search...")
    results = []
    try:
        with DDGS() as ddgs:
            search_results = list(ddgs.text(query, max_results=5))
            for result in search_results:
                results.append({
                    "url": result.get("href", ""),
                    "title": result.get("title", "")
                })
        return results
    except Exception as e:
        print(f"Search failed: {e}")
        return []

def main():
    query = '"Erison Rosa de Oliveira Barros"'
    results = search(query)

    if not results:
        print("No new links found.")
        return

    try:
        with open('README.md', 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print("README.md not found.")
        return

    # Extract existing links to avoid duplicates
    links_section_match = re.search(r'## Links\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if not links_section_match:
        print("Could not find '## Links' section in README.md")
        return

    existing_links_text = links_section_match.group(1)
    existing_urls = re.findall(r'\]\((https?://[^\)]+)\)', existing_links_text)

    new_links_formatted = []
    for res in results:
        url = res['url']
        if url and url not in existing_urls:
            title = res.get('title', 'Novo Link')
            formatted = f"- [Search Result]({url}) 👨🏼‍🏫 - {title}: {url}"
            new_links_formatted.append(formatted)

    if not new_links_formatted:
        print("No new relevant links to add.")
        return

    print("Adding new links:")
    for link in new_links_formatted:
        print(link)

    # Insert new links
    insertion_point = links_section_match.end(1)

    new_content = content[:insertion_point]
    if not new_content.endswith('\n'):
        new_content += '\n'

    for link in new_links_formatted:
        new_content += link + '\n'

    new_content += content[insertion_point:]

    with open('README.md', 'w') as f:
        f.write(new_content)
    print("README.md updated.")

if __name__ == "__main__":
    main()
