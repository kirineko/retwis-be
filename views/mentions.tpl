% include('shared/header.tpl', username=loginname)

<div class="span-24">
    <div class="span-16">
        <h2>Mentions of: {{ username }}</h2>

        % if username != loginname:
        <div class="box">
            % if not isfollowing:
            <a href="/{{ loginname }}/follow/{{ username }}">Following</a>
            % else:
            <a href="/{{ loginname }}/unfollow/{{ username }}">Stop Following</a>
            % end
        </div>
        % end

        % include('shared/posts.tpl', posts=posts)
    </div>
</div>

% include('shared/footer.tpl')