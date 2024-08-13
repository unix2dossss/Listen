import requests
import os

access_key = ''  # Replace with your actual Unsplash API key

# List of categories to search for
with open('categories.txt', 'r') as file:
    # Read all lines from the file and strip any leading/trailing whitespace
    categories = [line.strip() for line in file.readlines()]

# Directory to save images
save_dir = "category_images"
os.makedirs(save_dir, exist_ok=True)

# Function to search and download images
def download_image(category):
    query = category.replace(" ", "+")
    url = f"https://api.unsplash.com/search/photos?page=1&query={query}&per_page=1&orientation=landscape&order_by=relevant&client_id={access_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        if 'results' in data and data['results']:
            # Get the URL of the first image in the results
            raw_image_url = data['results'][0]['urls']['raw']
            # Append size parameters to the URL for 1920x1080 resolution
            image_url = f"{raw_image_url}&w=1920&h=1080"

            img_data = requests.get(image_url).content
            file_path = os.path.join(save_dir, f"{category}.jpg")
            with open(file_path, 'wb') as img_file:
                img_file.write(img_data)
            print(f"Downloaded {category}.jpg to {file_path}")
        else:
            print(f"No image found for category: {category}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching image for {category}: {e}")


# Download images for each category
for category in reversed(categories):
    if category == "Places & Travel":
        break
    download_image(category)
