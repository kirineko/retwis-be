
% include('shared/header.tpl', username=username)

<div class="span-24">
    <div class="span-16">
        <div id="updateform" class="box">
            <form action="/post" method="post">
                {{username}}, what's on your mind?
                <textarea name="content" id="" cols="70" rows="3"></textarea>
                <br>
                <input type="submit" value="Update">
            </form>
        </div>

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