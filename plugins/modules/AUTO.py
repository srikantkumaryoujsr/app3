import asyncio
import requests
import aiohttp
import base64
import pytz
from pytz import utc
from datetime import datetime, timedelta
from pyrogram import filters
from .. import bot as Client
from .. import bot
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from main import AUTH_USERS
from .download import account_login
AUTH_USERS.extend([7224758848])
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pyrogram.errors import FloodWait
LOG_CHANNEL_ID = -1002004338182

def get_current_date():
    # Get the current time in IST
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    yesterday = now - timedelta(days=1)
    formatted_date = yesterday.strftime("%Y-%m-%d")
    return formatted_date

def convert_timestamp_to_datetime(timestamp: int) -> str:
    date_time = datetime.utcfromtimestamp(timestamp)
    return date_time.strftime('%Y-%m-%d')

def get_current_date_vsp():
    # Get the current time in IST
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    yesterday = now - timedelta(days=1)
    day_of_week = yesterday.strftime("%A").upper()  # Full weekday name
    month_name = yesterday.strftime("%B").upper()  # Full month name
    day = yesterday.strftime("%d").zfill(2)  # Day of the month
    year = yesterday.strftime("%Y")  # Year
    return f"{day}-{month_name}-{year}, {day_of_week}"

async def fetch_data(session, url, headers=None):
    async with session.get(url, headers=headers) as response:
        return await response.json()

def decrypt_link(link):
    try:
        decoded_link = base64.b64decode(link)
        key = b'638udh3829162018'
        iv = b'fedcba9876543210'
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_link = unpad(cipher.decrypt(decoded_link), AES.block_size).decode('utf-8')
        return decrypted_link
    except ValueError as ve:
        print(f"Padding error while decrypting link: {ve}")
    except Exception as e:
        print(f"Error decrypting link: {e}")
    
scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")

@Client.on_message(filters.command("GDTEST") & filters.user(AUTH_USERS))
async def start_subjects_command(bot, message):
    await all_subject_send(bot)

async def all_subject_send(bot):
    subject_and_channel = {1142: (-1002289423851, 2), 1143: (-1002289423851, 3), 1144: (-1002289423851, 4), 1145: (-1002289423851, 5), 1146: (-1002289423851, 6), 1147: (-1002289423851, 7), 1151: (-1002289423851, 304)}
    
    for subjectid, (chatid, message_thread_id) in subject_and_channel.items():
        try:
            await account_logins(bot, subjectid, chatid, message_thread_id)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await account_logins(bot, subjectid, chatid, message_thread_id)
        except Exception as e:
            print(f"Error processing subject {subjectid}: {e}")

    try:
        await bot.send_message(
            chat_id=-1002289423851,
            text=f"**❤️ᴅᴇᴀʀ ꜱᴛᴜᴅᴇɴᴛ ᴀᴀᴘᴋɪ ᴄʟᴀꜱꜱ ᴜᴘᴅᴀᴛᴇ ʜᴏ ɢɪ ʜᴀɪ ❤️**\n\n**[ॐ] ᴅᴀᴛᴇ & ᴅᴀʏ : ➣ {get_current_date_vsp()}**\n\n**ʀᴇᴀᴄᴛɪᴏɴ❤️**", message_thread_id = 1
        )
    except Exception as e:
        print(f"Failed to send end message: {e}")

