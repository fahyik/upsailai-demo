import http.server
import socketserver
import threading
from discord.ext import commands


class _ClientContext:
    """A simple class to keep context for the client handler function"""

    def __init__(self, bot: commands.Bot, bot_max_latency: float):
        self.bot = bot
        self.bot_max_latency = bot_max_latency

    def health_status(self):
        """Returns the health status of the Discord bot client"""
        if (
            self.bot.latency > self.bot_max_latency  # Latency too high
            or self.bot.user is None  # Not logged in
            or not self.bot.is_ready()  # Client’s internal cache not ready
            or self.bot.is_closed()  # The websocket connection is closed
        ):
            return "unhealthy", 503  # Return 503 for unhealthy
        return "healthy", 200  # Return 200 for healthy


class HealthCheckHandler(http.server.BaseHTTPRequestHandler):
    """A custom HTTP handler for health checks"""

    def do_GET(self):
        if self.path == '/health':
            message, status_code = self.server.ctx.health_status()

            self.send_response(status_code)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(message.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        """Override to disable logging"""
        return


def start_http_health_check(bot: commands.Bot, port: int = 8080, bot_max_latency: float = 30):
    """Starts the HTTP health check server.

    Args:
        client: The discord.py client object to monitor.
        port: The port to bind the HTTP health check server to.
        bot_max_latency: The maximum acceptable latency (in seconds) for the bot's
            connection to Discord.
    """
    ctx = _ClientContext(bot, bot_max_latency)

    # Define the handler with the context
    handler = HealthCheckHandler
    handler.server_ctx = ctx  # Pass the context to the handler

    # Start the HTTP server in a separate thread
    def run_server():
        with socketserver.TCPServer(("0.0.0.0", port), handler) as httpd:
            httpd.ctx = ctx
            httpd.serve_forever()

    thread = threading.Thread(target=run_server)
    thread.start()
