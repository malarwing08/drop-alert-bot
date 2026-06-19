import time
import requests

# Replace with your NEW Discord webhook URL
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1517542262102294550/XBgWKaOFaGOirduuQ9ws-YXblB9SFulS7jlyqDyVno-t6OHLKHTy3hsMXIBLApodv2va"

PRODUCT_URLS = [
    "https://p-bandai.com/us/item/N2856354006",
    "https://p-bandai.com/us/item/N9061360004",
    "https://p-bandai.com/us/item/N9061361004",
    "https://p-bandai.com/us/item/N2835216004"
]

alerted = set()

def send_discord(message):
    try:
        requests.post(
            DISCORD_WEBHOOK,
            json={"content": message},
            timeout=15
        )
    except Exception as e:
        print("Discord error:", e)

def check_product(url):
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=15
    )

    text = response.text.lower()

    stock_keywords = [
        "add to cart",
        "buy now",
        "pre-order",
        "preorder",
        "in stock"
    ]

    sold_out_keywords = [
        "sold out",
        "out of stock",
        "unavailable"
    ]

    has_stock = any(keyword in text for keyword in stock_keywords)
    sold_out = any(keyword in text for keyword in sold_out_keywords)

    return has_stock and not sold_out

print("Bot started...")

send_discord("✅ P-Bandai monitor started.")

while True:
    try:
        for url in PRODUCT_URLS:

            print(f"Checking: {url}")

            if check_product(url):

                if url not in alerted:

                    send_discord(
                        f"🚨 PRODUCT AVAILABLE!\n{url}"
                    )

                    alerted.add(url)

                    print(f"ALERT SENT: {url}")

            else:
                if url in alerted:
                    alerted.remove(url)

        time.sleep(60)

    except Exception as e:
        print("Error:", e)
        time.sleep(60)
