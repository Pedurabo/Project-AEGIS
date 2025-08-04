<?php

namespace PenetrationTools\Chat;

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Monolog\Logger;
use Monolog\Handler\StreamHandler;

class ChatServer implements MessageComponentInterface
{
    protected $clients;
    protected $logger;

    public function __construct()
    {
        $this->clients = new \SplObjectStorage;
        $this->logger = new Logger('chat_server');
        $this->logger->pushHandler(new StreamHandler('logs/chat.log', Logger::INFO));
    }

    public function onOpen(ConnectionInterface $conn)
    {
        $this->clients->attach($conn);
        $this->logger->info("New connection! ({$conn->resourceId})");
        
        // Send welcome message
        $conn->send(json_encode([
            'type' => 'system',
            'message' => 'Welcome to Penetration Tools Chat!',
            'timestamp' => date('Y-m-d H:i:s')
        ]));
    }

    public function onMessage(ConnectionInterface $from, $msg)
    {
        $data = json_decode($msg, true);
        
        if (!$data) {
            $data = [
                'type' => 'message',
                'content' => $msg,
                'user' => 'Anonymous',
                'timestamp' => date('Y-m-d H:i:s')
            ];
        }

        $this->logger->info("Message from {$from->resourceId}: " . json_encode($data));

        foreach ($this->clients as $client) {
            if ($from !== $client) {
                $client->send(json_encode($data));
            }
        }
    }

    public function onClose(ConnectionInterface $conn)
    {
        $this->clients->detach($conn);
        $this->logger->info("Connection {$conn->resourceId} has disconnected");
    }

    public function onError(ConnectionInterface $conn, \Exception $e)
    {
        $this->logger->error("An error has occurred: {$e->getMessage()}");
        $conn->close();
    }
} 