from config.claud_config import CLAUD_CLIENT


async def postCloudMsg(content: str):
    msg_from_claud = CLAUD_CLIENT.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ]
    )

    return msg_from_claud
