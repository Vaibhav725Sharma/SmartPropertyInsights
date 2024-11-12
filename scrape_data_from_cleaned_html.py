import os
from bs4 import BeautifulSoup
import pandas as pd

# Folder containing the HTML files
folder_path = './Cleaned Html files'

# Initialize a list to store each property’s data
properties = []

def extract_text(soup_element, default=None):
    """Extracts text from a BeautifulSoup element if it exists; otherwise, returns a default value."""
    return soup_element.get_text(strip=True) if soup_element else default

def find_listing(soup):
    """Attempt to find listings using multiple selectors."""
    selectors = ['.resBuy__outerTupleWrap', '.tupleNew__outerTupleWrap', '.PseudoTupleRevamp__outerTupleWrap']
    for selector in selectors:
        listings = soup.select(selector)
        if listings:
            return listings
    return []

# Process each HTML file in the specified folder
for filename in os.listdir(folder_path):
    if filename.startswith("cleaned_page_") and filename.endswith(".html"):
        file_path = os.path.join(folder_path, filename)
        
        # Read and parse each HTML file
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            listings = find_listing(soup)

            print(f"{filename} - Found {len(listings)} listings")
            if len(listings) < 25:
                print(f"Warning: Expected around 25 listings, but found {len(listings)} in {filename}")

            # Extract property data from each listing
            for listing in listings:
                property_info = {}

                # Image URL
                image = listing.select_one('.resBuy__imageContainer img') or listing.select_one('.tupleNew__imgWrap img')
                property_info['Image_URL'] = image['src'] if image and 'src' in image.attrs else None

                # Featured Badge
                featured_badge = listing.select_one('.imgItems__tag') or listing.select_one('.ImgItem__tag')
                property_info['Featured'] = extract_text(featured_badge, default="No")

                # Shortlist Button
                property_info['Shortlisted'] = 'Yes' if listing.select_one('.icon_shortlist, .ImgItem__shortlistImage') else 'No'

                # Location Name
                location_name = listing.select_one('.resBuy__locationName') or listing.select_one('.tupleNew__locationName')
                property_info['Location_Name'] = extract_text(location_name)

                # Rating
                rating = listing.select_one('.resBuy__locRatings span') or listing.select_one('.tupleNew__locRatings span')
                property_info['Rating'] = extract_text(rating)

                # Tags
                tags = listing.select('.resBuy__contentTags span, .tupleNew__contentTags div')
                property_info['Tags'] = ', '.join(extract_text(tag) for tag in tags) if tags else None

                # Property Type and Link
                heading = listing.select_one('.resBuy__propertyHeading') or listing.select_one('.tupleNew__propertyHeading')
                if heading:
                    property_info['Property_Type'] = extract_text(heading)
                    property_info['Property_Link'] = heading.get('href', None)

                # Price and Price per Sqft
                price = listing.select_one('.resBuy__priceValWrap span, .tupleNew__priceValWrap span')
                property_info['Price'] = extract_text(price)

                price_per_sqft = listing.select_one('.resBuy__area2Type, .tupleNew__perSqftWrap')
                property_info['Price_per_sqft'] = extract_text(price_per_sqft)

                # Possession Status
                possession_status = listing.select_one('.resBuy__possessionBy, .tupleNew__fomoWrap')
                property_info['Possession_Status'] = extract_text(possession_status)

                # Highlights
                highlights = listing.select('.resBuy__unitHighlightTxt, .tupleNew__highlightTxt')
                property_info['Highlights'] = ', '.join(extract_text(highlight) for highlight in highlights)

                # Dealer Information
                dealer_name = listing.select_one('.resBuy__pbL2, .tupleNew__pbL2')
                property_info['Dealer_Name'] = extract_text(dealer_name)

                dealer_badge = listing.select_one('.resBuy__fdBadge, .ImgItem__badge')
                property_info['Dealer_Badge'] = extract_text(dealer_badge, default="None")

                # Contact Options
                property_info['View_Number'] = 'Available' if listing.select_one('.resBuy__viewNumber, .tupleNew__contactCta') else 'Not Available'
                property_info['Chat_Now'] = 'Available' if listing.select_one('.iconS_srpMob_20') else 'Not Available'
                property_info['Call'] = 'Available' if listing.select_one('.iconS_srpShortlist_30, .tupleNew__callIcon') else 'Not Available'

                # Append each property info dictionary to the list
                properties.append(property_info)

# Convert the data to a DataFrame and save it to a CSV file
df = pd.DataFrame(properties)
df.to_csv('property_listings.csv', index=False)

print("Data successfully saved to 'property_listings.csv'")
