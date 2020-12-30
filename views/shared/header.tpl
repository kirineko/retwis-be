<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Retiws</title>
    <link rel="stylesheet" href="/public/css/screen.css">
    <link rel="stylesheet" href="/public/css/custom.css">
</head>
<body>
    <div class="container">
        <div id="header" class="span-24">
            <div class="span-12">
                <br>
                <h1>Retiws</h1>
            </div>

            % if defined('username'):
            <div class="span-12 last right-align">
                <br>
                <br>
                <a href="/">home</a> |
                <a href="/mentions/{{username}}">mentions</a> |
                <a href="/{{username}}">{{username}}</a> |
                <a href="/timeline">timeline</a> |
                <a href="/logout">logout</a>
            </div>
            % end

            <hr>
        </div>