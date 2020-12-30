<div id="posts" class="span-15">
    % for post in posts:
    <div class="post">
        <strong>
            <a href="/{{ post.username }}">
                {{ post.username }}
            </a>
        </strong>
        {{ post.content }}
        <div class="date">{{ post.posttime }}</div>
    </div>
    % end
</div>