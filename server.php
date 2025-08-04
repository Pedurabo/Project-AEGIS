<?php

require_once 'vendor/autoload.php';

use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;
use PenetrationTools\Chat\ChatServer;

// Create logs directory if it doesn't exist
if (!is_dir('logs')) {
    mkdir('logs', 0777, true);
}

echo "Starting Penetration Tools Chat Server...\n";
echo "Server will be available at: ws://localhost:8080\n";
echo "Press Ctrl+C to stop the server\n\n";

// Create the server
$server = IoServer::factory(
    new HttpServer(
        new WsServer(
            new ChatServer()
        )
    ),
    8080
);

echo "Chat server is running on port 8080\n";
$server->run(); 