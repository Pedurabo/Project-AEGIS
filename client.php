<?php

require_once 'vendor/autoload.php';

use PenetrationTools\Chat\ChatClient;

if ($argc < 2) {
    echo "Usage: php client.php <username> [server_url]\n";
    echo "Example: php client.php John ws://localhost:8080\n";
    exit(1);
}

$username = $argv[1];
$serverUrl = $argv[2] ?? 'ws://localhost:8080';

echo "Connecting to chat server as: {$username}\n";
echo "Server: {$serverUrl}\n\n";

$client = new ChatClient($username);
$client->connect($serverUrl);

// Keep the script running
while (true) {
    echo "Enter your message (or 'quit' to exit): ";
    $input = trim(fgets(STDIN));
    
    if ($input === 'quit') {
        echo "Goodbye!\n";
        break;
    }
    
    if (!empty($input)) {
        $message = $client->sendMessage($input);
        echo "Sent: {$input}\n";
    }
} 