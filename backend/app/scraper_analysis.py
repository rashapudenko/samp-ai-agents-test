"""
Script to analyze the structure of Snyk vulnerabilities page.
This will help us understand the HTML structure for proper parsing.
"""
import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint

def analyze_page_structure(url="https://security.snyk.io/vuln/pip/"):
    """
    Analyze current structure of the Snyk vulnerabilities page
    """
    # Fetch the page
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        return None
    
    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Structure analysis
    page_structure = {
        "title": soup.title.text if soup.title else "No title found",
        "vulnerability_count": None,
        "sample_vulnerability": None,
        "pagination_info": None,
        "selectors": {}
    }
    
    # Try to find vulnerability items
    # Let's try different possible selectors
    potential_vuln_selectors = [
        '.vulns-table tbody tr',
        '.vulnerability-item',
        '.vulncard',
        '.vuln-list-item',
        'table.table tbody tr'
    ]
    
    vulnerabilities = []
    selected_selector = None
    
    for selector in potential_vuln_selectors:
        items = soup.select(selector)
        if items and len(items) > 0:
            selected_selector = selector
            print(f"Found vulnerability items using selector: {selector}")
            print(f"Number of items found: {len(items)}")
            
            # Analyze first item structure
            first_item = items[0]
            print("\nStructure of first vulnerability item:")
            print("-------------------------------------")
            print(f"HTML: {first_item}")
            print("\nAttributes:")
            print(first_item.attrs)
            
            # For each vulnerability item, try to extract key information
            for i, item in enumerate(items[:5]):  # Analyze first 5 items
                vuln = {"raw_html": str(item)}
                
                # Get all child elements with class names
                elements_with_class = item.find_all(class_=True)
                for element in elements_with_class:
                    class_name = " ".join(element.get('class'))
                    text = element.get_text(strip=True)
                    if text:
                        vuln[f"class_{class_name}"] = text
                
                # Try to find elements by common ID patterns
                id_elements = item.find_all(id=True)
                for element in id_elements:
                    id_name = element.get('id')
                    text = element.get_text(strip=True)
                    if text:
                        vuln[f"id_{id_name}"] = text
                
                # Look for data attributes
                for attr, value in item.attrs.items():
                    if attr.startswith('data-'):
                        vuln[attr] = value
                
                # Check for links
                links = item.find_all('a')
                if links:
                    vuln['links'] = [{'href': a.get('href'), 'text': a.get_text(strip=True)} for a in links]
                
                vulnerabilities.append(vuln)
                if i == 0:
                    page_structure["sample_vulnerability"] = vuln
            
            page_structure["vulnerabilities"] = vulnerabilities[:5]
            page_structure["selectors"]["vulnerability_item"] = selector
            break
    
    # Try to find pagination information
    pagination_selectors = [
        '.pagination',
        '.page-navigation',
        '.pages',
        'nav[aria-label="pagination"]'
    ]
    
    for selector in pagination_selectors:
        pagination = soup.select(selector)
        if pagination:
            page_structure["pagination_info"] = {
                "selector": selector,
                "html": str(pagination[0]),
                "links": []
            }
            pagination_links = pagination[0].find_all('a')
            for link in pagination_links:
                page_structure["pagination_info"]["links"].append({
                    "href": link.get('href'),
                    "text": link.get_text(strip=True)
                })
            break
    
    # Try to determine vulnerability count
    count_elements = [
        soup.select_one('.vuln-count'),
        soup.select_one('.results-count'),
        soup.select_one('.count')
    ]
    
    for element in count_elements:
        if element:
            page_structure["vulnerability_count"] = element.get_text(strip=True)
            break
    
    return page_structure

if __name__ == "__main__":
    structure = analyze_page_structure()
    if structure:
        print("\n===== PAGE STRUCTURE ANALYSIS =====\n")
        pprint(structure)
        
        # Save the structure to a file for reference
        with open('page_structure.json', 'w') as f:
            json.dump(structure, f, indent=4)
        print("\nAnalysis saved to page_structure.json")
    else:
        print("Failed to analyze page structure")