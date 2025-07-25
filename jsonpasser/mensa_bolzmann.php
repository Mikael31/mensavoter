<?php
/*  index.php
 *  GET  or POST  ➜  fetch current (or supplied) KW JSON and overwrite
 *  other methods ➜  fallback directory listing
 */

/* ------------  treat GET **and** POST the same ----------------------- */
if ($_SERVER['REQUEST_METHOD'] === "POST" || $_SERVER['REQUEST_METHOD'] === "GET") {
    header('content-type: text/plain; charset=utf-8');

    /* --- aktuelle ISO-Woche / Jahr als Default ------------------------- */
    $now      = new DateTime();
    $defYear  = $now->format('o');   // ISO-Jahr
    $defWeek  = $now->format('W');   // 01-53, bereits zweistellig

    $year = $_REQUEST['year'] ?? $defYear;
    $week = $_REQUEST['week'] ?? $defWeek;

    /* --- JSON holen ---------------------------------------------------- */
    $json = @file_get_contents(
        "https://tum-dev.github.io/eat-api/stucafe-garching/$year/$week.json"
    );

    if ($json === false) {
        http_response_code(502);
        exit("Upstream fetch failed.\n");
    }

    /* --- Nur heutigen Tag behalten ----------------------------------- */
    $todayIso = (new DateTime())->format('Y-m-d');        // z. B. 2025-07-23
    $data     = json_decode($json, true);                 // → Array
    if ($data && isset($data['days']) && is_array($data['days'])) {
        foreach ($data['days'] as $day) {
            if ($day['date'] === $todayIso) {
                $json = json_encode(
                    $day,
                    JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT
                );
                break;
            }
        }
    }

    /* --- Datei speichern ---------------------------------------------- */
    if (!is_dir('data')) mkdir('data', 0755, true);
    $target = 'data/mensa_bolzmann.json';

    if (file_put_contents($target, $json) === false) {
        http_response_code(500);
        exit("Failed to write $target\n");
    }

    echo "$target successfully updated.\n";

} else {
    /* --------- Fallback: simple listing -------------------------------- */
    header('content-type: text/html; charset=utf-8');

    if (!is_dir('data')) {
        echo "<em>No data directory.</em>";
        exit;
    }

    foreach (scandir('data') as $value) {
        if ($value !== '.' && $value !== '..') {
            echo "<a href='data/$value'>$value</a><br/>";
        }
    }
}
exit;
?>