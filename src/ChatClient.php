<?php

namespace PenetrationTools\Chat;

use Ratchet\Client\WebSocket;
use Ratchet\Client\Connector;
use React\EventLoop\Loop;
use Monolog\Logger;
use Monolog\Handler\StreamHandler;

class ChatClient
{
    protected $connector;
    protected $logger;
    protected $username;

    public function __construct($username = 'Anonymous')
    {
        $this->username = $username;
        $this->logger = new Logger('chat_client');
        $this->logger->pushHandler(new StreamHandler('logs/client.log', Logger::INFO));
    }

    public function connect($url = 'ws://localhost:8080')
    {
        $this->logger->info("Connecting to chat server: {$url}");
        
        $connector = new Connector();
        
        $connector($url)->then(
            function (WebSocket $conn) {
                $this->logger->info("Connected to chat server!");
                
                $conn->on('message', function ($msg) {
                    $data = json_decode($msg, true);
                    $this->handleMessage($data);
                });
                
                $conn->on('close', function ($code = null, $reason = null) {
                    $this->logger->info("Connection closed: {$code} - {$reason}");
                });
                
                // Send initial message
                $conn->send(json_encode([
                    'type' => 'join',
                    'user' => $this->username,
                    'timestamp' => date('Y-m-d H:i:s')
                ]));
                
                return $conn;
            },
            function (\Exception $e) {
                $this->logger->error("Could not connect: {$e->getMessage()}");
            }
        );
    }

    protected function handleMessage($data)
    {
        if (!$data) {
            $this->logger->warning("Received invalid message format");
            return;
        }

        switch ($data['type']) {
            case 'system':
                echo "\n[SYSTEM] {$data['message']}\n";
                break;
            case 'message':
                echo "\n[{$data['user']}] {$data['content']}\n";
                break;
            case 'join':
                echo "\n[SYSTEM] {$data['user']} joined the chat\n";
                break;
            default:
                echo "\n[UNKNOWN] " . json_encode($data) . "\n";
        }
    }

    public function sendMessage($content)
    {
        return json_encode([
            'type' => 'message',
            'content' => $content,
            'user' => $this->username,
            'timestamp' => date('Y-m-d H:i:s')
        ]);
    }
} 