async def account_logins(bot, subjectid, chatid, message_thread_id):
    userid = "189678"
    async with aiohttp.ClientSession() as session:
        try:
            token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjQzMDIyMzEiLCJlbWFpbCI6InNhdXJhYmhrYXVzaGlrc2hhcm1hc0BnbWFpbC5jb20iLCJ0aW1lc3RhbXAiOjE3MTUxNDg3ODl9.YHQvtTXSjEsaytQI1p2TVzb0faIm5R3e96LVKtCsZQU"
            hdr1 = {
                'auth-key': 'appxapi',
                'authorization': token,
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9'
            }
            
            res1 = await fetch_data(session, f"https://rozgarapinew.teachx.in/get/mycourse?userid={userid}", headers=hdr1)
            bdetail = res1.get("data", [])
           
            bname = bdetail[0]["course_name"]
            
            all_urls = ""
            couserid = []
            res3 = await fetch_data(session, f"https://rozgarapinew.teachx.in/get/alltopicfrmlivecourseclass?courseid=204&subjectid={subjectid}&start=-1", headers=hdr1)
            topic = res3.get("data", [])
            
            topicids = [i["topicid"] for i in topic]
            
            videos = []  
            all_important = {}  
            all_urls = ""
            for t in topicids:
                url = f"https://rozgarapinew.teachx.in/get/livecourseclassbycoursesubtopconceptapiv3?courseid=204&subjectid={subjectid}&topicid={t}&start=-1&conceptid="
                
                res4 = await fetch_data(session, url, headers=hdr1)
                videodata = res4.get("data", [])
                
                try:
                    for i in videodata:
                        couserid.append(i["id"])
                        
                except Exception as e:
                    print(e)
            for c in couserid:
                url = f"https://rozgarapinew.teachx.in/get/fetchVideoDetailsById?course_id=204&video_id={c}&ytflag=0&folder_wise_course=0"
                res4 = requests.get(url, headers=hdr1).json()
                video = res4.get("data", [])
                videos.append(video)
              
            for i in videos:
                try:
                    all_important[convert_timestamp_to_datetime(i["strtotime"])] = {
                        "title": i["Title"],
                        'pdf_link': decrypt_link(i['pdf_link'].replace(":", "=").replace("ZmVkY2JhOTg3NjU0MzIxMA", "==").split(',')[0]) if i.get("pdf_link") else "",
                        'pdf_link2': decrypt_link(i['pdf_link2'].replace(":", "=").replace("ZmVkY2JhOTg3NjU0MzIxMA", "==").split(',')[0]) if i.get("pdf_link2") else "",
                        'download_link': decrypt_link(i['download_link'].replace(":", "=").replace("ZmVkY2JhOTg3NjU0MzIxMA", "==").split(',')[0]).replace("720p", "720p") if i.get("download_link") else ""
                    }
                    
                except Exception:
                    pass
                            
            date = get_current_date()
            if date not in all_important:
                messages = {f"{get_current_date_vsp()}\n कल इस Subject की कोई Class नहीं हुआ\n"}
                
                if subjectid in messages:
                    await bot.send_message(chatid, text=messages[subjectid], message_thread_id=message_thread_id)
                return

            data = all_important.get(date, {})
            title = data.get("title")
            
            video = data.get("download_link")
            
            pdf_1 = data.get("pdf_link")
            
            pdf_2 = data.get("pdf_link2")
            
            if video:
                all_urls += f"{title}: {video}"
            if pdf_1:
                all_urls += f"\n{title} : {pdf_1}"
            if pdf_2:
                all_urls += f"\n{title} : {pdf_2}"
            
            if all_urls:
                with open(f"{title[:15]}.txt", 'w', encoding='utf-8') as f:
                    f.write(all_urls)
            print(all_urls)
            await account_login(bot, all_urls, bname, chatid, message_thread_id)
        
        except Exception as e:
            print(f"An error occurred: {e}")

# Scheduler setup
scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")

# Schedule setting command
@Client.on_message(filters.command("setschedule") & filters.user(AUTH_USERS))
async def set_schedule(bot, message):
    try:
        _, hour, minute = message.text.split()
        hour, minute = int(hour), int(minute)

        # Remove existing job and set a new one
        scheduler.remove_all_jobs()
        scheduler.add_job(
            func=all_subject_send,
            trigger=CronTrigger(hour=hour, minute=minute, second=0, timezone="Asia/Kolkata"),
            args=[bot]
        )

        await message.reply(f"Schedule set to {hour}:{minute} IST successfully.")
        
    except Exception as e:
        await message.reply(f"Error setting schedule: {e}")

# Start scheduler
scheduler.start()
