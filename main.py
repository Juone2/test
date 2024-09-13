# python3 /Users/juwon/Desktop/Develop_Study/discord-bot/test/main.py

import discord
from datetime import datetime, timedelta
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.environ.get('TOKEN_KEY')

CHANNEL_ID = "1052819133093384215"
CATEGORY_IDS = [
    1276183554660761641, 1276183604803928064, 1276183630712016978,
    1276183767974678574, 1276184216459153489, 1276184261430345778,
    1276184313859280929, 1276184503416782968, 1276184672862339178,
    1276184773378834506, 1276184805595414589, 1276184828894777354,
    1276184854140157952
]  # 삭제를 감지할 카테고리 ID 리스트
ROLE_ID = 1243848098325856318  # DM 보낼 역할 ID
REMOVE_ROLE_ID = 978262058065883236 # 삭제할 역할 ID 

if TOKEN:
    print("Token loaded successfully")
else:
    print("Failed to load token")

class MyClient(discord.Client):
    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name="봇 문의 디엠 J"), status=discord.Status.idle)
        print(f'Logged in as {self.user}')

    async def on_guild_channel_delete(self, channel):
        # 채널이 카테고리인지 확인하고, 삭제된 카테고리 ID가 리스트에 포함되어 있는지 확인
        if isinstance(channel, discord.CategoryChannel) and channel.id in CATEGORY_IDS:
            guild = channel.guild
            alert_role = guild.get_role(ROLE_ID)  # 알람을 받을 역할
            remove_role = guild.get_role(REMOVE_ROLE_ID)  # 역할 제거할 대상 역할

            # 알람을 받을 역할이 있는 멤버에게 알림 전송
            if alert_role:
                alert_tasks = [
                    self.send_dm(member, f"'{channel.name}' 카테고리가 삭제되어 보내는 알림 DM 입니다.")
                    for member in guild.members
                    if alert_role in member.roles
                ]
                await asyncio.gather(*alert_tasks)  # 알림 전송을 비동기 처리

            # 역할을 제거할 대상 역할이 있는 멤버에게서 역할 제거 및 알림 전송
            if remove_role:
                remove_tasks = [
                    self.remove_role_and_notify(member, remove_role, channel.name)
                    for member in guild.members
                    if remove_role in member.roles
                ]
                await asyncio.gather(*remove_tasks)  # 역할 제거와 알림 전송을 동시에 처리

    async def send_dm(self, member, message):
        """멤버에게 DM을 보내는 함수"""
        try:
            await member.send(message)
            print(f"Sent notification to {member.name}")
        except discord.Forbidden:
            print(f"Failed to send DM to {member.name} due to permissions.")
        except Exception as e:
            print(f"An error occurred while sending DM to {member.name}: {e}")

    async def remove_role_and_notify(self, member, role, category_name):
        """역할을 제거하고 해당 멤버에게 알림을 보내는 함수"""
        try:
            await member.remove_roles(role)  # 역할 제거
            await member.send(f"{category_name} 카테고리가 삭제되어, '{role.name}' 역할이 제거되었습니다.")
            print(f"Removed {role.name} and sent DM to {member.name}")
        except discord.Forbidden:
            print(f"Failed to remove {role.name} from {member.name} due to permissions.")
        except Exception as e:
            print(f"An error occurred while removing {role.name} from {member.name}: {e}")

# 필요한 인텐트 활성화
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

client = MyClient(intents=intents)
client.run(TOKEN)