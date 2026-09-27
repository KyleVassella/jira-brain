from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()          # loads .env into environment variables
client = Anthropic()   # reads ANTHROPIC_API_KEY automatically

resp = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=300,
    messages=[{"role": "user", "content": "In one sentence, what is a Jira epic?"}],
)
print(resp.content[0].text)

resp2 = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=100,
    messages=[{"role": "user", "content": "What did I just ask you?"}],
)
print(resp2.content[0].text)