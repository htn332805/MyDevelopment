import requests

def main():
    print("Hello, World!")
    response = requests.get("https://api.github.com")
    print(f"GitHub API Status: {response.status_code}")

if __name__ == "__main__":
    main()
