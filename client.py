import os
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

load_dotenv()
console = Console()

def check_api_keys():
    """Check if all required API keys are present in the environment."""
    # Both servers are now launched by the client, so we check for all keys.
    required_keys = ["GROQ_API_KEY", "OPENWEATHER_API_KEY", "NEWS_API_KEY"]
    missing = [key for key in required_keys if not os.getenv(key)]

    if missing:
        console.print(Panel(
            f"[red]❌ Missing API Keys:[/red]\n\n" +
            "\n".join([f"• {key}" for key in missing]) +
            "\n\nAdd them to your .env file!\n\n" +
            "Get free keys at:\n" +
            "• Groq: https://console.groq.com\n" +
            "• Weather: https://openweathermap.org/api\n" +
            "• News: https://newsapi.org",
            title="Configuration Error",
            border_style="red"
        ))
        return False
    return True

async def main():
    """Main function to initialize and run the MCP client and agent."""

    if not check_api_keys():
        return

    console.print(Panel(
        "🚀 [bold]LangGraph MCP Client[/bold] 🚀\n\n"
        "Both servers will be launched automatically via stdio.\n"
        "• Weather Server\n"
        "• News Server\n\n"
        "Connecting to servers...",
        title="Initializing MCP",
        border_style="blue"
    ))

    client = None
    try:
        # Configure and create the MultiServerMCPClient.
        client = MultiServerMCPClient({
            # Define the 'weather' tool server to be launched as a subprocess.
            "weather": {
                "command": "python",
                "args": ["weatherserver.py"],
                "transport": "stdio",
                # Pass the required API key to the subprocess environment.
                "env": {"OPENWEATHER_API_KEY": os.getenv("OPENWEATHER_API_KEY")}
            },
            # Define the 'news' tool server to be launched as a subprocess.
            "news": {
                "command": "python",
                "args": ["newsserver.py"],
                "transport": "stdio",
                # Pass the required API key to the subprocess environment.
                "env": {"NEWS_API_KEY": os.getenv("NEWS_API_KEY")}
            }
        })

        # Asynchronously get the tools from all configured MCP servers.
        tools = await client.get_tools()
        console.print(f"[green]✅ Connected! Found {len(tools)} MCP tools.[/green]")

        # Set up the language model (LLM) from Groq.
        model = ChatGroq(
            model="llama3-8b-8192",
            temperature=0.1,
            api_key=os.getenv("GROQ_API_KEY")
        )

        # Create a ReAct agent that can use the model and the MCP tools.
        agent = create_react_agent(model, tools)

        console.print(Panel(
            "🤖 [bold]MCP Agent Ready![/bold]\n\n"
            "Try these commands:\n"
            "• 'What's the weather in London?'\n"
            "• 'Show me the latest news about AI'\n"
            "• 'Get the weather for Tokyo and find news about space exploration'\n\n"
            "Type 'quit' to exit.",
            title="Ready to Chat",
            border_style="green"
        ))

        # Start the interactive chat loop.
        while True:
            try:
                user_input = console.input("\n[bold blue]mcp>[/bold blue] ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ["quit", "exit", "q"]:
                    console.print("[yellow]Goodbye! 👋[/yellow]")
                    break

                console.print("[dim]Agent thinking and using tools...[/dim]")

                response = await agent.ainvoke({
                    "messages": [{"role": "user", "content": user_input}]
                })

                final_message = response['messages'][-1].content
                console.print(f"\n[green]🤖 Agent:[/green] {final_message}")

            except KeyboardInterrupt:
                console.print("\n[yellow]Goodbye! 👋[/yellow]")
                break
            except Exception as e:
                console.print(f"[red]An error occurred during chat: {str(e)}[/red]")

    except Exception as e:
        console.print(f"[red]Failed to initialize MCP client: {str(e)}[/red]")
        console.print(
            "[bold yellow]Hint:[/bold yellow] Could not connect to a server. "
            "If you are using 'streamable_http', did you remember to start that server in a separate terminal first?"
        )


if __name__ == "__main__":
    asyncio.run(main())