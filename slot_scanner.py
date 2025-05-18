"""
Colorado DMV Appointment Checker
Author: Oussama Ennaciri

This script checks multiple DMV locations in Colorado for the earliest available
appointment for "First Time CO DL/ID/Permit" and alerts the user when an appointment
in May is found.
"""

import datetime
import asyncio
import webbrowser
import os
from pathlib import Path
from playwright.async_api import async_playwright

# List of DMV locations to check
LOCATIONS_TO_CHECK = [
    "Adams", "Westminster", "Boulder", "Denver NE",
    "Greeley", "Longmont", "Parker", "Aurora", "Golden", "Centennial"
]

DMV_URL = "REDACTED_DMV_URL"
ALARM_FILE = Path("Alarm.mp3")

if not ALARM_FILE.exists():
    raise FileNotFoundError("Alarm.mp3' is in the same folder.")

async def check_location(playwright, location):
    print(f"▶ Checking: {location}", flush=True)
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()

    try:
        await page.goto(DMV_URL, wait_until="domcontentloaded", timeout=30000)

        await page.locator(f"div.QflowObjectItem >> text='{location}'").first.click()
        await page.locator("p:text('First Time CO DL/ID/Permit')").click()
        await page.get_by_role("button", name="Next").click()
        await page.wait_for_selector(".ui-datepicker-calendar", timeout=10000)

        title = await page.locator(".ui-datepicker-title").inner_text()
        month_name, year = title.split()
        month = datetime.datetime.strptime(month_name, "%B").month
        year = int(year)

        days = await page.locator(".ui-datepicker-calendar td a").all_text_contents()
        days = [int(day.strip()) for day in days if day.strip().isdigit()]
        dates = [datetime.date(year, month, day) for day in days]

        if dates:
            earliest = min(dates)
            print(f"✅ {location}: {earliest.strftime('%A, %B %d, %Y')}", flush=True)
            return location, earliest
        else:
            print(f"❌ {location}: No available appointments.", flush=True)
            return location, None

    except Exception as e:
        print(f"⚠️ {location}: Error encountered: {e}", flush=True)
        return location, None
    finally:
        await browser.close()

async def monitor_appointments():
    print("🚦 DMV Appointment Checker Started")

    async with async_playwright() as playwright:
        while True:
            print(f"\n🔄 Checking all locations... ({datetime.datetime.now().strftime('%H:%M:%S')})", flush=True)
            results = [await check_location(playwright, location) for location in LOCATIONS_TO_CHECK]

            available = [(loc, date) for loc, date in results if date]
            if available:
                nearest_loc, nearest_date = min(available, key=lambda x: x[1])
                print(f"\n🏁 Earliest appointment: {nearest_loc} on {nearest_date.strftime('%A, %B %d, %Y')}", flush=True)

                if nearest_date.month == 5:
                    print("\n🚨 May appointment found — opening DMV site and playing alarm!", flush=True)
                    webbrowser.open(DMV_URL)
                    try:
                        os.system(f"afplay '{ALARM_FILE}'")
                    except Exception as e:
                        print(f"⚠️ Alarm failed to play: {e}", flush=True)

                    if nearest_date.day == 16:
                        print("🛑 May 16th appointment found — stopping search.", flush=True)
                        break
            else:
                print("❌ No appointments found at any location.", flush=True)

await monitor_appointments()
