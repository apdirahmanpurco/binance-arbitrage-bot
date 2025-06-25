import requests
import time

def get_p2p_price(fiat, trade_type, asset='USDT', rows=5):
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)"
    }
    payload = {
        "asset": asset,
        "fiat": fiat,
        "merchantCheck": False,
        "page": 1,
        "rows": rows,
        "payTypes": [],
        "publisherType": None,
        "tradeType": trade_type.upper()
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        offers = data.get("data", [])
        prices = [float(offer['adv']['price']) for offer in offers if 'adv' in offer]
        return sum(prices) / len(prices) if prices else None

    except Exception as e:
        print(f"❌ Error fetching {trade_type} {fiat}: {e}")
        return None

while True:
    print("\n🔄 Checking Binance P2P prices...\n")

    myr_buy = get_p2p_price('MYR', 'BUY')
    ngn_sell = get_p2p_price('NGN', 'SELL')

    if myr_buy and ngn_sell:
        print(f"🇲🇾 Buy USDT in MYR: RM {myr_buy:.2f}")
        print(f"🇳🇬 Sell USDT in NGN: ₦ {ngn_sell:.2f}")

        myr_usd = myr_buy / 4.70
        ngn_usd = ngn_sell / 1500
        profit = ((ngn_usd - myr_usd) / myr_usd) * 100

        print(f"📈 Estimated Profit Margin: {profit:.2f}%")

        if profit >= 5:
            print("✅ PROFITABLE OPPORTUNITY DETECTED!")
    else:
        print("⚠️ Could not get both prices.")

    time.sleep(15)
