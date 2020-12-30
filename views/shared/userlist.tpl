<ul class="user-list">
    % for user in users:
    <li>
        <a href="/{{ user.username }}">
            {{ user.username }}
        </a>
    </li>
    % end
</ul>