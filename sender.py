import httpx
import os
import asyncio

WEBHOOK = os.environ.get("WEBHOOK")
URL = "https://autojoinerchered-default-rtdb.europe-west1.firebasedatabase.app/servers.json?auth=AIzaSyBokCjJ7bIUOk_beo2gWQXst6PKqlFFEpc"
BASE_JOIN = "https://chillihub1.github.io/chillihub-joiner/?placeId=109983668079237&gameInstanceId="

seen = set()
client = httpx.AsyncClient(timeout=3.0, limits=httpx.Limits(max_connections=200, max_keepalive_connections=50))

async def send(job_id):
    join_link = BASE_JOIN + job_id
    payload = {
        "embeds": [{
            "color": 5814783,
            "fields": [
                {"name": "Job ID", "value": job_id, "inline": False},
                {"name": "Join Link", "value": f"[Click to Join]({join_link})", "inline": False}
            ]
        }]
    }
    try:
        await client.post(WEBHOOK, json=payload)
    except:
        pass

async def poll():
    global seen
    while True:
        try:
            r = await client.get(URL)
            if r.status_code != 200:
                await asyncio.sleep(0.01)
                continue
            data = r.json()
            if not isinstance(data, dict):
                await asyncio.sleep(0.01)
                continue
            tasks = []
            for val in data.values():
                job = val.get("jobId")
                if job and job not in seen and len(job) == 36:
                    seen.add(job)
                    tasks.append(send(job))
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
        except:
            pass
        await asyncio.sleep(0.01)

async def main():
    if not WEBHOOK:
        return
    await poll()

if __name__ == "__main__":
    asyncio.run(main())
