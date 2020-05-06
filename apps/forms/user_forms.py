from wtforms import Form, StringField, PasswordField, validators


class LoginForm(Form):
    username = StringField(
        label="用户名: ",
        validators=[
            validators.DataRequired("用户名必须填写!"),
            validators.Length(min=6, max=16, message="用户名最短为6个字符, 最长为16个字符")
        ],
        # render_kw={"class": "form-control", "placeholder": "请输入用户名"}
        render_kw={"class": "layui-input", "placeholder": "请输入用户名"}
    )

    password = PasswordField(
        label="密码: ",
        validators=[
            validators.DataRequired(message="密码必须填写!"),
            validators.Length(min=8, max=16, message="密码最短8个字符, 最长16个字符")
        ],
        # render_kw={"class": "form-control", "placeholder": "请输入密码"}
        render_kw={"class": "layui-input", "placeholder": "请输入密码"}

    )


class RegisterForm(LoginForm):
    password1 = PasswordField(
        label="确认密码: ",
        validators=[
            validators.DataRequired(message="密码必须填写!"),
            validators.EqualTo("password", message="两次输入的密码不一致!")
        ],
        # render_kw={"class": "form-control", "placeholder": "请确认密码"}
        render_kw={"class": "layui-input", "placeholder": "请确认密码"}

    )
