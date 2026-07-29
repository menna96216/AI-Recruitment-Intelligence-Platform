from utils.mongodb import client


try:

    client.admin.command("ping")

    print("MongoDB Connection OK")

except Exception as e:

    print(e)