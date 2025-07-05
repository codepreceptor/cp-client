import requests
import json
import os
import time

CONFIG_FILE = ".cp_config.json"

def save_config(server_url, api_key):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"server_url": server_url, "api_key": api_key}, f)

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE) as f:
        return json.load(f)

def pretty_print_json(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))

def validate_api(server_url, api_key):
    try:
        response = requests.get(
            f"{server_url}/api/available_tools",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        if response.status_code == 200:
            return response.json().get("tools", [])
        else:
            print("❌ Invalid API key or server not reachable.")
            return None
    except Exception as e:
        print("❌ Error connecting to server:", e)
        return None

def prompt_and_save_config():
    print('Script is under Development Phase, So you may need to manually fetch backened Source.')
    server_url = input("Enter your server URL (e.g., https://codepreceptor.com): ").strip().rstrip("/")
    api_key = input("Enter your API key: ").strip()
    tools = validate_api(server_url, api_key)
    if tools is not None:
        save_config(server_url, api_key)
        print("✅ API key validated and saved!")
        return server_url, api_key, tools
    else:
        print("❌ Validation failed. Try again.")
        return prompt_and_save_config()

def shorten_url(server_url, api_key):
    url = input("Enter URL to shorten: ").strip()
    res = requests.post(
        f"{server_url}/api/shorten-url",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"url": url}
    )
    pretty_print_json(res.json())

def list_links(server_url, api_key):
    res = requests.get(
        f"{server_url}/api/my-links",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    data = res.json()
    print(f"User: {data.get('username')}")
    print(f"Total links: {data.get('total_links')}")
    for link in data.get("short_links", []):
        print(f"\n🔗 Short URL: {link.get('short_url')}")
        print(f"  Click Times: {link.get('click_times', [])}")
        print(f"  Clicks by Day: {link.get('clicks_by_day', {})}")

def delete_link(server_url, api_key):
    short_url = input("Enter short URL to delete: ").strip()
    res = requests.post(
        f"{server_url}/api/delete-short-url",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"short_url": short_url}
    )
    pretty_print_json(res.json())

def usage_stats(server_url, api_key):
    res = requests.get(
        f"{server_url}/api/usage",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    pretty_print_json(res.json())


def monitor_clicks(server_url, api_key):
    print("🟢 Monitoring clicks every 5 seconds... Press Ctrl+C to stop.")
    last_counts = {}

    def process_links(endpoint, label, key):
        try:
            res = requests.get(
                f"{server_url}{endpoint}",
                headers={"Authorization": f"Bearer {api_key}"}
            )
            data = res.json()
            username = data.get("username", "Unknown")
            links = data.get(key, [])
            updated = False

            for link in links:
                url = link.get("short_url") or link.get("location_url") or "❓ Unknown URL"
                click_times = link.get("click_times", [])
                clicks_by_day = link.get("clicks_by_day", {})
                countries = link.get("countries", [])
                states = link.get("state", [])
                regions = link.get("region", [])

                current_count = len(click_times)
                previous_count = last_counts.get(url, -1)

                if current_count != previous_count:
                    if not updated:
                        print(f"\n--- {label} | {username} ---")
                        updated = True

                    print(f"{url} ➜ Total Clicks: {current_count}")
                    print(f"  Clicks by Day: {clicks_by_day}")

                    for i in range(current_count):
                        click_time = click_times[i] if i < len(click_times) else "?"
                        country = countries[i] if i < len(countries) else "?"
                        state = states[i] if i < len(states) else "?"
                        region = regions[i] if i < len(regions) else "?"
                        map_url = link.get("map_url", [])
                        maps = map_url[i] if i < len(map_url) else None

                        location_str = f"📍 {state}, {region}, {country}"
                        print(f"    🕒 {click_time} | {location_str}")
                        if maps:
                            print(f"       🗺️ Map: {maps}")

                    last_counts[url] = current_count

        except Exception as e:
            print(f"❌ Error fetching {label}:", e)

    try:
        while True:
            process_links("/api/my-links", "Short Links", "short_links")
            process_links("/api/my-location-links", "Location Links", "location_links")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped.")



def ip_lookup(server_url, api_key):
    ip = input("Enter IP to lookup: ").strip()
    res = requests.post(
        f"{server_url}/ip-look",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"ip": ip}
    )
    pretty_print_json(res.json())

def show_menu(tools):
    print("\nAvailable API Tools:")
    for i, tool in enumerate(tools, 1):
        print(f"{i}. {tool['name']} - {tool['description']}")
    print("0. Exit")

def create_location_url(server_url, api_key):
    url = input("Enter URL to generate location-based link: ").strip()
    res = requests.post(
        f"{server_url}/api/location-url",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"url": url}
    )
    pretty_print_json(res.json())

def list_location_links(server_url, api_key):
    res = requests.get(
        f"{server_url}/api/my-location-links",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    data = res.json()
    print(f"User: {data.get('username')}")
    print(f"Total location links: {data.get('total_links')}")
    for link in data.get("location_links", []):
        print(f"  🌍 Location URL: {link}")



def main():
    config = load_config()
    if config:
        server_url, api_key = config["server_url"], config["api_key"]
        tools = validate_api(server_url, api_key)
        if tools is None:
            print("❌ Saved API key invalid.")
            server_url, api_key, tools = prompt_and_save_config()
    else:
        server_url, api_key, tools = prompt_and_save_config()

    actions = {
    "Shorten URL": shorten_url,
    "My Short Links": list_links,
    "Delete Short URL": delete_link,
    "Usage (Daily)": usage_stats,
    "Monitor Clicks": monitor_clicks,
    "IP Lookup": ip_lookup,
    "Create Location URL": create_location_url,
    "My Location Links": list_location_links
     }

    while True:
        show_menu(tools)
        choice = input("Select a tool by number: ").strip()
        if choice == "0":
            print("👋 Exiting.")
            break
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(tools):
                tool_name = tools[idx]["name"]
                func = actions.get(tool_name)
                if func:
                    if tool_name == "IP Lookup":
                        func(server_url, api_key)
                    else:
                        func(server_url, api_key)
                else:
                    print("❌ Tool not implemented yet in script.")
            else:
                print("❌ Invalid choice.")
        except Exception as e:
            print("❌ Error:", e)

if __name__ == "__main__":
    main()
