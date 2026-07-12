import kagglehub

# Download latest version
path = kagglehub.dataset_download("dmahajanbe23/bmw-global-automotive-sales")

print("Path to dataset files:", path)
