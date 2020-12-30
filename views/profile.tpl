% include('shared/header.tpl', username=loginname)

<div class="span-24">
    <div class="span-16">
        <h2> {{ username }}</h2>

        % if username != loginname:
        <div class="box">
            % if not isfollowing:
            <a href="/{{ loginname }}/follow/{{ username }}">Following</a>
            % else:
            <a href="/{{ loginname }}/unfollow/{{ username }}">Stop Following</a>
            % end
            | <a href="/mentions/{{ username }}">See Mentions</a>
        </div>
        % end

        % include('shared/posts.tpl', posts=posts)
    </div>


    <div class="span-7 last">
        <div class="box">
            <h4>Followers: {{ followers_num }}</h4>
            % include('shared/userlist.tpl', users=followers)
        </div>

        <div class="box">
            <h4>Following: {{ following_num }}</h4>
            % include('shared/userlist.tpl', users=following)
        </div>
    </div>
</div>

% include('shared/footer.tpl')