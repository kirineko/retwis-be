% include('shared/header.tpl', username=username)

<div class="span-24">
    <div class="span-16">
        <h2>Timeline</h2>

        Posts from all users.
        <br>

        % include('shared/posts.tpl', posts=posts)
    </div>


    <div class="span-7 last">
        <div class="box">
            <h3>New Users</h3>

            % include('shared/userlist.tpl', users=users)
        </div>
    </div>
</div>

% include('shared/footer.tpl')