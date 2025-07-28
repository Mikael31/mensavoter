<?php
// reset_votes.php – Resets the votes to 0
$jsonFile = __DIR__ . '/data/votes.json';

$emptyVotes = [
    "mensa_garching" => 0,
    "mensa_bolzmann" => 0,
    "mensa_maschinenbau" => 0
];

if (file_put_contents($jsonFile, json_encode($emptyVotes, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE), LOCK_EX) !== false) {
    echo "Votes reset successfully\n";
} else {
    echo "Failed to reset votes\n";
}
?>