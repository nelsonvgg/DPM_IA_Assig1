from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from pyngrok import ngrok

# Azure Computer Vision credentials
AZURE_COMPUTER_VISION_KEY = "ChfecyUFiPg2gpLJjitwZQXCQtDhZF4vtjHHOiZK5bZ7GswGYKYAJQQJ99BCACYeBjFXJ3w3AAAFACOGDiHF"
AZURE_COMPUTER_VISION_ENDPOINT = "https://nvgg-domain.cognitiveservices.azure.com/"

# Test image URL
local_image_url = "http://127.0.0.1:5000/images/4b1f94e030cd4193be65cf36b1865b32.png"  # Replace with a valid image URL

def test_generate_description():
    # Start ngrok to expose the local server
    ngrok_tunnel = ngrok.connect(5000)  # Returns an NgrokTunnel object
    public_url = ngrok_tunnel.public_url  # Extract the public URL as a string
    print(f"Public URL: {public_url}")

    # Replace the local URL with the ngrok public URL
    public_image_url = local_image_url.replace("http://127.0.0.1:5000", public_url)
    print(f"Public Image URL: {public_image_url}")


    # Authenticate the Computer Vision client
    computervision_client = ComputerVisionClient(
        AZURE_COMPUTER_VISION_ENDPOINT,
        CognitiveServicesCredentials(AZURE_COMPUTER_VISION_KEY)
    )

    try:
        # Analyze the image for a description
        description_result = computervision_client.describe_image(public_image_url)

        # Print the results
        if description_result.captions:
            print("Description:")
            for caption in description_result.captions:
                print(f" - {caption.text} (confidence: {caption.confidence:.2f})")
        else:
            print("No description could be generated for this image.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Stop ngrok when done
        ngrok.disconnect(public_url)

if __name__ == "__main__":
    test_generate_description()