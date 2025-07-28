<?php
/**
 * vote.php – Increments vote for the selected mensa
 * Usage: vote.php?mensa=garching
 */

header('Content-Type: application/json; charset=utf-8');

$jsonFile = __DIR__ . '/data/votes.json';

// Get mensa parameter
$mensa = $_GET['mensa'] ?? '';
$validMensas = ['mensa_garching', 'mensa_bolzmann', 'mensa_maschinenbau'];

if (!in_array($mensa, $validMensas)) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid mensa']);
    exit;
}

// Read current votes
if (!file_exists($jsonFile)) {
    $votes = [
        "mensa_garching" => 0,
        "mensa_bolzmann" => 0,
        "mensa_maschinenbau" => 0
    ];
} else {
    $votes = json_decode(file_get_contents($jsonFile), true);
}

// Increment vote
$votes[$mensa]++;

// Save updated votes
if (file_put_contents($jsonFile, json_encode($votes, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE)) === false) {
    http_response_code(500);
    echo json_encode(['error' => 'Failed to save votes']);
    exit;
}

// Return updated votes
echo json_encode(['success' => true, 'votes' => $votes]);
?>