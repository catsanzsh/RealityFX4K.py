import asyncio
import websockets

# List of connected players
connected_players = set()

async def handle_player(websocket, path):
    # Add new player
    connected_players.add(websocket)
    print("New player connected!")

    try:
        async for message in websocket:
            print(f"Received: {message}")

            # Send message to all players except the sender
            for player in connected_players.copy():  # Use a copy to avoid modification errors
                if player != websocket:
                    try:
                        await player.send(message)
                    except websockets.exceptions.ConnectionClosed:
                        connected_players.remove(player)

    except websockets.exceptions.ConnectionClosed:
        print("Player disconnected!")
    finally:
        connected_players.remove(websocket)

async def main():
    async with websockets.serve(handle_player, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # Run forever

# Use asyncio.run() to properly start the server
asyncio.run(main())
